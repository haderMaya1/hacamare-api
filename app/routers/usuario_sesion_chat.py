# app/routers/usuario_sesion_chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import usuario_sesion_chat_service
from app.schemas.usuario_sesion_chat import UsuarioSesionChatCreate, UsuarioSesionChatResponse
from app.utils.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/usuario-sesion-chat", tags=["usuario-sesion-chat"])

@router.post("/", response_model=UsuarioSesionChatResponse, status_code=201)
def join_session(body: UsuarioSesionChatCreate,
                 db: Session = Depends(get_db),
                 current_user: Usuario = Depends(get_current_user)):
    return usuario_sesion_chat_service.join_session(
        db, current_user.id_usuario, body.id_sesion
    )

@router.delete("/", status_code=200)
def leave_session(body: UsuarioSesionChatCreate,
                  db: Session = Depends(get_db),
                  current_user: Usuario = Depends(get_current_user)):
    return usuario_sesion_chat_service.leave_session(
        db, current_user.id_usuario, body.id_sesion
    )

@router.get("/participants/{id_sesion}", response_model=List[UsuarioSesionChatResponse])
def list_participants(id_sesion: int,
                      db: Session = Depends(get_db),
                      current_user: Usuario = Depends(get_current_user)):
    return usuario_sesion_chat_service.list_participants(db, id_sesion)
