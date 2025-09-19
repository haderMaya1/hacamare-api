from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.sesion_chat import SesionChat
from app.schemas.sesion_chat import SesionChatCreate, SesionChatUpdate

def create_sesion_chat(db: Session, sesion: SesionChatCreate, anfitrion_id: int):
    nueva_sesion = SesionChat(
        nombre_tema=sesion.nombre_tema,
        tipo=sesion.tipo,
        estado=sesion.estado,
        anfitrion_id=anfitrion_id
    )
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    return nueva_sesion

def get_sesion_chat(db: Session, sesion_id: int):
    sesion = db.query(SesionChat).filter(SesionChat.id_sesion == sesion_id).first()
    if not sesion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sesión no encontrada")
    return sesion

def get_sesiones_chat(db: Session):
    return db.query(SesionChat).all()

def delete_sesion_chat(db: Session, sesion_id: int, user_id: int):
    sesion = get_sesion_chat(db, sesion_id)
    if sesion.anfitrion_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para eliminar esta sesión")
    db.delete(sesion)
    db.commit()
    return {"message": "Sesión eliminada"}

def update_sesion_chat(db: Session, sesion_id: int, sesion_data: SesionChatCreate, user_id: int):
    sesion = get_sesion_chat(db, sesion_id)
    if sesion.anfitrion_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para modificar esta sesión")
    sesion.nombre_tema = sesion_data.nombre_tema
    sesion.tipo = sesion_data.tipo
    sesion.estado = sesion_data.estado
    db.commit()
    db.refresh(sesion)
    return sesion
