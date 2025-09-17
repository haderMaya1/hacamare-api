from sqlalchemy.orm import Session
from app.models.usuario_interes import UsuarioInteres
from app.schemas.usuario_interes import UsuarioInteresCreate
from typing import List, Optional

def crear_usuario_interes(db: Session, usuario_interes: UsuarioInteresCreate) -> UsuarioInteres:
    nuevo = UsuarioInteres(**usuario_interes.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_usuario_intereses(db: Session) -> List[UsuarioInteres]:
    return db.query(UsuarioInteres).all()

def obtener_usuario_interes(db: Session, id_usuario: int, id_interes: int) -> Optional[UsuarioInteres]:
    return (
        db.query(UsuarioInteres)
        .filter(
            UsuarioInteres.id_usuario == id_usuario,
            UsuarioInteres.id_interes == id_interes
        )
        .first()
    )

def eliminar_usuario_interes(db: Session, id_usuario: int, id_interes: int) -> bool:
    rel = obtener_usuario_interes(db, id_usuario, id_interes)
    if not rel:
        return False
    db.delete(rel)
    db.commit()
    return True
