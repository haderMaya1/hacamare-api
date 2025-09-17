from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comentario import Comentario
from app.schemas.comentario import ComentarioCreate, ComentarioResponse
from typing import List

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.post("/", response_model=ComentarioResponse)
def create_comentario(comentario: ComentarioCreate, db: Session = Depends(get_db)):
    nuevo_comentario = Comentario(**comentario.dict())
    db.add(nuevo_comentario)
    db.commit()
    db.refresh(nuevo_comentario)
    return nuevo_comentario

@router.get("/", response_model=List[ComentarioResponse])
def get_comentarios(db: Session = Depends(get_db)):
    return db.query(Comentario).all()

@router.get("/{id_comentario}", response_model=ComentarioResponse)
def get_comentario(id_comentario: int, db: Session = Depends(get_db)):
    comentario = db.query(Comentario).filter(Comentario.id_comentario == id_comentario).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comentario

@router.delete("/{id_comentario}")
def delete_comentario(id_comentario: int, db: Session = Depends(get_db)):
    comentario = db.query(Comentario).filter(Comentario.id_comentario == id_comentario).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    db.delete(comentario)
    db.commit()
    return {"detail": "Comentario eliminado correctamente"}
