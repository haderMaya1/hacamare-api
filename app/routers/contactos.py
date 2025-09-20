from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.contacto import ContactoCreate, ContactoResponse
from app.services import contacto_service as service
from app.utils.security import get_current_user

router = APIRouter(prefix="/contactos", tags=["Contactos"])

@router.post("/", response_model=ContactoResponse, status_code=status.HTTP_201_CREATED)
def crear_contacto(data: ContactoCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.crear_contacto(db, current_user.id_usuario, data)

@router.get("/", response_model=List[ContactoResponse])
def listar_contactos(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.listar_contactos(db, current_user.id_usuario)

@router.delete("/{contacto_id}")
def eliminar_contacto(contacto_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.eliminar_contacto(db, contacto_id, current_user.id_usuario)
