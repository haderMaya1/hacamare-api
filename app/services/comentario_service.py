from sqlalchemy.orm import Session
from app.models.comentario import Comentario
from app.schemas.comentario import ComentarioCreate, ComentarioUpdate

def crear_comentario(db: Session, comentario: ComentarioCreate):
    nuevo = Comentario(**comentario.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_comentarios(db: Session):
    return db.query(Comentario).all()

def obtener_comentario_por_id(db: Session, id_comentario: int):
    return db.query(Comentario).filter(Comentario.id_comentario == id_comentario).first()

def obtener_comentarios_por_publicacion(db: Session, id_publicacion: int):
    return db.query(Comentario).filter(Comentario.id_publicacion == id_publicacion).all()

def obtener_respuestas(db: Session, id_comentario: int):
    return db.query(Comentario).filter(Comentario.id_comentario_padre == id_comentario).all()

def actualizar_comentario(db: Session, id_comentario: int, comentario: ComentarioUpdate):
    db_comentario = obtener_comentario_por_id(db, id_comentario)
    if not db_comentario:
        return None
    for field, value in comentario.dict(exclude_unset=True).items():
        setattr(db_comentario, field, value)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def eliminar_comentario(db: Session, id_comentario: int):
    db_comentario = obtener_comentario_por_id(db, id_comentario)
    if not db_comentario:
        return None
    db.delete(db_comentario)
    db.commit()
    return db_comentario
