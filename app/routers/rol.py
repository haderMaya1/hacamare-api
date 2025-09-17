from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolResponse, RolUpdate, RolOut

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)

@router.post("/", response_model=RolOut)
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = Rol(nombre=rol.nombre)
    db_rol.set_permisos(rol.permisos or {})
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return RolOut.from_orm(db_rol)

@router.get("/", response_model=List[RolOut])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Rol).all()
    return [RolOut.from_orm(r) for r in roles]

@router.get("/{rol_id}", response_model=RolOut)
def get_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return RolOut.from_orm(rol)

@router.put("/{rol_id}", response_model=RolOut)
def update_rol(rol_id: int, rol_update: RolUpdate, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    if rol_update.nombre is not None:
        rol.nombre = rol_update.nombre
    if rol_update.permisos is not None:
        rol.set_permisos(rol_update.permisos)

    db.commit()
    db.refresh(rol)
    return RolOut.from_orm(rol)

@router.delete("/{rol_id}")
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    db.delete(rol)
    db.commit()
    return {"detail": "Rol eliminado correctamente"}
