from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate

def create_notificacion(db: Session, notificacion: NotificacionCreate) -> Notificacion:
    nueva = Notificacion(**notificacion.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def get_notificaciones(db: Session, usuario_id: int = None):
    query = db.query(Notificacion)
    if usuario_id:
        query = query.filter(Notificacion.id_usuario == usuario_id)
    return query.all()

def get_notificacion(db: Session, notificacion_id: int) -> Notificacion:
    notif = db.query(Notificacion).filter(Notificacion.id_notificacion == notificacion_id).first()
    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notificación {notificacion_id} no encontrada"
        )
    return notif

def update_notificacion(db: Session, notificacion_id: int, notif_data: NotificacionUpdate) -> Notificacion:
    notif = get_notificacion(db, notificacion_id)
    for key, value in notif_data.dict(exclude_unset=True).items():
        setattr(notif, key, value)
    db.commit()
    db.refresh(notif)
    return notif

def delete_notificacion(db: Session, notificacion_id: int):
    notif = get_notificacion(db, notificacion_id)
    db.delete(notif)
    db.commit()
    return {"message": f"Notificación {notificacion_id} eliminada correctamente"}
