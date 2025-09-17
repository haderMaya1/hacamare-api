from sqlalchemy.orm import Session
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate, MensajeUpdate

def crear_mensaje(db: Session, mensaje: MensajeCreate):
    nuevo = Mensaje(**mensaje.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_mensajes(db: Session):
    return db.query(Mensaje).all()

def obtener_mensaje_por_id(db: Session, id_mensaje: int):
    return db.query(Mensaje).filter(Mensaje.id_mensaje == id_mensaje).first()

def obtener_mensajes_por_sesion(db: Session, id_sesion: int):
    return db.query(Mensaje).filter(Mensaje.id_sesion == id_sesion).all()

def actualizar_mensaje(db: Session, id_mensaje: int, mensaje: MensajeUpdate):
    db_mensaje = obtener_mensaje_por_id(db, id_mensaje)
    if not db_mensaje:
        return None
    for key, value in mensaje.dict(exclude_unset=True).items():
        setattr(db_mensaje, key, value)
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje

def eliminar_mensaje(db: Session, id_mensaje: int):
    db_mensaje = obtener_mensaje_por_id(db, id_mensaje)
    if not db_mensaje:
        return None
    db.delete(db_mensaje)
    db.commit()
    return db_mensaje
