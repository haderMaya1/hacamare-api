from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario_interes import UsuarioInteresCreate, UsuarioInteresResponse
from app.services.usuario_interes_service import (
    crear_usuario_interes,
    obtener_usuario_intereses,
    obtener_usuario_interes,
    eliminar_usuario_interes,
)

router = APIRouter(prefix="/usuario-interes", tags=["UsuarioInteres"])

@router.post("/", response_model=dict)
def create_usuario_interes(rel: UsuarioInteresCreate, db: Session = Depends(get_db)):
    nuevo = crear_usuario_interes(db, rel)
    return {
        "message": "Relación usuario-interés creada exitosamente",
        "data": UsuarioInteresResponse.model_validate(nuevo, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_usuario_intereses(db: Session = Depends(get_db)):
    relaciones = obtener_usuario_intereses(db)
    return {
        "message": "Lista de relaciones usuario-interés",
        "data": [UsuarioInteresResponse.model_validate(r, from_attributes=True) for r in relaciones]
    }

@router.get("/{id_usuario}/{id_interes}", response_model=dict)
def get_usuario_interes(id_usuario: int, id_interes: int, db: Session = Depends(get_db)):
    rel = obtener_usuario_interes(db, id_usuario, id_interes)
    if not rel:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {
        "message": "Relación encontrada",
        "data": UsuarioInteresResponse.model_validate(rel, from_attributes=True)
    }

@router.delete("/{id_usuario}/{id_interes}", response_model=dict)
def delete_usuario_interes(id_usuario: int, id_interes: int, db: Session = Depends(get_db)):
    eliminado = eliminar_usuario_interes(db, id_usuario, id_interes)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"message": "Relación usuario-interés eliminada correctamente"}
