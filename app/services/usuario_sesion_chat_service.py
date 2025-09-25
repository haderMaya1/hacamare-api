# app/services/usuario_sesion_chat_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from app.models.usuario_sesion_chat import UsuarioSesionChat
from app.models.usuario import Usuario
from app.models.sesion_chat import SesionChat


def join_session(db: Session, id_usuario: int, id_sesion: int):
    # Verificar existencia de usuario y sesión
    if not db.query(Usuario).filter_by(id_usuario=id_usuario).first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not db.query(SesionChat).filter_by(id_sesion=id_sesion).first():
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    # Evitar duplicados
    existing = db.execute(
        select(UsuarioSesionChat).where(
            (UsuarioSesionChat.c.id_usuario == id_usuario) &
            (UsuarioSesionChat.c.id_sesion == id_sesion)
        )
    ).first()
    if existing:
        return {"message": "El usuario ya está en la sesión"}

    db.execute(
        insert(UsuarioSesionChat).values(
            id_usuario=id_usuario,
            id_sesion=id_sesion
        )
    )
    db.commit()
    return {"id_usuario": id_usuario, "id_sesion": id_sesion}


def leave_session(db: Session, id_usuario: int, id_sesion: int):
    # Borrar con delete() + where + columnas .c
    result = db.execute(
        delete(UsuarioSesionChat).where(
            (UsuarioSesionChat.c.id_usuario == id_usuario) &
            (UsuarioSesionChat.c.id_sesion == id_sesion)
        )
    )
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="El usuario no está en esta sesión")
    db.commit()
    return {"message": "Usuario removido de la sesión"}


def list_participants(db: Session, id_sesion: int):
    # Seleccionar participantes usando select() y columnas .c
    result = db.execute(
        select(UsuarioSesionChat).where(
            UsuarioSesionChat.c.id_sesion == id_sesion
        )
    ).mappings().all()
    # mappings() => [{'id_usuario': ..., 'id_sesion': ...}, ...]
    return [dict(row) for row in result]
