from sqlalchemy.orm import Session
from app.models.faq import Faq
from app.schemas.faq import FaqCreate, FaqUpdate

def crear_faq(db: Session, faq: FaqCreate):
    nueva_faq = Faq(**faq.dict())
    db.add(nueva_faq)
    db.commit()
    db.refresh(nueva_faq)
    return nueva_faq

def obtener_faqs(db: Session):
    return db.query(Faq).all()

def obtener_faq(db: Session, id_faq: int):
    return db.query(Faq).filter(Faq.id_faq == id_faq).first()

def actualizar_faq(db: Session, id_faq: int, faq_data: FaqUpdate):
    faq = db.query(Faq).filter(Faq.id_faq == id_faq).first()
    if not faq:
        return None
    update_data = faq_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(faq, key, value)
    db.commit()
    db.refresh(faq)
    return faq

def eliminar_faq(db: Session, id_faq: int):
    faq = db.query(Faq).filter(Faq.id_faq == id_faq).first()
    if not faq:
        return None
    db.delete(faq)
    db.commit()
    return faq
