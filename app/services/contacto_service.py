from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.contacto import Contacto
from app.models.usuario import Usuario
from app.schemas.contacto import ContactoCreate

def crear_contacto(db: Session, usuario_id_1: int, data: ContactoCreate):
    if usuario_id_1 == data.usuario_id_2:
        raise HTTPException(status_code=400, detail="No puedes agregarte a ti mismo")

    # Verificar que el otro usuario exista
    if not db.query(Usuario).filter_by(id_usuario=data.usuario_id_2).first():
        raise HTTPException(status_code=404, detail="El usuario destino no existe")

    # Evitar duplicados (en cualquier orden)
    existente = db.query(Contacto).filter(
        ((Contacto.usuario_id_1 == usuario_id_1) & (Contacto.usuario_id_2 == data.usuario_id_2)) |
        ((Contacto.usuario_id_1 == data.usuario_id_2) & (Contacto.usuario_id_2 == usuario_id_1))
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Contacto ya registrado")

    contacto = Contacto(
        usuario_id_1=usuario_id_1,
        usuario_id_2=data.usuario_id_2
    )
    db.add(contacto)
    db.commit()
    db.refresh(contacto)
    return contacto

def listar_contactos(db: Session, user_id: int):
    return db.query(Contacto).filter(
        (Contacto.usuario_id_1 == user_id) | (Contacto.usuario_id_2 == user_id)
    ).all()

def eliminar_contacto(db: Session, contacto_id: int, user_id: int):
    contacto = db.query(Contacto).filter_by(id_contacto=contacto_id).first()
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")

    # Solo uno de los usuarios puede eliminarlo
    if contacto.usuario_id_1 != user_id and contacto.usuario_id_2 != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar este contacto")

    db.delete(contacto)
    db.commit()
    return {"message": "Contacto eliminado"}
