from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate, NotificacionResponse
from typing import List

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

@router.post("/", response_model=NotificacionResponse)
def create_notificacion(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    nueva_notificacion = Notificacion(**notificacion.dict())
    db.add(nueva_notificacion)
    db.commit()
    db.refresh(nueva_notificacion)
    return nueva_notificacion

@router.get("/", response_model=List[NotificacionResponse])
def get_notificaciones(db: Session = Depends(get_db)):
    return db.query(Notificacion).all()

@router.get("/{id_notificacion}", response_model=NotificacionResponse)
def get_notificacion(id_notificacion: int, db: Session = Depends(get_db)):
    notificacion = db.query(Notificacion).filter(Notificacion.id_notificacion == id_notificacion).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notificacion

@router.put("/{id_notificacion}", response_model=NotificacionResponse)
def update_notificacion(id_notificacion: int, update: NotificacionUpdate, db: Session = Depends(get_db)):
    notificacion = db.query(Notificacion).filter(Notificacion.id_notificacion == id_notificacion).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    notificacion.estado = update.estado
    db.commit()
    db.refresh(notificacion)
    return notificacion

@router.delete("/{id_notificacion}")
def delete_notificacion(id_notificacion: int, db: Session = Depends(get_db)):
    notificacion = db.query(Notificacion).filter(Notificacion.id_notificacion == id_notificacion).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    db.delete(notificacion)
    db.commit()
    return {"detail": "Notificación eliminada correctamente"}
