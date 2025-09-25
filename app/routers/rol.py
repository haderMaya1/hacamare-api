from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services import rol_service
from app.schemas.rol import RolCreate, RolResponse, RolUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=List[RolResponse])
def listar_roles(db: Session = Depends(get_db),
                 current_user=Depends(get_current_user)):
    return rol_service.get_roles(db)

@router.get("/{rol_id}", response_model=RolResponse)
def obtener_rol(rol_id: int,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    return rol_service.get_rol(db, rol_id)

@router.post("/", response_model=RolResponse, status_code=201)
def crear_rol(rol: RolCreate,
              db: Session = Depends(get_db),
              current_user=Depends(get_current_user)):
    return rol_service.create_rol(db, rol)

@router.put("/{rol_id}", response_model=RolResponse)
def actualizar_rol(rol_id: int,
                   rol: RolUpdate,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    return rol_service.update_rol(db, rol_id, rol)

@router.delete("/{rol_id}")
def eliminar_rol(rol_id: int,
                 db: Session = Depends(get_db),
                 current_user=Depends(get_current_user)):
    return rol_service.delete_rol(db, rol_id)
