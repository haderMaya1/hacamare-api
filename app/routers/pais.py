from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import pais_service
from app.schemas.pais import PaisCreate, PaisUpdate, PaisResponse
from app.utils.security import get_current_user
from app.utils.security import require_role

router = APIRouter(prefix="/paises", tags=["paises"])

# GET público
@router.get("/", response_model=List[PaisResponse])
def listar_paises(db: Session = Depends(get_db)):
    return pais_service.get_paises(db)

@router.get("/{pais_id}", response_model=PaisResponse)
def obtener_pais(pais_id: int, db: Session = Depends(get_db)):
    return pais_service.get_pais(db, pais_id)

# CRUD restringido a admin
@router.post("/", response_model=PaisResponse, status_code=201)
def crear_pais(
    pais: PaisCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):
    return pais_service.create_pais(db, pais)

@router.put("/{pais_id}", response_model=PaisResponse)
def actualizar_pais(
    pais_id: int,
    pais: PaisUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):
    return pais_service.update_pais(db, pais_id, pais)

@router.delete("/{pais_id}")
def eliminar_pais(
    pais_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):
    return pais_service.delete_pais(db, pais_id)
