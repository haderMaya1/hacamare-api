from sqlalchemy.orm import Session
from app.models.sesion_chat import SesionChat
from app.schemas.sesion_chat import SesionChatCreate, SesionChatUpdate

def crear_sesion_chat(db: Session, sesion: SesionChatCreate):
    nueva = SesionChat(**sesion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_sesiones_chat(db: Session):
    return db.query(SesionChat).all()

def obtener_sesion_chat_por_id(db: Session, id_sesion: int):
    return db.query(SesionChat).filter(SesionChat.id_sesion == id_sesion).first()

def actualizar_sesion_chat(db: Session, id_sesion: int, sesion: SesionChatUpdate):
    s = obtener_sesion_chat_por_id(db, id_sesion)
    if not s:
        return None
    for key, value in sesion.dict(exclude_unset=True).items():
        setattr(s, key, value)
    db.commit()
    db.refresh(s)
    return s

def eliminar_sesion_chat(db: Session, id_sesion: int):
    s = obtener_sesion_chat_por_id(db, id_sesion)
    if not s:
        return None
    db.delete(s)
    db.commit()
    return s
