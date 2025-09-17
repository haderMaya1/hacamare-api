from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.usuario_sesion_chat import UsuarioSesionChat
from app.schemas.usuario_sesion_chat import UsuarioSesionChatCreate, UsuarioSesionChatResponse

router = APIRouter(prefix="/usuario_sesion_chat", tags=["Usuarios en Sesiones de Chat"])

@router.post("/", response_model=UsuarioSesionChatResponse)
def create_usuario_sesion_chat(relacion: UsuarioSesionChatCreate, db: Session = Depends(get_db)):
    existe = db.query(UsuarioSesionChat).filter_by(
        id_usuario=relacion.id_usuario, id_sesion=relacion.id_sesion
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="La relación ya existe")
    nueva_relacion = UsuarioSesionChat(**relacion.dict())
    db.add(nueva_relacion)
    db.commit()
    db.refresh(nueva_relacion)
    return nueva_relacion

@router.get("/", response_model=List[UsuarioSesionChatResponse])
def get_relaciones(db: Session = Depends(get_db)):
    return db.query(UsuarioSesionChat).all()

@router.get("/usuario/{id_usuario}", response_model=List[UsuarioSesionChatResponse])
def get_sesiones_de_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return db.query(UsuarioSesionChat).filter(UsuarioSesionChat.id_usuario == id_usuario).all()

@router.get("/sesion/{id_sesion}", response_model=List[UsuarioSesionChatResponse])
def get_usuarios_de_sesion(id_sesion: int, db: Session = Depends(get_db)):
    return db.query(UsuarioSesionChat).filter(UsuarioSesionChat.id_sesion == id_sesion).all()

@router.delete("/")
def delete_usuario_sesion_chat(relacion: UsuarioSesionChatCreate, db: Session = Depends(get_db)):
    obj = db.query(UsuarioSesionChat).filter_by(
        id_usuario=relacion.id_usuario, id_sesion=relacion.id_sesion
    ).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    db.delete(obj)
    db.commit()
    return {"message": "Relación eliminada"}
