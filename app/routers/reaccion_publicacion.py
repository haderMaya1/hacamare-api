from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reaccion_publicacion import ReaccionPublicacion
from app.schemas.reaccion_publicacion import ReaccionPublicacionCreate, ReaccionPublicacionResponse
from typing import List

router = APIRouter(prefix="/reacciones", tags=["Reacciones"])

@router.post("/", response_model=ReaccionPublicacionResponse)
def create_reaccion(reaccion: ReaccionPublicacionCreate, db: Session = Depends(get_db)):
    nueva_reaccion = ReaccionPublicacion(**reaccion.dict())
    db.add(nueva_reaccion)
    db.commit()
    db.refresh(nueva_reaccion)
    return nueva_reaccion

@router.get("/", response_model=List[ReaccionPublicacionResponse])
def get_reacciones(db: Session = Depends(get_db)):
    return db.query(ReaccionPublicacion).all()

@router.get("/{id_reaccion}", response_model=ReaccionPublicacionResponse)
def get_reaccion(id_reaccion: int, db: Session = Depends(get_db)):
    reaccion = db.query(ReaccionPublicacion).filter(ReaccionPublicacion.id_reaccion == id_reaccion).first()
    if not reaccion:
        raise HTTPException(status_code=404, detail="Reacción no encontrada")
    return reaccion

@router.delete("/{id_reaccion}")
def delete_reaccion(id_reaccion: int, db: Session = Depends(get_db)):
    reaccion = db.query(ReaccionPublicacion).filter(ReaccionPublicacion.id_reaccion == id_reaccion).first()
    if not reaccion:
        raise HTTPException(status_code=404, detail="Reacción no encontrada")
    db.delete(reaccion)
    db.commit()
    return {"detail": "Reacción eliminada correctamente"}
