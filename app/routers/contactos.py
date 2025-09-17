from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.contacto import ContactoCreate, ContactoResponse
from app.services.contacto_service import (
    crear_contacto,
    obtener_contactos,
    obtener_contacto_por_id,
    obtener_contactos_usuario,
    eliminar_contacto
)

router = APIRouter(prefix="/contactos", tags=["Contactos"])

@router.post("/", response_model=dict)
def create_contacto(contacto: ContactoCreate, db: Session = Depends(get_db)):
    nuevo = crear_contacto(db, contacto)
    if not nuevo:
        raise HTTPException(status_code=400, detail="El contacto ya existe")
    return {
        "message": "Contacto creado exitosamente",
        "data": ContactoResponse.model_validate(nuevo, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_contactos(db: Session = Depends(get_db)):
    contactos = obtener_contactos(db)
    return {
        "message": "Lista de contactos",
        "data": [ContactoResponse.model_validate(c, from_attributes=True) for c in contactos]
    }

@router.get("/{id_contacto}", response_model=dict)
def get_contacto(id_contacto: int, db: Session = Depends(get_db)):
    contacto = obtener_contacto_por_id(db, id_contacto)
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return {
        "message": "Contacto encontrado",
        "data": ContactoResponse.model_validate(contacto, from_attributes=True)
    }

@router.get("/usuario/{id_usuario}", response_model=dict)
def get_contactos_usuario(id_usuario: int, db: Session = Depends(get_db)):
    contactos = obtener_contactos_usuario(db, id_usuario)
    return {
        "message": "Lista de contactos del usuario",
        "data": [ContactoResponse.model_validate(c, from_attributes=True) for c in contactos]
    }

@router.delete("/{id_contacto}", response_model=dict)
def delete_contacto(id_contacto: int, db: Session = Depends(get_db)):
    eliminado = eliminar_contacto(db, id_contacto)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return {"message": "Contacto eliminado correctamente"}
