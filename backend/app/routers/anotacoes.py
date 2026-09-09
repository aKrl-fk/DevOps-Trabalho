from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Anotações"])


@router.post("/livros/{livro_id}/anotacoes", response_model=schemas.AnotacaoOut)
def criar_anotacao(livro_id: int, anotacao: schemas.AnotacaoCreate, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    nova = models.Anotacao(livro_id=livro_id, **anotacao.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("/livros/{livro_id}/anotacoes", response_model=List[schemas.AnotacaoOut])
def listar_anotacoes(livro_id: int, db: Session = Depends(get_db)):
    return db.query(models.Anotacao).filter(models.Anotacao.livro_id == livro_id).all()


@router.delete("/anotacoes/{anotacao_id}")
def remover_anotacao(anotacao_id: int, db: Session = Depends(get_db)):
    anotacao = db.query(models.Anotacao).filter(models.Anotacao.id == anotacao_id).first()
    if not anotacao:
        raise HTTPException(status_code=404, detail="Anotação não encontrada")
    db.delete(anotacao)
    db.commit()
    return {"detalhe": "Anotação removida com sucesso"}
