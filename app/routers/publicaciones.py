from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import publicacion_service
from app.schemas.publicacion import PublicacionCreate, PublicacionUpdate, PublicacionResponse
from app.utils.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/publicaciones", tags=["publicaciones"])


@router.get("/", response_model=List[PublicacionResponse])
def listar_publicaciones(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return publicacion_service.get_publicaciones(db, skip=skip, limit=limit)


@router.get("/{publicacion_id}", response_model=PublicacionResponse)
def obtener_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    return publicacion_service.get_publicacion(db, publicacion_id)


@router.post("/", response_model=PublicacionResponse, status_code=201)
def crear_publicacion(publicacion: PublicacionCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return publicacion_service.create_publicacion(db, publicacion, current_user.id_usuario)


@router.put("/{publicacion_id}", response_model=PublicacionResponse)
def actualizar_publicacion(publicacion_id: int, publicacion: PublicacionUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return publicacion_service.update_publicacion(
        db, publicacion_id, publicacion,
        usuario_id=current_user.id_usuario,
        es_admin=(current_user.id_rol == 1)
    )

@router.delete("/{publicacion_id}")
def eliminar_publicacion(
    publicacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return publicacion_service.delete_publicacion(
        db, publicacion_id,
        usuario_id=current_user.id_usuario,
        es_admin=(current_user.id_rol == 1)
    )
