from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime
from app.models.password_reset import PasswordReset
from app.models.usuario import Usuario
from app.utils.security import hash_password
from app.utils.helpers import get_user_by_email

def create_reset_token(db: Session, email: str) -> str:
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    token = str(uuid4())
    db.add(PasswordReset(user_id=user.id_usuario, token=token))
    db.commit()
    return token  # en producción se enviaría por email

def reset_password(db: Session, token: str, new_password: str):
    record = db.query(PasswordReset).filter(
        PasswordReset.token == token,
        PasswordReset.expires_at > datetime.utcnow()
    ).first()
    if not record:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    user = db.query(Usuario).filter_by(id_usuario=record.user_id).first()
    user.contraseña = hash_password(new_password)
    db.delete(record)
    db.commit()
