from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import sesion_chat_service
from app.schemas.sesion_chat import (
    SesionChatCreate,
    SesionChatResponse,
    SesionChatUpdate
)
from app.utils.security import get_current_user

router = APIRouter(prefix="/sesiones-chat", tags=["sesiones_chat"])

@router.post("/", response_model=SesionChatResponse, status_code=201)
def crear_sesion_chat(
    sesion: SesionChatCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return sesion_chat_service.create_sesion_chat(
        db=db,
        sesion=sesion,
        anfitrion_id=current_user.id_usuario
    )

@router.get("/", response_model=List[SesionChatResponse])
def listar_sesiones_chat(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return sesion_chat_service.get_sesiones_chat(db)

@router.get("/{sesion_id}", response_model=SesionChatResponse)
def obtener_sesion_chat(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return sesion_chat_service.get_sesion_chat(db, sesion_id)

@router.put("/{sesion_id}", response_model=SesionChatResponse)
def actualizar_sesion_chat(
    sesion_id: int,
    sesion: SesionChatUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return sesion_chat_service.update_sesion_chat(db, sesion_id, sesion)

@router.delete("/{sesion_id}")
def eliminar_sesion_chat(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return sesion_chat_service.delete_sesion_chat(db, sesion_id)
