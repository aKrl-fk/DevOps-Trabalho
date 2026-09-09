from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/metas", tags=["Metas"])


@router.post("", response_model=schemas.MetaOut)
def criar_meta(meta: schemas.MetaCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Meta).filter(models.Meta.ano == meta.ano).first()
    if existente:
        raise HTTPException(status_code=400, detail="Já existe uma meta cadastrada para esse ano")
    nova = models.Meta(**meta.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("/{ano}", response_model=schemas.MetaProgresso)
def progresso_meta(ano: int, db: Session = Depends(get_db)):
    meta = db.query(models.Meta).filter(models.Meta.ano == ano).first()
    if not meta:
        raise HTTPException(status_code=404, detail="Meta não encontrada para esse ano")

    livros_lidos = (
        db.query(models.Livro)
        .join(models.Avaliacao)
        .filter(models.Avaliacao.data_conclusao.between(f"{ano}-01-01", f"{ano}-12-31"))
        .count()
    )

    percentual = round((livros_lidos / meta.quantidade_meta) * 100, 1) if meta.quantidade_meta else 0

    return schemas.MetaProgresso(
        ano=ano,
        quantidade_meta=meta.quantidade_meta,
        livros_lidos=livros_lidos,
        percentual=percentual,
    )
