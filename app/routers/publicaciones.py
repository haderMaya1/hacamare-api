from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.publicacion import Publicacion
from app.schemas.publicacion import PublicacionCreate, PublicacionResponse, PublicacionUpdate

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"])

@router.post("/", response_model=PublicacionResponse)
def create_publicacion(publicacion: PublicacionCreate, db: Session = Depends(get_db)):
    nueva_pub = Publicacion(**publicacion.dict())
    db.add(nueva_pub)
    db.commit()
    db.refresh(nueva_pub)
    return nueva_pub

@router.get("/", response_model=List[PublicacionResponse])
def get_publicaciones(db: Session = Depends(get_db)):
    return db.query(Publicacion).all()

@router.get("/{id_publicacion}", response_model=PublicacionResponse)
def get_publicacion(id_publicacion: int, db: Session = Depends(get_db)):
    pub = db.query(Publicacion).filter(Publicacion.id_publicacion == id_publicacion).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return pub

@router.put("/{id_publicacion}", response_model=PublicacionResponse)
def update_publicacion(id_publicacion: int, pub_update: PublicacionUpdate, db: Session = Depends(get_db)):
    pub = db.query(Publicacion).filter(Publicacion.id_publicacion == id_publicacion).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    for key, value in pub_update.dict(exclude_unset=True).items():
        setattr(pub, key, value)
    db.commit()
    db.refresh(pub)
    return pub

@router.delete("/{id_publicacion}")
def delete_publicacion(id_publicacion: int, db: Session = Depends(get_db)):
    pub = db.query(Publicacion).filter(Publicacion.id_publicacion == id_publicacion).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    db.delete(pub)
    db.commit()
    return {"detail": "Publicación eliminada correctamente"}
