from sqlalchemy.orm import Session
from app.models.usuario_sesion_chat import UsuarioSesionChat
from app.schemas.usuario_sesion_chat import UsuarioSesionChatCreate

def add_usuario_a_sesion(db: Session, usuario_sesion: UsuarioSesionChatCreate):
    stmt = UsuarioSesionChat.insert().values(
        id_usuario=usuario_sesion.id_usuario,
        id_sesion=usuario_sesion.id_sesion
    )
    db.execute(stmt)
    db.commit()
    return usuario_sesion

def get_relaciones_usuario_sesion(db: Session):
    return db.query(UsuarioSesionChat).all()

def get_relacion(db: Session, id_usuario: int, id_sesion: int):
    return db.query(UsuarioSesionChat).filter_by(id_usuario=id_usuario, id_sesion=id_sesion).first()

def remove_usuario_de_sesion(db: Session, id_usuario: int, id_sesion: int):
    stmt = UsuarioSesionChat.delete().where(
        (UsuarioSesionChat.c.id_usuario == id_usuario) &
        (UsuarioSesionChat.c.id_sesion == id_sesion)
    )
    db.execute(stmt)
    db.commit()
    return {"message": "Usuario eliminado de la sesión"}