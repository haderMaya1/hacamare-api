from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.interes import InteresCreate, InteresUpdate, InteresResponse
from app.services.interes_service import (
    crear_interes,
    obtener_intereses,
    obtener_interes_por_id,
    actualizar_interes,
    eliminar_interes,
)

router = APIRouter(prefix="/intereses", tags=["Intereses"])

@router.post("/", response_model=dict)
def create_interes(interes: InteresCreate, db: Session = Depends(get_db)):
    nuevo_interes = crear_interes(db, interes)
    return {
        "message": "Interés creado exitosamente",
        "data": InteresResponse.model_validate(nuevo_interes, from_attributes=True)
    }

@router.get("/", response_model=dict)
def get_intereses(db: Session = Depends(get_db)):
    intereses = obtener_intereses(db)
    return {
        "message": "Lista de intereses",
        "data": [InteresResponse.model_validate(i, from_attributes=True) for i in intereses]
    }

@router.get("/{interes_id}", response_model=dict)
def get_interes(interes_id: int, db: Session = Depends(get_db)):
    interes = obtener_interes_por_id(db, interes_id)
    if not interes:
        raise HTTPException(status_code=404, detail="Interés no encontrado")
    return {
        "message": "Interés encontrado",
        "data": InteresResponse.model_validate(interes, from_attributes=True)
    }

@router.put("/{interes_id}", response_model=dict)
def update_interes(interes_id: int, interes: InteresUpdate, db: Session = Depends(get_db)):
    actualizado = actualizar_interes(db, interes_id, interes)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Interés no encontrado")
    return {
        "message": "Interés actualizado correctamente",
        "data": InteresResponse.model_validate(actualizado, from_attributes=True)
    }

@router.delete("/{interes_id}", response_model=dict)
def delete_interes(interes_id: int, db: Session = Depends(get_db)):
    eliminado = eliminar_interes(db, interes_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Interés no encontrado")
    return {"message": "Interés eliminado correctamente"}
