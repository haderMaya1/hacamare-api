from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import usuario_service
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_service.get_usuarios(db, skip=skip, limit=limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_service.get_usuario(db, usuario_id)


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_service.create_usuario(db, usuario)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_service.update_usuario(db, usuario_id, usuario_data)


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_service.delete_usuario(db, usuario_id)


@router.post("/{usuario_id}/intereses/{interes_id}", response_model=UsuarioResponse)
def agregar_interes(usuario_id: int, interes_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_service.agregar_interes_usuario(db, usuario_id, interes_id)

@router.delete("/{usuario_id}/intereses/{interes_id}", response_model=UsuarioResponse)
def quitar_interes(usuario_id: int, interes_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_service.quitar_interes_usuario(db, usuario_id, interes_id)