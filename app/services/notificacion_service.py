from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate

def crear_notificacion(db: Session, data: NotificacionCreate):
    notif = Notificacion(**data.dict())
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def listar_notificaciones(db: Session):
    return db.query(Notificacion).all()

def obtener_notificacion(db: Session, notif_id: int):
    notif = db.query(Notificacion).filter_by(id_notificacion=notif_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notif

def actualizar_notificacion(db: Session, notif_id: int, data: NotificacionUpdate):
    notif = obtener_notificacion(db, notif_id)
    if data.tipo is not None:
        notif.tipo = data.tipo
    if data.contenido is not None:
        notif.contenido = data.contenido
    if data.estado is not None:
        notif.estado = data.estado
    db.commit()
    db.refresh(notif)
    return notif

def eliminar_notificacion(db: Session, notif_id: int):
    notif = obtener_notificacion(db, notif_id)
    db.delete(notif)
    db.commit()
    return {"message": "Notificación eliminada correctamente"}
