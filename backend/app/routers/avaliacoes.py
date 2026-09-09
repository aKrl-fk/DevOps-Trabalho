from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Avaliações"])


@router.post("/livros/{livro_id}/avaliacao", response_model=schemas.AvaliacaoOut)
def criar_avaliacao(livro_id: int, avaliacao: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    existente = db.query(models.Avaliacao).filter(models.Avaliacao.livro_id == livro_id).first()
    if existente:
        raise HTTPException(status_code=400, detail="Este livro já possui uma avaliação")

    nova = models.Avaliacao(livro_id=livro_id, **avaliacao.model_dump())
    db.add(nova)

    # Marca o livro como lido automaticamente
    livro.status = "lido"

    db.commit()
    db.refresh(nova)
    return nova


@router.get("/livros/{livro_id}/avaliacao", response_model=schemas.AvaliacaoOut)
def obter_avaliacao(livro_id: int, db: Session = Depends(get_db)):
    avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.livro_id == livro_id).first()
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao
