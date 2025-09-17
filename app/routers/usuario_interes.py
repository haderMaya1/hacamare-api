from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.usuario_interes import UsuarioInteres
from app.schemas.usuario_interes import UsuarioInteresCreate, UsuarioInteresOut

router = APIRouter(prefix="/usuario_interes", tags=["UsuarioInteres"])

@router.post("/", response_model=UsuarioInteresOut)
def create_usuario_interes(relacion: UsuarioInteresCreate, db: Session = Depends(get_db)):
    existe = db.query(UsuarioInteres).filter_by(
        id_usuario=relacion.id_usuario, 
        id_interes=relacion.id_interes
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Relación ya existe")
    
    nueva = UsuarioInteres(**relacion.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=List[UsuarioInteresOut])
def get_relaciones(db: Session = Depends(get_db)):
    return db.query(UsuarioInteres).all()

@router.get("/usuario/{id_usuario}", response_model=List[UsuarioInteresOut])
def get_intereses_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return db.query(UsuarioInteres).filter_by(id_usuario=id_usuario).all()

@router.delete("/", response_model=dict)
def delete_usuario_interes(relacion: UsuarioInteresCreate, db: Session = Depends(get_db)):
    interes = db.query(UsuarioInteres).filter_by(
        id_usuario=relacion.id_usuario, id_interes=relacion.id_interes
    ).first()
    if not interes:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    db.delete(interes)
    db.commit()
    return {"detail": "Relación eliminada correctamente"}
