from sqlalchemy.orm import Session
from app.models.reaccion_publicacion import ReaccionPublicacion
from app.schemas.reaccion_publicacion import ReaccionPublicacionCreate, ReaccionPublicacionUpdate

def crear_reaccion(db: Session, reaccion: ReaccionPublicacionCreate):
    nueva = ReaccionPublicacion(**reaccion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_reacciones(db: Session):
    return db.query(ReaccionPublicacion).all()

def obtener_reaccion_por_id(db: Session, id_reaccion: int):
    return db.query(ReaccionPublicacion).filter(ReaccionPublicacion.id_reaccion == id_reaccion).first()

def obtener_reacciones_por_publicacion(db: Session, id_publicacion: int):
    return db.query(ReaccionPublicacion).filter(ReaccionPublicacion.id_publicacion == id_publicacion).all()

def actualizar_reaccion(db: Session, id_reaccion: int, reaccion: ReaccionPublicacionUpdate):
    db_reaccion = obtener_reaccion_por_id(db, id_reaccion)
    if not db_reaccion:
        return None
    db_reaccion.tipo = reaccion.tipo
    db.commit()
    db.refresh(db_reaccion)
    return db_reaccion

def eliminar_reaccion(db: Session, id_reaccion: int):
    db_reaccion = obtener_reaccion_por_id(db, id_reaccion)
    if not db_reaccion:
        return None
    db.delete(db_reaccion)
    db.commit()
    return db_reaccion
