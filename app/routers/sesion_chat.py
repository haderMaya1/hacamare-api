from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.sesion_chat import SesionChatCreate, SesionChatResponse, SesionChatUpdate
from app.services.sesion_chat_service import create_sesion_chat, update_sesion_chat, get_sesion_chat, get_sesiones_chat, delete_sesion_chat
from app.utils.security import get_current_user

router = APIRouter(prefix="/sesiones", tags=["sesiones"])

@router.post("/", response_model=SesionChatResponse, status_code=201)
def crear_sesion(sesion: SesionChatCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_sesion_chat(db, sesion, current_user.id_usuario)

@router.get("/{sesion_id}", response_model=SesionChatResponse)
def obtener_sesion(sesion_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_sesion_chat(db, sesion_id)

@router.get("/", response_model=List[SesionChatResponse])
def listar_sesiones(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_sesiones_chat(db)

@router.delete("/{sesion_id}")
def eliminar_sesion(sesion_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_sesion_chat(db, sesion_id, current_user.id_usuario)

@router.put("/{sesion_id}", response_model=SesionChatResponse)
def actualizar_sesion(sesion_id: int, sesion: SesionChatCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_sesion_chat(db, sesion_id, sesion, current_user.id_usuario)