from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.solicitud_amistad import (
    SolicitudAmistadCreate, SolicitudAmistadUpdate, SolicitudAmistadResponse
)
from app.services.solicitud_amistad_service import (
    crear_solicitud, obtener_solicitudes, obtener_solicitud,
    actualizar_solicitud, eliminar_solicitud
)

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes de Amistad"])

@router.post("/", response_model=dict)
def create_solicitud(solicitud: SolicitudAmistadCreate, db: Session = Depends(get_db)):
    nueva = crear_solicitud(db, solicitud)
    return {
        "message": "Solicitud enviada exitosamente",
        "data": SolicitudAmistadResponse.model_validate(nueva, from_attributes=True)
    }

@router.get("/", response_model=dict)
def read_solicitudes(db: Session = Depends(get_db)):
    solicitudes = obtener_solicitudes(db)
    return {
        "data": [SolicitudAmistadResponse.model_validate(s, from_attributes=True) for s in solicitudes]
    }

@router.get("/{id_solicitud}", response_model=dict)
def read_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    solicitud = obtener_solicitud(db, id_solicitud)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return {"data": SolicitudAmistadResponse.model_validate(solicitud, from_attributes=True)}

@router.put("/{id_solicitud}", response_model=dict)
def update_solicitud(id_solicitud: int, solicitud_data: SolicitudAmistadUpdate, db: Session = Depends(get_db)):
    solicitud = actualizar_solicitud(db, id_solicitud, solicitud_data)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return {
        "message": "Solicitud actualizada correctamente",
        "data": SolicitudAmistadResponse.model_validate(solicitud, from_attributes=True)
    }

@router.delete("/{id_solicitud}", response_model=dict)
def delete_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    solicitud = eliminar_solicitud(db, id_solicitud)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return {"message": "Solicitud eliminada correctamente"}
