from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.publicacion import Publicacion
from app.schemas.publicacion import PublicacionCreate, PublicacionUpdate
from app.utils.helpers import not_found_exception


def get_publicaciones(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Publicacion).filter(Publicacion.estado == "visible").offset(skip).limit(limit).all()


def get_publicacion(db: Session, publicacion_id: int) -> Publicacion:
    publicacion = db.query(Publicacion).filter(Publicacion.id_publicacion == publicacion_id).first()
    if not publicacion:
        not_found_exception("Publicación", publicacion_id)
    return publicacion


def create_publicacion(db: Session, publicacion: PublicacionCreate, usuario_id: int) -> Publicacion:
    nueva_publicacion = Publicacion(
        texto=publicacion.texto,
        imagen=publicacion.imagen,
        id_usuario=usuario_id
    )
    db.add(nueva_publicacion)
    db.commit()
    db.refresh(nueva_publicacion)
    return nueva_publicacion


def update_publicacion(db: Session, publicacion_id: int,
                       publicacion_data: PublicacionUpdate,
                       usuario_id: int, es_admin: bool = False) -> Publicacion:
    publicacion = get_publicacion(db, publicacion_id)

    if not es_admin and publicacion.id_usuario != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta publicación"
        )

    for key, value in publicacion_data.model_dump(exclude_unset=True).items():
        setattr(publicacion, key, value)

    db.commit()
    db.refresh(publicacion)
    return publicacion



def delete_publicacion(db: Session, publicacion_id: int, usuario_id: int, es_admin: bool = False):
    publicacion = get_publicacion(db, publicacion_id)

    if not es_admin and publicacion.id_usuario != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta publicación"
        )

    # En lugar de borrar, marcamos como eliminada
    publicacion.estado = "eliminado"
    db.commit()
    return {"message": f"Publicación {publicacion_id} eliminada"}
