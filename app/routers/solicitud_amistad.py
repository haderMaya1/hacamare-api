from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.solicitud_amistad import SolicitudCreate, SolicitudUpdate, SolicitudResponse
from app.services import solicitud_amistad_service as service
from app.utils.security import get_current_user

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])

@router.post("/", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED)
def crear(data: SolicitudCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.crear_solicitud(db, current_user.id_usuario, data)

@router.get("/", response_model=List[SolicitudResponse])
def listar(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.listar_solicitudes(db, current_user.id_usuario)

@router.put("/{solicitud_id}", response_model=SolicitudResponse)
def actualizar(solicitud_id: int, data: SolicitudUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.actualizar_estado(db, solicitud_id, current_user.id_usuario, data)

@router.delete("/{solicitud_id}")
def eliminar(solicitud_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.eliminar_solicitud(db, solicitud_id, current_user.id_usuario)
