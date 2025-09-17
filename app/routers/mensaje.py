from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.mensaje import MensajeCreate, MensajeUpdate, MensajeResponse
from app.services.mensaje_service import (
    crear_mensaje,
    obtener_mensajes,
    obtener_mensaje_por_id,
    obtener_mensajes_por_sesion,
    actualizar_mensaje,
    eliminar_mensaje
)

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])

@router.post("/", response_model=dict)
def create_mensaje(mensaje: MensajeCreate, db: Session = Depends(get_db)):
    nuevo = crear_mensaje(db, mensaje)
    return {
        "message": "Mensaje enviado exitosamente",
        "data": MensajeResponse.model_validate(nuevo, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_mensajes(db: Session = Depends(get_db)):
    mensajes = obtener_mensajes(db)
    return {
        "message": "Lista de mensajes",
        "data": [MensajeResponse.model_validate(m, from_attributes=True) for m in mensajes]
    }

@router.get("/{id_mensaje}", response_model=dict)
def get_mensaje(id_mensaje: int, db: Session = Depends(get_db)):
    mensaje = obtener_mensaje_por_id(db, id_mensaje)
    if not mensaje:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return {
        "message": "Mensaje encontrado",
        "data": MensajeResponse.model_validate(mensaje, from_attributes=True)
    }

@router.get("/sesion/{id_sesion}", response_model=dict)
def get_mensajes_sesion(id_sesion: int, db: Session = Depends(get_db)):
    mensajes = obtener_mensajes_por_sesion(db, id_sesion)
    return {
        "message": "Lista de mensajes de la sesión",
        "data": [MensajeResponse.model_validate(m, from_attributes=True) for m in mensajes]
    }

@router.put("/{id_mensaje}", response_model=dict)
def update_mensaje(id_mensaje: int, mensaje: MensajeUpdate, db: Session = Depends(get_db)):
    actualizado = actualizar_mensaje(db, id_mensaje, mensaje)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return {
        "message": "Mensaje actualizado correctamente",
        "data": MensajeResponse.model_validate(actualizado, from_attributes=True)
    }

@router.delete("/{id_mensaje}", response_model=dict)
def delete_mensaje(id_mensaje: int, db: Session = Depends(get_db)):
    eliminado = eliminar_mensaje(db, id_mensaje)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return {"message": "Mensaje eliminado correctamente"}
