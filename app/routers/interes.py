from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import interes_service
from app.schemas.interes import InteresCreate, InteresResponse, InteresUpdate
from app.utils.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/intereses", tags=["intereses"])


def check_admin(user: Usuario):
    if user.id_rol != 1:  # Ajusta si tu rol de admin es distinto
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden realizar esta acción"
        )


# --- SOLO LECTURA (usuarios autenticados) ---
@router.get("/", response_model=List[InteresResponse])
def listar_intereses(db: Session = Depends(get_db)):
    return interes_service.get_intereses(db)


@router.get("/{interes_id}", response_model=InteresResponse)
def obtener_interes(interes_id: int, db: Session = Depends(get_db)):
    return interes_service.get_interes(db, interes_id)


# --- CRUD SOLO ADMIN ---
@router.post("/", response_model=InteresResponse, status_code=201)
def crear_interes(
    interes: InteresCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    check_admin(current_user)
    return interes_service.create_interes(db, interes)


@router.put("/{interes_id}", response_model=InteresResponse)
def actualizar_interes(
    interes_id: int,
    interes: InteresUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    check_admin(current_user)
    return interes_service.update_interes(db, interes_id, interes)


@router.delete("/{interes_id}")
def eliminar_interes(
    interes_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    check_admin(current_user)
    return interes_service.delete_interes(db, interes_id)
