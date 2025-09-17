from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.publicacion import PublicacionCreate, PublicacionUpdate, PublicacionResponse
from app.services.publicacion_service import (
    crear_publicacion,
    obtener_publicaciones,
    obtener_publicacion_por_id,
    actualizar_publicacion,
    eliminar_publicacion
)

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"])

@router.post("/", response_model=dict)
def create_publicacion(publicacion: PublicacionCreate, db: Session = Depends(get_db)):
    nueva = crear_publicacion(db, publicacion)
    return {
        "message": "Publicación creada exitosamente",
        "data": PublicacionResponse.model_validate(nueva, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_publicaciones(db: Session = Depends(get_db)):
    publicaciones = obtener_publicaciones(db)
    return {
        "message": "Lista de publicaciones",
        "data": [PublicacionResponse.model_validate(p, from_attributes=True) for p in publicaciones]
    }

@router.get("/{id_publicacion}", response_model=dict)
def get_publicacion(id_publicacion: int, db: Session = Depends(get_db)):
    pub = obtener_publicacion_por_id(db, id_publicacion)
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return {
        "message": "Publicación encontrada",
        "data": PublicacionResponse.model_validate(pub, from_attributes=True)
    }

@router.put("/{id_publicacion}", response_model=dict)
def update_publicacion(id_publicacion: int, publicacion: PublicacionUpdate, db: Session = Depends(get_db)):
    pub = actualizar_publicacion(db, id_publicacion, publicacion)
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return {
        "message": "Publicación actualizada correctamente",
        "data": PublicacionResponse.model_validate(pub, from_attributes=True)
    }

@router.delete("/{id_publicacion}", response_model=dict)
def delete_publicacion(id_publicacion: int, db: Session = Depends(get_db)):
    pub = eliminar_publicacion(db, id_publicacion)
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return {"message": "Publicación eliminada correctamente"}
