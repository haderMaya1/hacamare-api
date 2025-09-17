from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.usuario_service import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=dict)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = crear_usuario(db, usuario)
    return {
        "message": "Usuario creado exitosamente",
        "data": UsuarioResponse.model_validate(nuevo_usuario, from_attributes=True)   # 👈 CORREGIDO
    }

@router.get("/", response_model=dict)
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = obtener_usuarios(db)
    return {
        "message": "Lista de usuarios",
        "data": [UsuarioResponse.model_validate(u, from_attributes=True) for u in usuarios]  # 👈 CORREGIDO
    }

@router.get("/{usuario_id}", response_model=dict)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "message": "Usuario encontrado",
        "data": UsuarioResponse.model_validate(usuario, from_attributes=True)   # 👈 CORREGIDO
    }

@router.put("/{usuario_id}", response_model=dict)
def update_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    actualizado = actualizar_usuario(db, usuario_id, usuario)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "message": "Usuario actualizado correctamente",
        "data": UsuarioResponse.model_validate(actualizado, from_attributes=True)   # 👈 CORREGIDO
    }

@router.delete("/{usuario_id}", response_model=dict)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    eliminado = eliminar_usuario(db, usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
