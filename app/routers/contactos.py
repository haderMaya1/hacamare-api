from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contacto import Contacto
from app.schemas.contacto import ContactoCreate, ContactoResponse
from typing import List

router = APIRouter(prefix="/contactos", tags=["Contactos"])

@router.post("/", response_model=ContactoResponse)
def create_contacto(contacto: ContactoCreate, db: Session = Depends(get_db)):
    if contacto.usuario_id_1 == contacto.usuario_id_2:
        raise HTTPException(status_code=400, detail="Un usuario no puede ser su propio contacto")

    # evitar duplicados (en ambos sentidos)
    existe = db.query(Contacto).filter(
        ((Contacto.usuario_id_1 == contacto.usuario_id_1) & (Contacto.usuario_id_2 == contacto.usuario_id_2)) |
        ((Contacto.usuario_id_1 == contacto.usuario_id_2) & (Contacto.usuario_id_2 == contacto.usuario_id_1))
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Contacto ya existe")

    nuevo_contacto = Contacto(**contacto.dict())
    db.add(nuevo_contacto)
    db.commit()
    db.refresh(nuevo_contacto)
    return nuevo_contacto

@router.get("/", response_model=List[ContactoResponse])
def get_contactos(db: Session = Depends(get_db)):
    return db.query(Contacto).all()

@router.get("/usuario/{id_usuario}", response_model=List[ContactoResponse])
def get_contactos_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return db.query(Contacto).filter(
        (Contacto.usuario_id_1 == id_usuario) | (Contacto.usuario_id_2 == id_usuario)
    ).all()

@router.delete("/{id_contacto}")
def delete_contacto(id_contacto: int, db: Session = Depends(get_db)):
    contacto = db.query(Contacto).filter(Contacto.id_contacto == id_contacto).first()
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    db.delete(contacto)
    db.commit()
    return {"detail": "Contacto eliminado correctamente"}
