from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.reaccion_publicacion import ReaccionCreate, ReaccionUpdate, ReaccionResponse
from app.services import reaccion_publicacion_service
from app.utils.security import get_current_user

router = APIRouter(prefix="/reacciones", tags=["Reacciones"])

@router.post("/", response_model=ReaccionResponse, status_code=status.HTTP_201_CREATED)
def crear_reaccion(reaccion: ReaccionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return reaccion_publicacion_service.crear_reaccion(db, reaccion, current_user)

@router.get("/publicacion/{id_publicacion}", response_model=List[ReaccionResponse])
def listar_reacciones(id_publicacion: int, db: Session = Depends(get_db)):
    return reaccion_publicacion_service.listar_reacciones_publicacion(db, id_publicacion)

@router.put("/{id_reaccion}", response_model=ReaccionResponse)
def actualizar_reaccion(id_reaccion: int, reaccion_update: ReaccionUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return reaccion_publicacion_service.actualizar_reaccion(db, id_reaccion, reaccion_update, current_user)

@router.delete("/{id_reaccion}")
def eliminar_reaccion(id_reaccion: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return reaccion_publicacion_service.eliminar_reaccion(db, id_reaccion, current_user)
