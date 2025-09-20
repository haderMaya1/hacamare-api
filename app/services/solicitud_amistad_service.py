from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.solicitud_amistad import SolicitudAmistad
from app.models.usuario import Usuario
from app.schemas.solicitud_amistad import SolicitudCreate, SolicitudUpdate

def crear_solicitud(db: Session, remitente_id: int, data: SolicitudCreate):
    # Verificar que el destinatario exista
    destinatario = db.query(Usuario).filter_by(id_usuario=data.destinatario_id).first()
    if not destinatario:
        raise HTTPException(status_code=404, detail="Destinatario no encontrado")
    if destinatario.id_usuario == remitente_id:
        raise HTTPException(status_code=400, detail="No puedes enviarte una solicitud a ti mismo")

    # Verificar si ya existe una solicitud pendiente
    existente = db.query(SolicitudAmistad).filter(
        SolicitudAmistad.remitente_id == remitente_id,
        SolicitudAmistad.destinatario_id == data.destinatario_id,
        SolicitudAmistad.estado == "pendiente"
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una solicitud pendiente")

    nueva = SolicitudAmistad(
        mensaje=data.mensaje,
        remitente_id=remitente_id,
        destinatario_id=data.destinatario_id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_solicitudes(db: Session, user_id: int):
    return db.query(SolicitudAmistad).filter(
        (SolicitudAmistad.remitente_id == user_id) |
        (SolicitudAmistad.destinatario_id == user_id)
    ).all()

def actualizar_estado(db: Session, solicitud_id: int, user_id: int, data: SolicitudUpdate):
    solicitud = db.query(SolicitudAmistad).filter_by(id_solicitud=solicitud_id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if solicitud.destinatario_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para actualizar esta solicitud")

    if data.estado not in ["aceptada", "rechazada"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    solicitud.estado = data.estado
    db.commit()
    db.refresh(solicitud)
    return solicitud

def eliminar_solicitud(db: Session, solicitud_id: int, user_id: int):
    solicitud = db.query(SolicitudAmistad).filter_by(id_solicitud=solicitud_id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if solicitud.remitente_id != user_id and solicitud.destinatario_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar esta solicitud")

    db.delete(solicitud)
    db.commit()
    return {"message": "Solicitud eliminada"}
