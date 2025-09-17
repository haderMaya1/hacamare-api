from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.contacto import Contacto
from app.schemas.contacto import ContactoCreate

def crear_contacto(db: Session, contacto: ContactoCreate):
    # Evitar duplicados (amistad en cualquier dirección)
    existente = db.query(Contacto).filter(
        or_(
            (Contacto.usuario_id_1 == contacto.usuario_id_1) & (Contacto.usuario_id_2 == contacto.usuario_id_2),
            (Contacto.usuario_id_1 == contacto.usuario_id_2) & (Contacto.usuario_id_2 == contacto.usuario_id_1)
        )
    ).first()

    if existente:
        return None

    nuevo = Contacto(**contacto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_contactos(db: Session):
    return db.query(Contacto).all()

def obtener_contacto_por_id(db: Session, id_contacto: int):
    return db.query(Contacto).filter(Contacto.id_contacto == id_contacto).first()

def obtener_contactos_usuario(db: Session, id_usuario: int):
    return db.query(Contacto).filter(
        or_(Contacto.usuario_id_1 == id_usuario, Contacto.usuario_id_2 == id_usuario)
    ).all()

def eliminar_contacto(db: Session, id_contacto: int):
    contacto = obtener_contacto_por_id(db, id_contacto)
    if not contacto:
        return None
    db.delete(contacto)
    db.commit()
    return contacto
