from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.utils.security import hash_password
from app.utils.helpers import not_found_exception


def get_usuario(db: Session, usuario_id: int) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        not_found_exception("Usuario", usuario_id)
    return usuario


def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()


def create_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    nuevo_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        contraseña=hash_password(usuario.contraseña),
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        edad=usuario.edad,
        email=usuario.email,
        telefono=usuario.telefono,
        pais=usuario.pais,
        estado=usuario.estado,
        ciudad=usuario.ciudad,
        foto_perfil=usuario.foto_perfil,
        id_rol=usuario.id_rol,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate) -> Usuario:
    usuario = get_usuario(db, usuario_id)
    for key, value in usuario_data.model_dump(exclude_unset=True).items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(db: Session, usuario_id: int):
    usuario = get_usuario(db, usuario_id)
    db.delete(usuario)
    db.commit()
    return {"message": f"Usuario {usuario_id} eliminado"}
