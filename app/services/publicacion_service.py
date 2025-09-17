from sqlalchemy.orm import Session
from app.models.publicacion import Publicacion
from app.schemas.publicacion import PublicacionCreate, PublicacionUpdate

def crear_publicacion(db: Session, publicacion: PublicacionCreate):
    nueva = Publicacion(**publicacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_publicaciones(db: Session):
    return db.query(Publicacion).all()

def obtener_publicacion_por_id(db: Session, id_publicacion: int):
    return db.query(Publicacion).filter(Publicacion.id_publicacion == id_publicacion).first()

def actualizar_publicacion(db: Session, id_publicacion: int, publicacion: PublicacionUpdate):
    pub = obtener_publicacion_por_id(db, id_publicacion)
    if not pub:
        return None
    for key, value in publicacion.dict(exclude_unset=True).items():
        setattr(pub, key, value)
    db.commit()
    db.refresh(pub)
    return pub

def eliminar_publicacion(db: Session, id_publicacion: int):
    pub = obtener_publicacion_por_id(db, id_publicacion)
    if not pub:
        return None
    db.delete(pub)
    db.commit()
    return pub
