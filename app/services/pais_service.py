from sqlalchemy.orm import Session
from app.models.pais import Pais
from app.schemas.pais import PaisCreate
from fastapi import HTTPException

def get_paises(db: Session):
    return db.query(Pais).all()

def create_pais(db: Session, pais: PaisCreate) -> Pais:
    nuevo = Pais(**pais.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def get_pais(db: Session, pais_id: int) -> Pais:
    pais = db.query(Pais).filter(Pais.id_pais == pais_id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return pais
