from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.services.rol_service import (
    crear_rol,
    obtener_roles,
    obtener_rol_por_id,
    actualizar_rol,
    eliminar_rol
)
import json

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=dict)
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    nuevo_rol = crear_rol(db, rol)
    return {
        "message": "Rol creado exitosamente",
        "data": RolResponse.model_validate(
            {**nuevo_rol.__dict__, "permisos": json.loads(nuevo_rol.permisos)},
            from_attributes=True
        )
    }

@router.get("/", response_model=dict)
def get_roles(db: Session = Depends(get_db)):
    roles = obtener_roles(db)
    return {
        "message": "Lista de roles",
        "data": [
            RolResponse.model_validate(
                {**r.__dict__, "permisos": json.loads(r.permisos)},
                from_attributes=True
            ) for r in roles
        ]
    }

@router.get("/{rol_id}", response_model=dict)
def get_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = obtener_rol_por_id(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {
        "message": "Rol encontrado",
        "data": RolResponse.model_validate(
            {**rol.__dict__, "permisos": json.loads(rol.permisos)},
            from_attributes=True
        )
    }

@router.put("/{rol_id}", response_model=dict)
def update_rol(rol_id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    actualizado = actualizar_rol(db, rol_id, rol)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {
        "message": "Rol actualizado correctamente",
        "data": RolResponse.model_validate(
            {**actualizado.__dict__, "permisos": json.loads(actualizado.permisos)},
            from_attributes=True
        )
    }

@router.delete("/{rol_id}", response_model=dict)
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    eliminado = eliminar_rol(db, rol_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"message": "Rol eliminado correctamente"}
