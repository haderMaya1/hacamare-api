from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.helpers import get_user_by_username


def register_user(db: Session, usuario: UsuarioCreate) -> Usuario:
    """Registra un nuevo usuario en la base de datos"""
    db_usuario = get_user_by_username(db, usuario.nombre_usuario)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )

    nuevo_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        contraseña=hash_password(usuario.contraseña),
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        edad=usuario.edad,
        email=usuario.email,
        id_rol=usuario.id_rol,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def authenticate_user(db: Session, nombre_usuario: str, contraseña: str) -> Usuario | None:
    """Verifica si el usuario existe y la contraseña es correcta"""
    usuario = get_user_by_username(db, nombre_usuario)
    if not usuario or not verify_password(contraseña, usuario.contraseña):
        return None
    return usuario


def login_user(db: Session, nombre_usuario: str, contraseña: str) -> dict:
    """Autentica al usuario y devuelve un token JWT"""
    usuario = authenticate_user(db, nombre_usuario, contraseña)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": str(usuario.id_usuario)})
    return {"access_token": access_token, "token_type": "bearer"}
