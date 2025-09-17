from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario_sesion_chat import UsuarioSesionChatCreate, UsuarioSesionChatResponse
from app.services.usuario_sesion_chat_service import (
    crear_usuario_sesion_chat,
    obtener_relaciones_usuario_sesion,
    obtener_relacion,
    eliminar_usuario_sesion_chat
)

router = APIRouter(prefix="/usuario-sesion-chat", tags=["Usuario - Sesión Chat"])

@router.post("/", response_model=dict)
def create_usuario_sesion_chat(relacion: UsuarioSesionChatCreate, db: Session = Depends(get_db)):
    nueva = crear_usuario_sesion_chat(db, relacion)
    if not nueva:
        raise HTTPException(status_code=400, detail="Relación ya existe")
    return {
        "message": "Relación usuario-sesión creada exitosamente",
        "data": UsuarioSesionChatResponse.model_validate(nueva, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_relaciones_usuario_sesion(db: Session = Depends(get_db)):
    relaciones = obtener_relaciones_usuario_sesion(db)
    return {
        "message": "Lista de relaciones usuario-sesión",
        "data": [UsuarioSesionChatResponse.model_validate(r, from_attributes=True) for r in relaciones]
    }

@router.get("/{id_usuario}/{id_sesion}", response_model=dict)
def get_relacion_usuario_sesion(id_usuario: int, id_sesion: int, db: Session = Depends(get_db)):
    relacion = obtener_relacion(db, id_usuario, id_sesion)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {
        "message": "Relación encontrada",
        "data": UsuarioSesionChatResponse.model_validate(relacion, from_attributes=True)
    }

@router.delete("/{id_usuario}/{id_sesion}", response_model=dict)
def delete_usuario_sesion_chat(id_usuario: int, id_sesion: int, db: Session = Depends(get_db)):
    eliminado = eliminar_usuario_sesion_chat(db, id_usuario, id_sesion)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"message": "Relación usuario-sesión eliminada correctamente"}
