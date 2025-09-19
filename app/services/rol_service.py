from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate

def create_rol(db: Session, rol: RolCreate):
    nuevo_rol = Rol(nombre=rol.nombre)
    if rol.permisos:
        nuevo_rol.set_permisos(rol.permisos)
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

def get_roles(db: Session):
    return db.query(Rol).all()

def get_rol(db: Session, rol_id: int):
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    return rol

def update_rol(db: Session, rol_id: int, rol_update: RolUpdate):
    rol = get_rol(db, rol_id)
    if rol_update.nombre:
        rol.nombre = rol_update.nombre
    if rol_update.permisos is not None:
        rol.set_permisos(rol_update.permisos)
    db.commit()
    db.refresh(rol)
    return rol

def delete_rol(db: Session, rol_id: int):
    rol = get_rol(db, rol_id)
    db.delete(rol)
    db.commit()
    return {"message": "Rol eliminado correctamente"}
