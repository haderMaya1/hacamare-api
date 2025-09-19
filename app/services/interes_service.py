from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.interes import Interes
from app.schemas.interes import InteresCreate, InteresUpdate

def create_interes(db: Session, interes: InteresCreate):
    nuevo = Interes(nombre=interes.nombre, categoria=interes.categoria)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def get_intereses(db: Session):
    return db.query(Interes).all()

def get_interes(db: Session, interes_id: int):
    interes = db.query(Interes).filter(Interes.id_interes == interes_id).first()
    if not interes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interés no encontrado")
    return interes

def update_interes(db: Session, interes_id: int, interes_update: InteresUpdate):
    interes = get_interes(db, interes_id)
    if interes_update.nombre is not None:
        interes.nombre = interes_update.nombre
    if interes_update.categoria is not None:
        interes.categoria = interes_update.categoria
    db.commit()
    db.refresh(interes)
    return interes

def delete_interes(db: Session, interes_id: int):
    interes = get_interes(db, interes_id)
    db.delete(interes)
    db.commit()
    return {"message": "Interés eliminado correctamente"}
