from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate, MensajeUpdate
from app.utils.security import get_current_user


def crear_mensaje(db: Session, mensaje: MensajeCreate, current_user):
    nuevo_mensaje = Mensaje(
        contenido=mensaje.contenido,
        imagen=mensaje.imagen,
        id_remitente=current_user.id_usuario,
        id_sesion=mensaje.id_sesion
    )
    db.add(nuevo_mensaje)
    db.commit()
    db.refresh(nuevo_mensaje)
    return nuevo_mensaje


def obtener_mensaje(db: Session, id_mensaje: int, current_user):
    mensaje = db.query(Mensaje).filter_by(id_mensaje=id_mensaje).first()
    if not mensaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")
    return mensaje


def listar_mensajes(db: Session, id_sesion: int, current_user):
    mensajes = db.query(Mensaje).filter_by(id_sesion=id_sesion).all()
    return mensajes


def actualizar_mensaje(db: Session, id_mensaje: int, mensaje_update: MensajeUpdate, current_user):
    mensaje = db.query(Mensaje).filter_by(id_mensaje=id_mensaje).first()
    if not mensaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")

    if mensaje.id_remitente != current_user.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes editar este mensaje")

    if mensaje_update.contenido is not None:
        mensaje.contenido = mensaje_update.contenido
    if mensaje_update.imagen is not None:
        mensaje.imagen = mensaje_update.imagen

    db.commit()
    db.refresh(mensaje)
    return mensaje


def eliminar_mensaje(db: Session, id_mensaje: int, current_user):
    mensaje = db.query(Mensaje).filter_by(id_mensaje=id_mensaje).first()
    if not mensaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")

    if mensaje.id_remitente != current_user.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes eliminar este mensaje")

    db.delete(mensaje)
    db.commit()
    return {"message": "Mensaje eliminado"}
