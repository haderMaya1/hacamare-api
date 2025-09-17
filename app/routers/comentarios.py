from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.comentario import (
    ComentarioCreate,
    ComentarioUpdate,
    ComentarioResponse
)
from app.services.comentario_service import (
    crear_comentario,
    obtener_comentarios,
    obtener_comentario_por_id,
    obtener_comentarios_por_publicacion,
    obtener_respuestas,
    actualizar_comentario,
    eliminar_comentario
)

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.post("/", response_model=dict)
def create_comentario(comentario: ComentarioCreate, db: Session = Depends(get_db)):
    nuevo = crear_comentario(db, comentario)
    return {
        "message": "Comentario creado exitosamente",
        "data": ComentarioResponse.model_validate(nuevo, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_comentarios(db: Session = Depends(get_db)):
    comentarios = obtener_comentarios(db)
    return {
        "message": "Lista de comentarios",
        "data": [ComentarioResponse.model_validate(c, from_attributes=True) for c in comentarios]
    }

@router.get("/{id_comentario}", response_model=dict)
def get_comentario(id_comentario: int, db: Session = Depends(get_db)):
    comentario = obtener_comentario_por_id(db, id_comentario)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {
        "message": "Comentario encontrado",
        "data": ComentarioResponse.model_validate(comentario, from_attributes=True)
    }

@router.get("/publicacion/{id_publicacion}", response_model=dict)
def get_comentarios_publicacion(id_publicacion: int, db: Session = Depends(get_db)):
    comentarios = obtener_comentarios_por_publicacion(db, id_publicacion)
    return {
        "message": "Lista de comentarios de la publicación",
        "data": [ComentarioResponse.model_validate(c, from_attributes=True) for c in comentarios]
    }

@router.get("/{id_comentario}/respuestas", response_model=dict)
def get_respuestas_comentario(id_comentario: int, db: Session = Depends(get_db)):
    respuestas = obtener_respuestas(db, id_comentario)
    return {
        "message": "Lista de respuestas del comentario",
        "data": [ComentarioResponse.model_validate(r, from_attributes=True) for r in respuestas]
    }

@router.put("/{id_comentario}", response_model=dict)
def update_comentario(id_comentario: int, comentario: ComentarioUpdate, db: Session = Depends(get_db)):
    actualizado = actualizar_comentario(db, id_comentario, comentario)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {
        "message": "Comentario actualizado correctamente",
        "data": ComentarioResponse.model_validate(actualizado, from_attributes=True)
    }

@router.delete("/{id_comentario}", response_model=dict)
def delete_comentario(id_comentario: int, db: Session = Depends(get_db)):
    eliminado = eliminar_comentario(db, id_comentario)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {"message": "Comentario eliminado correctamente"}
