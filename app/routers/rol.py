from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolResponse, RolUpdate
from typing import List

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)

@router.post("/", response_model=RolResponse)
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.get("/", response_model=List[RolResponse])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

@router.get("/{rol_id}", response_model=RolResponse)
def get_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.put("/{rol_id}", response_model=RolResponse)
def update_rol(rol_id: int, rol_update: RolUpdate, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    for key, value in rol_update.dict(exclude_unset=True).items():
        setattr(rol, key, value)

    db.commit()
    db.refresh(rol)
    return rol

@router.delete("/{rol_id}")
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    db.delete(rol)
    db.commit()
    return {"detail": "Rol eliminado correctamente"}
