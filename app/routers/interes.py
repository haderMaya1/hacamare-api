from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import interes_service
from app.schemas.interes import InteresCreate, InteresResponse, InteresUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/intereses", tags=["intereses"])

@router.post("/", response_model=InteresResponse, status_code=201)
def crear_interes(interes: InteresCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return interes_service.create_interes(db, interes)

@router.get("/", response_model=List[InteresResponse])
def listar_intereses(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return interes_service.get_intereses(db)

@router.get("/{interes_id}", response_model=InteresResponse)
def obtener_interes(interes_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return interes_service.get_interes(db, interes_id)

@router.put("/{interes_id}", response_model=InteresResponse)
def actualizar_interes(interes_id: int, interes: InteresUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return interes_service.update_interes(db, interes_id, interes)

@router.delete("/{interes_id}")
def eliminar_interes(interes_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return interes_service.delete_interes(db, interes_id)
