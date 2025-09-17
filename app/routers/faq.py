from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.faq import Faq
from app.schemas.faq import FaqCreate, FaqUpdate, FaqResponse
from typing import List

router = APIRouter(prefix="/faqs", tags=["FAQs"])

@router.post("/", response_model=FaqResponse)
def create_faq(faq: FaqCreate, db: Session = Depends(get_db)):
    nueva_faq = Faq(**faq.dict())
    db.add(nueva_faq)
    db.commit()
    db.refresh(nueva_faq)
    return nueva_faq

@router.get("/", response_model=List[FaqResponse])
def get_faqs(db: Session = Depends(get_db)):
    return db.query(Faq).all()

@router.get("/{id_faq}", response_model=FaqResponse)
def get_faq(id_faq: int, db: Session = Depends(get_db)):
    faq = db.query(Faq).filter(Faq.id_faq == id_faq).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    return faq

@router.put("/{id_faq}", response_model=FaqResponse)
def update_faq(id_faq: int, faq_update: FaqUpdate, db: Session = Depends(get_db)):
    faq = db.query(Faq).filter(Faq.id_faq == id_faq).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    for key, value in faq_update.dict().items():
        setattr(faq, key, value)
    db.commit()
    db.refresh(faq)
    return faq

@router.delete("/{id_faq}")
def delete_faq(id_faq: int, db: Session = Depends(get_db)):
    faq = db.query(Faq).filter(Faq.id_faq == id_faq).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    db.delete(faq)
    db.commit()
    return {"detail": "FAQ eliminada correctamente"}
