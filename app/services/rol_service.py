from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate
import json

def crear_rol(db: Session, rol: RolCreate):
    nuevo_rol = Rol(
        nombre=rol.nombre,
        permisos=json.dumps(rol.permisos or {})
    )
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

def obtener_roles(db: Session):
    return db.query(Rol).all()

def obtener_rol_por_id(db: Session, rol_id: int):
    return db.query(Rol).filter(Rol.id_rol == rol_id).first()

def actualizar_rol(db: Session, rol_id: int, rol: RolUpdate):
    db_rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not db_rol:
        return None
    if rol.nombre is not None:
        db_rol.nombre = rol.nombre
    if rol.permisos is not None:
        db_rol.permisos = json.dumps(rol.permisos)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def eliminar_rol(db: Session, rol_id: int):
    db_rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not db_rol:
        return None
    db.delete(db_rol)
    db.commit()
    return db_rol
