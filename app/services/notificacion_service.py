from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate

def crear_notificacion(db: Session, notificacion: NotificacionCreate):
    nueva = Notificacion(**notificacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_notificaciones(db: Session):
    return db.query(Notificacion).all()

def obtener_notificacion(db: Session, notificacion_id: int):
    noti = db.query(Notificacion).filter(Notificacion.id_notificacion == notificacion_id).first()
    if not noti:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return noti

def actualizar_notificacion(db: Session, notificacion_id: int, cambios: NotificacionUpdate):
    noti = db.query(Notificacion).filter(Notificacion.id_notificacion == notificacion_id).first()
    if not noti:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    for key, value in cambios.dict(exclude_unset=True).items():
        setattr(noti, key, value)

    db.commit()
    db.refresh(noti)
    return noti

def eliminar_notificacion(db: Session, notificacion_id: int):
    noti = db.query(Notificacion).filter(Notificacion.id_notificacion == notificacion_id).first()
    if not noti:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    db.delete(noti)
    db.commit()
    return True
