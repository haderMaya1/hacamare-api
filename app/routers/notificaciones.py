from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services import notificacion_service
from app.schemas.notificacion import (
    NotificacionCreate, NotificacionResponse, NotificacionUpdate
)
from app.utils.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])

@router.post("/", response_model=NotificacionResponse, status_code=201)
def crear_notificacion(
    notificacion: NotificacionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Podrías verificar permisos si solo admin puede crear
    return notificacion_service.create_notificacion(db, notificacion)

@router.get("/", response_model=List[NotificacionResponse])
def listar_notificaciones(
    usuario_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return notificacion_service.get_notificaciones(db, usuario_id)

@router.get("/{notificacion_id}", response_model=NotificacionResponse)
def obtener_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return notificacion_service.get_notificacion(db, notificacion_id)

@router.put("/{notificacion_id}", response_model=NotificacionResponse)
def actualizar_notificacion(
    notificacion_id: int,
    notif: NotificacionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return notificacion_service.update_notificacion(db, notificacion_id, notif)

@router.delete("/{notificacion_id}")
def eliminar_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return notificacion_service.delete_notificacion(db, notificacion_id)
