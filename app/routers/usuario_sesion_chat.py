from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario_sesion_chat import UsuarioSesionChatCreate, UsuarioSesionChatResponse
from app.services import usuario_sesion_chat_service as service

router = APIRouter(prefix="/usuario-sesion-chat", tags=["Usuario - Sesión Chat"])

router = APIRouter(prefix="/usuario-sesion", tags=["UsuarioSesionChat"])

@router.post("/", response_model=UsuarioSesionChatResponse, status_code=201)
def add_usuario(usuario_sesion: UsuarioSesionChatCreate, db: Session = Depends(get_db)):
    return service.add_usuario_a_sesion(db, usuario_sesion)

@router.delete("/", status_code=200)
def remove_usuario(id_usuario: int, id_sesion: int, db: Session = Depends(get_db)):
    return service.remove_usuario_de_sesion(db, id_usuario, id_sesion)
@router.get("/", response_model=dict)
def get_relaciones_usuario_sesion(db: Session = Depends(get_db)):
    relaciones = service.get_relacion(db)
    return {
        "message": "Lista de relaciones usuario-sesión",
        "data": [UsuarioSesionChatResponse.model_validate(r, from_attributes=True) for r in relaciones]
    }

@router.get("/{id_usuario}/{id_sesion}", response_model=dict)
def get_relacion_usuario_sesion(id_usuario: int, id_sesion: int, db: Session = Depends(get_db)):
    relacion = service.get_relaciones_usuario_sesion(db, id_usuario, id_sesion)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {
        "message": "Relación encontrada",
        "data": UsuarioSesionChatResponse.model_validate(relacion, from_attributes=True)
    }