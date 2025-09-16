from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.interes import Interes
from app.schemas.interes import InteresCreate, InteresUpdate, InteresOut

router = APIRouter(prefix="/intereses", tags=["Interes"])

@router.post("/", response_model=InteresOut)
def create_interes(interes: InteresCreate, db: Session = Depends(get_db)):
    nuevo = Interes(**interes.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=List[InteresOut])
def get_intereses(db: Session = Depends(get_db)):
    return db.query(Interes).all()

@router.get("/{id_interes}", response_model=InteresOut)
def get_interes(id_interes: int, db: Session = Depends(get_db)):
    interes = db.query(Interes).filter(Interes.id_interes == id_interes).first()
    if not interes:
        raise HTTPException(status_code=404, detail="Interes no encontrado")
    return interes

@router.put("/{id_interes}", response_model=InteresOut)
def update_interes(id_interes: int, interes_update: InteresUpdate, db: Session = Depends(get_db)):
    interes = db.query(Interes).filter(Interes.id_interes == id_interes).first()
    if not interes:
        raise HTTPException(status_code=404, detail="Interes no encontrado")
    for key, value in interes_update.model_dump(exclude_unset=True).items():
        setattr(interes, key, value)
    db.commit()
    db.refresh(interes)
    return interes

@router.delete("/{id_interes}")
def delete_interes(id_interes: int, db: Session = Depends(get_db)):
    interes = db.query(Interes).filter(Interes.id_interes == id_interes).first()
    if not interes:
        raise HTTPException(status_code=404, detail="Interes no encontrado")
    db.delete(interes)
    db.commit()
    return {"detail": "Interes eliminado correctamente"}
