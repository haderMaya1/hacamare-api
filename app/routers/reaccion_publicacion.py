from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.reaccion_publicacion import (
    ReaccionPublicacionCreate,
    ReaccionPublicacionUpdate,
    ReaccionPublicacionResponse
)
from app.services.reaccion_publicacion_service import (
    crear_reaccion,
    obtener_reacciones,
    obtener_reaccion_por_id,
    obtener_reacciones_por_publicacion,
    actualizar_reaccion,
    eliminar_reaccion
)

router = APIRouter(prefix="/reacciones", tags=["Reacciones Publicación"])

@router.post("/", response_model=dict)
def create_reaccion(reaccion: ReaccionPublicacionCreate, db: Session = Depends(get_db)):
    nueva = crear_reaccion(db, reaccion)
    return {
        "message": "Reacción creada exitosamente",
        "data": ReaccionPublicacionResponse.model_validate(nueva, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_reacciones(db: Session = Depends(get_db)):
    reacciones = obtener_reacciones(db)
    return {
        "message": "Lista de reacciones",
        "data": [ReaccionPublicacionResponse.model_validate(r, from_attributes=True) for r in reacciones]
    }

@router.get("/{id_reaccion}", response_model=dict)
def get_reaccion(id_reaccion: int, db: Session = Depends(get_db)):
    reaccion = obtener_reaccion_por_id(db, id_reaccion)
    if not reaccion:
        raise HTTPException(status_code=404, detail="Reacción no encontrada")
    return {
        "message": "Reacción encontrada",
        "data": ReaccionPublicacionResponse.model_validate(reaccion, from_attributes=True)
    }

@router.get("/publicacion/{id_publicacion}", response_model=dict)
def get_reacciones_publicacion(id_publicacion: int, db: Session = Depends(get_db)):
    reacciones = obtener_reacciones_por_publicacion(db, id_publicacion)
    return {
        "message": "Lista de reacciones de la publicación",
        "data": [ReaccionPublicacionResponse.model_validate(r, from_attributes=True) for r in reacciones]
    }

@router.put("/{id_reaccion}", response_model=dict)
def update_reaccion(id_reaccion: int, reaccion: ReaccionPublicacionUpdate, db: Session = Depends(get_db)):
    actualizada = actualizar_reaccion(db, id_reaccion, reaccion)
    if not actualizada:
        raise HTTPException(status_code=404, detail="Reacción no encontrada")
    return {
        "message": "Reacción actualizada correctamente",
        "data": ReaccionPublicacionResponse.model_validate(actualizada, from_attributes=True)
    }

@router.delete("/{id_reaccion}", response_model=dict)
def delete_reaccion(id_reaccion: int, db: Session = Depends(get_db)):
    eliminada = eliminar_reaccion(db, id_reaccion)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Reacción no encontrada")
    return {"message": "Reacción eliminada correctamente"}
