# app/models/password_reset.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class PasswordReset(Base):
    __tablename__ = "password_reset"
    id_password_reset = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=15))
    
    usuarios = relationship("Usuario", back_populates="password_resets")
