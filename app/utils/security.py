from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.helpers import get_user_by_id
from app.config import settings
from app.utils.permissions import PERMISSIONS
from app.models.usuario import Usuario
from app.models.rol import Rol
from typing import Optional, Callable
import json
import os

# ==========================
# CONTEXTO DE ENCRIPTACIÓN
# ==========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ==========================
# FUNCIONES DE CONTRASEÑAS
# ==========================
def hash_password(password: str) -> str:
    """Hashea la contraseña en texto plano"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ==========================
# FUNCIONES DE TOKENS JWT
# ==========================
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Genera un token JWT con expiración"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """Decodifica y valida un token JWT"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


# ==========================
# DEPENDENCIAS DE ROL
# ==========================

def _role_name_from_user(user: Usuario) -> str:
    # si tu relación rol está cargada: user.rol.nombre
    try:
        return (user.rol.nombre or "").lower()
    except Exception:
        # fallback si no hay relación cargada:
        return {1: "administrador", 2: "usuario"}.get(user.id_rol, "usuario")

def require_permission(permission: str) -> Callable:
    """
    Devuelve una dependencia que exige un permiso determinado.
    Uso: dependencies=[Depends(require_permission("usuarios:read_all"))]
    """
    def dependency(current_user: Usuario = Depends(get_current_user)):
        role = _role_name_from_user(current_user)
        perms = PERMISSIONS.get(role, {})
        if not (perms.get("all") or perms.get(permission)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para realizar esta operación"
            )
        return current_user
    return dependency

def require_role(required: list[str]):
    """
    required: lista de permisos o nombres de rol permitidos.
    Ej: ["admin"]  o  ["usuarios:listar"]
    """
    def wrapper(
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        rol = db.query(Rol).filter(Rol.id_rol == current_user.id_rol).first()
        if not rol:
            raise HTTPException(status_code=403, detail="Rol no encontrado")

        # Si required es un nombre de rol
        if any(req.lower() == rol.nombre.lower() for req in required):
            return current_user

        # Si es permiso, revisa el JSON de permisos
        permisos = json.loads(rol.permisos or "{}")
        if any(permisos.get(req, False) for req in required):
            return current_user

        raise HTTPException(status_code=403, detail="Permiso denegado")
    return wrapper

# ==========================
# DEPENDENCIAS DE USUARIO
# ==========================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtiene el usuario actual a partir del token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user

def require_permission(permission: str):
    """
    Devuelve una dependencia que valida si el usuario tiene
    el permiso solicitado.
    """
    def dependency(current_user: Usuario = Depends(get_current_user)):
        role = current_user.rol.nombre.lower()
        perms = PERMISSIONS.get(role, {})
        if not (perms.get("all") or perms.get(permission)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para esta operación"
            )
        return current_user
    return dependency

def admin_required(current_user: Usuario = Depends(get_current_user)):
    role = _role_name_from_user(current_user)
    if role != "administrador" and not (current_user.id_rol == 1):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")
    return current_user

def owner_or_admin(get_resource_owner_id: Callable[[any], int]):
    """
    Devuelve una dependencia que valida que current_user sea dueño del recurso
    o administrador. get_resource_owner_id es una función que recibe (db, resource_id)
    y devuelve el id del owner. Uso:
      @router.put("/{id}", dependencies=[Depends(owner_or_admin(lambda db, id: get_pub_owner(db, id)))])
    """
    def dependency(resource_id: int, db = Depends(...), current_user: Usuario = Depends(get_current_user)):
        owner_id = get_resource_owner_id(db, resource_id)
        if owner_id != current_user.id_usuario and current_user.id_rol != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
        return current_user
    return dependency