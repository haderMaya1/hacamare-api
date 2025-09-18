from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.services.auth_service import register_user, login_user
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.utils.secutiry import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UsuarioResponse)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return register_user(db, usuario)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(db, form_data.username, form_data.password)

@router.get("/me", response_model=UsuarioResponse)
def read_users_me(current_user: UsuarioResponse = Depends(get_current_user)):
    return current_user
