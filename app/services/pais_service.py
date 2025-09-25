from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.pais import Pais
from app.schemas.pais import PaisCreate, PaisUpdate

def get_paises(db: Session):
    return db.query(Pais).all()

def get_pais(db: Session, pais_id: int) -> Pais:
    pais = db.query(Pais).filter(Pais.id_pais == pais_id).first()
    if not pais:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="País no encontrado")
    return pais

def create_pais(db: Session, pais: PaisCreate) -> Pais:
    nuevo = Pais(**pais.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update_pais(db: Session, pais_id: int, pais_data: PaisUpdate) -> Pais:
    pais = get_pais(db, pais_id)
    for key, value in pais_data.model_dump(exclude_unset=True).items():
        setattr(pais, key, value)
    db.commit()
    db.refresh(pais)
    return pais

def delete_pais(db: Session, pais_id: int):
    pais = get_pais(db, pais_id)
    db.delete(pais)
    db.commit()
    return {"message": f"País {pais_id} eliminado correctamente"}
