from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.comentario import ComentarioCreate, ComentarioResponse, ComentarioUpdate
from app.services import comentario_service
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.post("/", response_model=ComentarioResponse, status_code=status.HTTP_201_CREATED)
def crear_comentario(
    data: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return comentario_service.crear_comentario(db, data, current_user.id_usuario)

@router.get("/{comentario_id}", response_model=ComentarioResponse)
def obtener_comentario(
    comentario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return comentario_service.obtener_comentario(db, comentario_id)

@router.get("/publicacion/{publicacion_id}", response_model=list[ComentarioResponse])
def listar_comentarios(
    publicacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return comentario_service.listar_comentarios(db, publicacion_id)

@router.put("/{comentario_id}", response_model=ComentarioResponse)
def actualizar_comentario(
    comentario_id: int,
    data: ComentarioUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return comentario_service.actualizar_comentario(db, comentario_id, current_user.id_usuario, data)

@router.delete("/{comentario_id}")
def eliminar_comentario(
    comentario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return comentario_service.eliminar_comentario(db, comentario_id, current_user.id_usuario)
