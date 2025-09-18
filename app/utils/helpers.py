from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.rol import Rol

# ==========================
# EXCEPCIONES PERSONALIZADAS
# ==========================
def not_found_exception(entity: str, entity_id: int):
    """Genera excepción 404 cuando no se encuentra un recurso"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} con id {entity_id} no encontrado"
    )


def unauthorized_exception():
    """Genera excepción 401 de acceso no autorizado"""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado"
    )


def forbidden_exception():
    """Genera excepción 403 de acceso prohibido"""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado"
    )


# ==========================
# RESPUESTAS ESTÁNDAR
# ==========================
def success_response(message: str, data: dict | list | None = None) -> dict:
    """Devuelve una respuesta estándar para éxito"""
    return {
        "message": message,
        "data": data
    }


# ==========================
# USUARIOS
# ==========================
def get_user_by_username(db: Session, nombre_usuario: str):
    """Obtener un usuario por su nombre de usuario"""
    return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

def get_user_by_email(db: Session, email: str):
    """Obtener un usuario por su email"""
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """Obtener un usuario por ID"""
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

# ==========================
# ROLES
# ==========================
def get_rol_by_id(db: Session, id_rol: int):
    """Obtener un rol por ID"""
    return db.query(Rol).filter(Rol.id_rol == id_rol).first()