from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import authenticate_user, create_access_token, hash_password
from app.schemas.auth import Token
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token(data={"sub": user.nombre_usuario})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.nombre_usuario == form_data.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_pass = hash_password(form_data.password)
    nuevo = Usuario(
        nombre_usuario=form_data.username,
        contraseña=hashed_pass,
        nombres=form_data.username.capitalize(),
        apellidos="Default",
        edad=20,
        email=f"{form_data.username}@test.com",
        id_rol=1
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    token = create_access_token(data={"sub": nuevo.nombre_usuario})
    return {"access_token": token, "token_type": "bearer"}
