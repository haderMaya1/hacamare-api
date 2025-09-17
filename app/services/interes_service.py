from sqlalchemy.orm import Session
from app.models.interes import Interes
from app.schemas.interes import InteresCreate, InteresUpdate
from typing import List, Optional

def crear_interes(db: Session, interes: InteresCreate) -> Interes:
    nuevo_interes = Interes(**interes.dict())
    db.add(nuevo_interes)
    db.commit()
    db.refresh(nuevo_interes)
    return nuevo_interes

def obtener_intereses(db: Session) -> List[Interes]:
    return db.query(Interes).all()

def obtener_interes_por_id(db: Session, interes_id: int) -> Optional[Interes]:
    return db.query(Interes).filter(Interes.id_interes == interes_id).first()

def actualizar_interes(db: Session, interes_id: int, interes: InteresUpdate) -> Optional[Interes]:
    db_interes = db.query(Interes).filter(Interes.id_interes == interes_id).first()
    if not db_interes:
        return None
    for key, value in interes.dict(exclude_unset=True).items():
        setattr(db_interes, key, value)
    db.commit()
    db.refresh(db_interes)
    return db_interes

def eliminar_interes(db: Session, interes_id: int) -> bool:
    db_interes = db.query(Interes).filter(Interes.id_interes == interes_id).first()
    if not db_interes:
        return False
    db.delete(db_interes)
    db.commit()
    return True
