from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.sesion_chat import SesionChat
from app.schemas.sesion_chat import SesionChatCreate, SesionChatUpdate

def create_sesion_chat(db: Session, sesion: SesionChatCreate, anfitrion_id: int) -> SesionChat:
    nueva = SesionChat(
        nombre_tema=sesion.nombre_tema,
        tipo=sesion.tipo,
        estado=sesion.estado,
        fecha_creacion=datetime.utcnow(),
        anfitrion_id=anfitrion_id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def get_sesiones_chat(db: Session):
    return db.query(SesionChat).all()

def get_sesion_chat(db: Session, sesion_id: int) -> SesionChat:
    sesion = db.query(SesionChat).filter(SesionChat.id_sesion == sesion_id).first()
    if not sesion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Sesión de chat no encontrada")
    return sesion

def update_sesion_chat(db: Session, sesion_id: int, data: SesionChatUpdate) -> SesionChat:
    sesion = get_sesion_chat(db, sesion_id)
    if data.nombre_tema is not None:
        sesion.nombre_tema = data.nombre_tema
    if data.tipo is not None:
        sesion.tipo = data.tipo
    if data.estado is not None:
        sesion.estado = data.estado
    db.commit()
    db.refresh(sesion)
    return sesion

def delete_sesion_chat(db: Session, sesion_id: int):
    sesion = get_sesion_chat(db, sesion_id)
    db.delete(sesion)
    db.commit()
    return {"message": "Sesión de chat eliminada correctamente"}
