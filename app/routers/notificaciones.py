from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate, NotificacionResponse
from app.services.notificacion_service import (
    crear_notificacion, obtener_notificaciones, obtener_notificacion,
    actualizar_notificacion, eliminar_notificacion
)

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

@router.post("/", response_model=NotificacionResponse)
def create_notificacion(request: NotificacionCreate, db: Session = Depends(get_db)):
    return crear_notificacion(db, request)

@router.get("/", response_model=List[NotificacionResponse])
def list_notificaciones(db: Session = Depends(get_db)):
    return obtener_notificaciones(db)

@router.get("/{notificacion_id}", response_model=NotificacionResponse)
def get_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    return obtener_notificacion(db, notificacion_id)

@router.put("/{notificacion_id}", response_model=NotificacionResponse)
def update_notificacion(notificacion_id: int, request: NotificacionUpdate, db: Session = Depends(get_db)):
    return actualizar_notificacion(db, notificacion_id, request)

@router.delete("/{notificacion_id}")
def delete_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    eliminado = eliminar_notificacion(db, notificacion_id)
    return {"message": "Notificación eliminada correctamente"} if eliminado else {"message": "No se eliminó"}
