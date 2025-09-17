from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.sesion_chat import SesionChatCreate, SesionChatUpdate, SesionChatResponse
from app.services.sesion_chat_service import (
    crear_sesion_chat,
    obtener_sesiones_chat,
    obtener_sesion_chat_por_id,
    actualizar_sesion_chat,
    eliminar_sesion_chat
)

router = APIRouter(prefix="/sesiones_chat", tags=["Sesiones de Chat"])

@router.post("/", response_model=dict)
def create_sesion_chat(sesion: SesionChatCreate, db: Session = Depends(get_db)):
    nueva = crear_sesion_chat(db, sesion)
    return {
        "message": "Sesión de chat creada exitosamente",
        "data": SesionChatResponse.model_validate(nueva, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_sesiones_chat(db: Session = Depends(get_db)):
    sesiones = obtener_sesiones_chat(db)
    return {
        "message": "Lista de sesiones de chat",
        "data": [SesionChatResponse.model_validate(s, from_attributes=True) for s in sesiones]
    }

@router.get("/{id_sesion}", response_model=dict)
def get_sesion_chat(id_sesion: int, db: Session = Depends(get_db)):
    s = obtener_sesion_chat_por_id(db, id_sesion)
    if not s:
        raise HTTPException(status_code=404, detail="Sesión de chat no encontrada")
    return {
        "message": "Sesión de chat encontrada",
        "data": SesionChatResponse.model_validate(s, from_attributes=True)
    }

@router.put("/{id_sesion}", response_model=dict)
def update_sesion_chat(id_sesion: int, sesion: SesionChatUpdate, db: Session = Depends(get_db)):
    s = actualizar_sesion_chat(db, id_sesion, sesion)
    if not s:
        raise HTTPException(status_code=404, detail="Sesión de chat no encontrada")
    return {
        "message": "Sesión de chat actualizada correctamente",
        "data": SesionChatResponse.model_validate(s, from_attributes=True)
    }

@router.delete("/{id_sesion}", response_model=dict)
def delete_sesion_chat(id_sesion: int, db: Session = Depends(get_db)):
    s = eliminar_sesion_chat(db, id_sesion)
    if not s:
        raise HTTPException(status_code=404, detail="Sesión de chat no encontrada")
    return {"message": "Sesión de chat eliminada correctamente"}
