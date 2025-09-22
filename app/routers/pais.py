from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import pais_service
from app.schemas.pais import PaisCreate, PaisResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/paises", tags=["paises"])

@router.get("/", response_model=List[PaisResponse])
def listar_paises(db: Session = Depends(get_db),
                  current_user=Depends(get_current_user)):
    return pais_service.get_paises(db)

@router.post("/", response_model=PaisResponse, status_code=201)
def crear_pais(pais: PaisCreate,
               db: Session = Depends(get_db),
               current_user=Depends(get_current_user)):
    return pais_service.create_pais(db, pais)
