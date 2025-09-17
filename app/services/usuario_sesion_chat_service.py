from sqlalchemy.orm import Session
from app.models.usuario_sesion_chat import UsuarioSesionChat
from app.schemas.usuario_sesion_chat import UsuarioSesionChatCreate

def crear_usuario_sesion_chat(db: Session, relacion: UsuarioSesionChatCreate):
    existente = db.query(UsuarioSesionChat).filter_by(
        id_usuario=relacion.id_usuario, id_sesion=relacion.id_sesion
    ).first()
    if existente:
        return None
    nueva = UsuarioSesionChat(**relacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_relaciones_usuario_sesion(db: Session):
    return db.query(UsuarioSesionChat).all()

def obtener_relacion(db: Session, id_usuario: int, id_sesion: int):
    return db.query(UsuarioSesionChat).filter_by(id_usuario=id_usuario, id_sesion=id_sesion).first()

def eliminar_usuario_sesion_chat(db: Session, id_usuario: int, id_sesion: int):
    relacion = obtener_relacion(db, id_usuario, id_sesion)
    if not relacion:
        return None
    db.delete(relacion)
    db.commit()
    return relacion
