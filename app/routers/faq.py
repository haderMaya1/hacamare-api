from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.faq import FaqCreate, FaqUpdate, FaqResponse
from app.services import faq_service as service
from app.utils.security import get_current_user

router = APIRouter(prefix="/faq", tags=["FAQ"])

@router.post("/", response_model=FaqResponse, status_code=status.HTTP_201_CREATED)
def crear_faq(data: FaqCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Solo usuarios autenticados pueden crear FAQs (puedes reforzar con rol si lo deseas)
    return service.crear_faq(db, data)

@router.get("/", response_model=List[FaqResponse])
def listar_faqs(db: Session = Depends(get_db)):
    # Se pueden listar sin autenticación si quieres que sean públicas
    return service.listar_faqs(db)

@router.get("/{faq_id}", response_model=FaqResponse)
def obtener_faq(faq_id: int, db: Session = Depends(get_db)):
    return service.obtener_faq(db, faq_id)

@router.put("/{faq_id}", response_model=FaqResponse)
def actualizar_faq(faq_id: int, data: FaqUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.actualizar_faq(db, faq_id, data)

@router.delete("/{faq_id}")
def eliminar_faq(faq_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.eliminar_faq(db, faq_id)
