from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/livros/{livro_id}/progresso", tags=["Progresso"])


def _buscar_livro(livro_id: int, db: Session) -> models.Livro:
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.post("", response_model=schemas.ProgressoOut)
def registrar_progresso(livro_id: int, progresso: schemas.ProgressoCreate, db: Session = Depends(get_db)):
    _buscar_livro(livro_id, db)
    novo = models.Progresso(livro_id=livro_id, **progresso.model_dump())
    db.add(novo)

    # Atualiza status do livro para "lendo" automaticamente
    livro = _buscar_livro(livro_id, db)
    if livro.status == "quero_ler":
        livro.status = "lendo"

    db.commit()
    db.refresh(novo)
    return novo


@router.get("", response_model=List[schemas.ProgressoOut])
def listar_progresso(livro_id: int, db: Session = Depends(get_db)):
    _buscar_livro(livro_id, db)
    return (
        db.query(models.Progresso)
        .filter(models.Progresso.livro_id == livro_id)
        .order_by(models.Progresso.data)
        .all()
    )
