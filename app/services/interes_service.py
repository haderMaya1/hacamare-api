from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.interes import Interes
from app.schemas.interes import InteresCreate, InteresUpdate


# --- SOLO LECTURA PARA USUARIOS ---

def get_intereses(db: Session):
    """
    Lista todos los intereses disponibles
    """
    return db.query(Interes).order_by(Interes.nombre).all()


def get_interes(db: Session, interes_id: int):
    """
    Obtiene un interés específico
    """
    interes = db.query(Interes).filter(Interes.id_interes == interes_id).first()
    if not interes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interés no encontrado"
        )
    return interes


# --- CRUD SOLO PARA ADMIN ---

def create_interes(db: Session, interes: InteresCreate):
    """
    Crea un interés (solo admin)
    """
    existe = db.query(Interes).filter(Interes.nombre == interes.nombre).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El interés ya existe"
        )
    nuevo = Interes(nombre=interes.nombre, categoria=interes.categoria)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_interes(db: Session, interes_id: int, interes_update: InteresUpdate):
    """
    Actualiza un interés (solo admin)
    """
    interes = get_interes(db, interes_id)
    if interes_update.nombre is not None:
        interes.nombre = interes_update.nombre
    if interes_update.categoria is not None:
        interes.categoria = interes_update.categoria
    db.commit()
    db.refresh(interes)
    return interes


def delete_interes(db: Session, interes_id: int):
    """
    Elimina un interés (solo admin)
    """
    interes = get_interes(db, interes_id)
    db.delete(interes)
    db.commit()
    return {"message": "Interés eliminado correctamente"}
