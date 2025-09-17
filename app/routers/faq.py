from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.faq import FaqCreate, FaqUpdate, FaqResponse
from app.services.faq_service import (
    crear_faq, obtener_faqs, obtener_faq, actualizar_faq, eliminar_faq
)

router = APIRouter(prefix="/faqs", tags=["FAQs"])

@router.post("/", response_model=dict)
def create_faq(faq: FaqCreate, db: Session = Depends(get_db)):
    nueva_faq = crear_faq(db, faq)
    return {
        "message": "FAQ creada exitosamente",
        "data": FaqResponse.model_validate(nueva_faq, from_attributes=True)   # 👈 CORREGIDO
    }

@router.get("/", response_model=dict)
def read_faqs(db: Session = Depends(get_db)):
    faqs = obtener_faqs(db)
    return {
        "data": [FaqResponse.model_validate(f, from_attributes=True) for f in faqs]   # 👈 CORREGIDO
    }

@router.get("/{id_faq}", response_model=dict)
def read_faq(id_faq: int, db: Session = Depends(get_db)):
    faq = obtener_faq(db, id_faq)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    return {"data": FaqResponse.model_validate(faq, from_attributes=True)}   # 👈 CORREGIDO

@router.put("/{id_faq}", response_model=dict)
def update_faq(id_faq: int, faq_data: FaqUpdate, db: Session = Depends(get_db)):
    faq_actualizada = actualizar_faq(db, id_faq, faq_data)
    if not faq_actualizada:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    return {
        "message": "FAQ actualizada correctamente",
        "data": FaqResponse.model_validate(faq_actualizada, from_attributes=True)   # 👈 CORREGIDO
    }

@router.delete("/{id_faq}", response_model=dict)
def delete_faq(id_faq: int, db: Session = Depends(get_db)):
    faq_eliminada = eliminar_faq(db, id_faq)
    if not faq_eliminada:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    return {"message": "FAQ eliminada correctamente"}
