from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.faq import Faq
from app.schemas.faq import FaqCreate, FaqUpdate

def crear_faq(db: Session, data: FaqCreate):
    faq = Faq(**data.dict())
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq

def listar_faqs(db: Session):
    return db.query(Faq).all()

def obtener_faq(db: Session, faq_id: int):
    faq = db.query(Faq).filter_by(id_faq=faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    return faq

def actualizar_faq(db: Session, faq_id: int, data: FaqUpdate):
    faq = obtener_faq(db, faq_id)
    if data.pregunta is not None:
        faq.pregunta = data.pregunta
    if data.respuesta is not None:
        faq.respuesta = data.respuesta
    db.commit()
    db.refresh(faq)
    return faq

def eliminar_faq(db: Session, faq_id: int):
    faq = obtener_faq(db, faq_id)
    db.delete(faq)
    db.commit()
    return {"message": "FAQ eliminada correctamente"}
