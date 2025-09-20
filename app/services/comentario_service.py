from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.comentario import Comentario
from app.schemas.comentario import ComentarioCreate, ComentarioUpdate
from app.models.usuario import Usuario
from app.models.publicacion import Publicacion

def crear_comentario(db: Session, data: ComentarioCreate, id_usuario: int):
    # Validar existencia de publicación
    publicacion = db.query(Publicacion).filter_by(id_publicacion=data.id_publicacion).first()
    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    # Validar comentario padre (si existe)
    if data.id_comentario_padre:
        padre = db.query(Comentario).filter_by(id_comentario=data.id_comentario_padre).first()
        if not padre:
            raise HTTPException(status_code=404, detail="Comentario padre no encontrado")

    comentario = Comentario(
        contenido=data.contenido,
        estado=data.estado,
        id_publicacion=data.id_publicacion,
        id_usuario=id_usuario,
        id_comentario_padre=data.id_comentario_padre,
        imagen=data.imagen
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario

def obtener_comentario(db: Session, comentario_id: int):
    comentario = db.query(Comentario).filter_by(id_comentario=comentario_id).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comentario

def listar_comentarios(db: Session, publicacion_id: int):
    return db.query(Comentario).filter_by(id_publicacion=publicacion_id).all()

def actualizar_comentario(db: Session, comentario_id: int, user_id: int, data: ComentarioUpdate):
    comentario = obtener_comentario(db, comentario_id)
    if comentario.id_usuario != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar este comentario")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(comentario, field, value)
    db.commit()
    db.refresh(comentario)
    return comentario

def eliminar_comentario(db: Session, comentario_id: int, user_id: int):
    comentario = obtener_comentario(db, comentario_id)
    if comentario.id_usuario != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar este comentario")
    db.delete(comentario)
    db.commit()
    return {"message": "Comentario eliminado"}
