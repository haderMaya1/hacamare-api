from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.solicitud_amistad import SolicitudAmistad
from app.schemas.solicitud_amistad import SolicitudCreate, SolicitudResponse
from typing import List

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes de Amistad"])

@router.post("/", response_model=SolicitudResponse)
def create_solicitud(solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    if solicitud.remitente_id == solicitud.destinatario_id:
        raise HTTPException(status_code=400, detail="No puedes enviarte solicitud a ti mismo")

    nueva_solicitud = SolicitudAmistad(**solicitud.dict())
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud

@router.get("/", response_model=List[SolicitudResponse])
def get_solicitudes(db: Session = Depends(get_db)):
    return db.query(SolicitudAmistad).all()

@router.put("/{id_solicitud}", response_model=SolicitudResponse)
def update_estado(id_solicitud: int, estado: str, db: Session = Depends(get_db)):
    solicitud = db.query(SolicitudAmistad).filter(SolicitudAmistad.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if estado not in ["pendiente", "aceptada", "rechazada"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    solicitud.estado = estado
    db.commit()
    db.refresh(solicitud)
    return solicitud

@router.delete("/{id_solicitud}")
def delete_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    solicitud = db.query(SolicitudAmistad).filter(SolicitudAmistad.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    db.delete(solicitud)
    db.commit()
    return {"detail": "Solicitud eliminada correctamente"}
