from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate, NotificacionResponse
from app.services import notificacion_service as service
from app.utils.security import get_current_user

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

@router.post("/", response_model=NotificacionResponse, status_code=status.HTTP_201_CREATED)
def crear_notificacion(data: NotificacionCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.crear_notificacion(db, data)

@router.get("/", response_model=List[NotificacionResponse])
def listar_notificaciones(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Podría restringirse por usuario si se requiere
    return service.listar_notificaciones(db)

@router.get("/{notif_id}", response_model=NotificacionResponse)
def obtener_notificacion(notif_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.obtener_notificacion(db, notif_id)

@router.put("/{notif_id}", response_model=NotificacionResponse)
def actualizar_notificacion(notif_id: int, data: NotificacionUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.actualizar_notificacion(db, notif_id, data)

@router.delete("/{notif_id}")
def eliminar_notificacion(notif_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.eliminar_notificacion(db, notif_id)
