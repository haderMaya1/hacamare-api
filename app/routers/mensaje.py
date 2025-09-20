from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.mensaje import MensajeCreate, MensajeUpdate, MensajeResponse
from app.services import mensaje_service
from app.utils.security import get_current_user
from typing import List

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])

@router.post("/", response_model=MensajeResponse, status_code=status.HTTP_201_CREATED)
def crear_mensaje(mensaje: MensajeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return mensaje_service.crear_mensaje(db, mensaje, current_user)

@router.get("/{id_mensaje}", response_model=MensajeResponse, status_code=status.HTTP_200_OK)
def obtener_mensaje(id_mensaje: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return mensaje_service.obtener_mensaje(db, id_mensaje, current_user)

@router.get("/sesion/{id_sesion}", response_model=List[MensajeResponse], status_code=status.HTTP_200_OK)
def listar_mensajes(id_sesion: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return mensaje_service.listar_mensajes(db, id_sesion, current_user)

@router.put("/{id_mensaje}", response_model=MensajeResponse, status_code=status.HTTP_200_OK)
def actualizar_mensaje(id_mensaje: int, mensaje_update: MensajeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return mensaje_service.actualizar_mensaje(db, id_mensaje, mensaje_update, current_user)

@router.delete("/{id_mensaje}", status_code=status.HTTP_200_OK)
def eliminar_mensaje(id_mensaje: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return mensaje_service.eliminar_mensaje(db, id_mensaje, current_user)
