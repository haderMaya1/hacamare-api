from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate
from app.utils.security import (
    hash_password, verify_password, create_access_token
)
from app.utils.helpers import get_user_by_username, get_user_by_email


def register_user(db: Session, usuario: UsuarioCreate) -> Usuario:
    """
    Registra un nuevo usuario en la base de datos
    - Valida nombre de usuario y email únicos
    - Asigna rol por defecto si no se especifica
    """
    if get_user_by_username(db, usuario.nombre_usuario):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )

    if get_user_by_email(db, usuario.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Rol por defecto = usuario (id=2) si no viene en la petición
    rol_id = usuario.id_rol
    if rol_id is None:
        rol_usuario = db.query(Rol).filter(Rol.nombre.ilike("usuario")).first()
        if not rol_usuario:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No existe rol por defecto 'usuario'"
            )
        rol_id = rol_usuario.id_rol

    nuevo_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        contraseña=hash_password(usuario.contraseña),
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        edad=usuario.edad,
        email=usuario.email,
        id_rol=rol_id,
        estado_cuenta="activo",
        email_verificado=0
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def authenticate_user(db: Session, nombre_usuario: str, contraseña: str) -> Usuario | None:
    """
    Verifica si el usuario existe, la contraseña es correcta
    y la cuenta está activa.
    """
    usuario = get_user_by_username(db, nombre_usuario)
    if not usuario:
        return None
    if usuario.estado_cuenta != "activo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cuenta {usuario.estado_cuenta}"
        )
    if not verify_password(contraseña, usuario.contraseña):
        return None
    return usuario


def login_user(db: Session, nombre_usuario: str, contraseña: str) -> dict:
    """
    Autentica al usuario y devuelve un token JWT
    """
    usuario = authenticate_user(db, nombre_usuario, contraseña)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Incluimos user_id en 'sub' (importante para get_current_user)
    access_token = create_access_token({"sub": str(usuario.id_usuario)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": usuario.id_usuario,
        "username": usuario.nombre_usuario,
        "rol": usuario.id_rol
    }
