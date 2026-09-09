from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Trechos"])


@router.post("/livros/{livro_id}/trechos", response_model=schemas.TrechoOut)
def criar_trecho(livro_id: int, trecho: schemas.TrechoCreate, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    novo = models.Trecho(livro_id=livro_id, **trecho.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/livros/{livro_id}/trechos", response_model=List[schemas.TrechoOut])
def listar_trechos(livro_id: int, db: Session = Depends(get_db)):
    return db.query(models.Trecho).filter(models.Trecho.livro_id == livro_id).all()


@router.delete("/trechos/{trecho_id}")
def remover_trecho(trecho_id: int, db: Session = Depends(get_db)):
    trecho = db.query(models.Trecho).filter(models.Trecho.id == trecho_id).first()
    if not trecho:
        raise HTTPException(status_code=404, detail="Trecho não encontrado")
    db.delete(trecho)
    db.commit()
    return {"detalhe": "Trecho removido com sucesso"}
