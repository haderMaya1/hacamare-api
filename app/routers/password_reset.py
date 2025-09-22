from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.password_reset import (ResetConfirm, ResetRequest)
from app.services.password_reset_services import (create_reset_token, reset_password)
from app.database import get_db

router = APIRouter(prefix="/password_reset", tags=["password_reset"])


@router.post("/password/forgot")
def forgot_password(data: ResetRequest, db: Session = Depends(get_db)):
    token = create_reset_token(db, data.email)
    return {"reset_token": token}  # Solo demo

@router.post("/password/reset")
def confirm_reset(data: ResetConfirm, db: Session = Depends(get_db)):
    reset_password(db, data.token, data.new_password)
    return {"message": "Contraseña actualizada"}