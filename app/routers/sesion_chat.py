from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.sesion_chat import SesionChat
from app.schemas.sesion_chat import SesionChatCreate, SesionChatResponse, SesionChatUpdate

router = APIRouter(prefix="/sesiones_chat", tags=["Sesiones de Chat"])

@router.post("/", response_model=SesionChatResponse)
def create_sesion_chat(sesion: SesionChatCreate, db: Session = Depends(get_db)):
    nueva_sesion = SesionChat(**sesion.dict())
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    return nueva_sesion

@router.get("/", response_model=List[SesionChatResponse])
def get_sesiones_chat(db: Session = Depends(get_db)):
    return db.query(SesionChat).all()

@router.get("/{id_sesion}", response_model=SesionChatResponse)
def get_sesion_chat(id_sesion: int, db: Session = Depends(get_db)):
    sesion = db.query(SesionChat).filter(SesionChat.id_sesion == id_sesion).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return sesion

@router.put("/{id_sesion}", response_model=SesionChatResponse)
def update_sesion_chat(id_sesion: int, sesion_update: SesionChatUpdate, db: Session = Depends(get_db)):
    sesion = db.query(SesionChat).filter(SesionChat.id_sesion == id_sesion).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    for key, value in sesion_update.dict(exclude_unset=True).items():
        setattr(sesion, key, value)
    db.commit()
    db.refresh(sesion)
    return sesion

@router.delete("/{id_sesion}")
def delete_sesion_chat(id_sesion: int, db: Session = Depends(get_db)):
    sesion = db.query(SesionChat).filter(SesionChat.id_sesion == id_sesion).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    db.delete(sesion)
    db.commit()
    return {"detail": "Sesión eliminada correctamente"}
