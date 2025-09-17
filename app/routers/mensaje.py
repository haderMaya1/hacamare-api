from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate, MensajeResponse

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])

@router.post("/", response_model=MensajeResponse)
def create_mensaje(mensaje: MensajeCreate, db: Session = Depends(get_db)):
    nuevo_mensaje = Mensaje(**mensaje.dict())
    db.add(nuevo_mensaje)
    db.commit()
    db.refresh(nuevo_mensaje)
    return nuevo_mensaje

@router.get("/", response_model=List[MensajeResponse])
def get_mensajes(db: Session = Depends(get_db)):
    return db.query(Mensaje).all()

@router.get("/sesion/{id_sesion}", response_model=List[MensajeResponse])
def get_mensajes_sesion(id_sesion: int, db: Session = Depends(get_db)):
    return db.query(Mensaje).filter(Mensaje.id_sesion == id_sesion).all()

@router.get("/{id_mensaje}", response_model=MensajeResponse)
def get_mensaje(id_mensaje: int, db: Session = Depends(get_db)):
    mensaje = db.query(Mensaje).filter(Mensaje.id_mensaje == id_mensaje).first()
    if not mensaje:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return mensaje

@router.delete("/{id_mensaje}")
def delete_mensaje(id_mensaje: int, db: Session = Depends(get_db)):
    mensaje = db.query(Mensaje).filter(Mensaje.id_mensaje == id_mensaje).first()
    if not mensaje:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    db.delete(mensaje)
    db.commit()
    return {"message": "Mensaje eliminado correctamente"}
