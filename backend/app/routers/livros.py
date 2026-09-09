from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("", response_model=schemas.LivroOut)
def criar_livro(livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    novo_livro = models.Livro(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@router.get("", response_model=List[schemas.LivroOut])
def listar_livros(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Livro)
    if status:
        query = query.filter(models.Livro.status == status)
    return query.all()


@router.get("/{livro_id}", response_model=schemas.LivroOut)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.put("/{livro_id}", response_model=schemas.LivroOut)
def atualizar_livro(livro_id: int, dados: schemas.LivroUpdate, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}")
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
    return {"detalhe": "Livro removido com sucesso"}
