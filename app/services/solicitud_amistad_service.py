from sqlalchemy.orm import Session
from app.models.solicitud_amistad import SolicitudAmistad
from app.schemas.solicitud_amistad import SolicitudAmistadCreate, SolicitudAmistadUpdate

def crear_solicitud(db: Session, solicitud: SolicitudAmistadCreate):
    nueva_solicitud = SolicitudAmistad(**solicitud.dict())
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud

def obtener_solicitudes(db: Session):
    return db.query(SolicitudAmistad).all()

def obtener_solicitud(db: Session, id_solicitud: int):
    return db.query(SolicitudAmistad).filter(SolicitudAmistad.id_solicitud == id_solicitud).first()

def actualizar_solicitud(db: Session, id_solicitud: int, datos: SolicitudAmistadUpdate):
    solicitud = obtener_solicitud(db, id_solicitud)
    if not solicitud:
        return None
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(solicitud, key, value)
    db.commit()
    db.refresh(solicitud)
    return solicitud

def eliminar_solicitud(db: Session, id_solicitud: int):
    solicitud = obtener_solicitud(db, id_solicitud)
    if not solicitud:
        return None
    db.delete(solicitud)
    db.commit()
    return solicitud
