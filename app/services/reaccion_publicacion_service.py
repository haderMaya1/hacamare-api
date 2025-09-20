from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.reaccion_publicacion import ReaccionPublicacion
from app.schemas.reaccion_publicacion import ReaccionCreate, ReaccionUpdate

VALID_REACTIONS = {"like", "dislike", "me_encanta", "me_divierte", "me_asombra", "me_entristece", "me_enoja"}

def crear_reaccion(db: Session, reaccion: ReaccionCreate, current_user):
    if reaccion.tipo not in VALID_REACTIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de reacción inválido")

    # Verificar si el usuario ya reaccionó a la publicación
    existente = db.query(ReaccionPublicacion).filter_by(
        id_usuario=current_user.id_usuario,
        id_publicacion=reaccion.id_publicacion
    ).first()
    if existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya has reaccionado a esta publicación")

    nueva_reaccion = ReaccionPublicacion(
        tipo=reaccion.tipo,
        id_usuario=current_user.id_usuario,
        id_publicacion=reaccion.id_publicacion
    )
    db.add(nueva_reaccion)
    db.commit()
    db.refresh(nueva_reaccion)
    return nueva_reaccion


def listar_reacciones_publicacion(db: Session, id_publicacion: int):
    return db.query(ReaccionPublicacion).filter_by(id_publicacion=id_publicacion).all()


def actualizar_reaccion(db: Session, id_reaccion: int, reaccion_update: ReaccionUpdate, current_user):
    reaccion = db.query(ReaccionPublicacion).filter_by(id_reaccion=id_reaccion).first()
    if not reaccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reacción no encontrada")

    if reaccion.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes editar esta reacción")

    if reaccion_update.tipo:
        if reaccion_update.tipo not in VALID_REACTIONS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de reacción inválido")
        reaccion.tipo = reaccion_update.tipo

    db.commit()
    db.refresh(reaccion)
    return reaccion


def eliminar_reaccion(db: Session, id_reaccion: int, current_user):
    reaccion = db.query(ReaccionPublicacion).filter_by(id_reaccion=id_reaccion).first()
    if not reaccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reacción no encontrada")

    if reaccion.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes eliminar esta reacción")

    db.delete(reaccion)
    db.commit()
    return {"message": "Reacción eliminada"}
