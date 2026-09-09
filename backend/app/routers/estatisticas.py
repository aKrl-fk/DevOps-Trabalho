from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/estatisticas", tags=["Estatísticas"])


@router.get("", response_model=schemas.Estatisticas)
def obter_estatisticas(db: Session = Depends(get_db)):
    total_livros = db.query(models.Livro).count()
    total_lidos = db.query(models.Livro).filter(models.Livro.status == "lido").count()
    total_lendo = db.query(models.Livro).filter(models.Livro.status == "lendo").count()

    hoje = date.today()
    paginas_mes = (
        db.query(func.coalesce(func.sum(models.Progresso.pagina_atual), 0))
        .filter(
            extract("month", models.Progresso.data) == hoje.month,
            extract("year", models.Progresso.data) == hoje.year,
        )
        .scalar()
    )

    nota_media = db.query(func.avg(models.Avaliacao.nota)).scalar()

    genero_mais_lido = (
        db.query(models.Livro.genero, func.count(models.Livro.id).label("qtd"))
        .filter(models.Livro.status == "lido")
        .group_by(models.Livro.genero)
        .order_by(func.count(models.Livro.id).desc())
        .first()
    )

    return schemas.Estatisticas(
        total_livros=total_livros,
        total_lidos=total_lidos,
        total_lendo=total_lendo,
        paginas_lidas_mes_atual=paginas_mes or 0,
        nota_media=round(nota_media, 2) if nota_media else None,
        genero_mais_lido=genero_mais_lido[0] if genero_mais_lido else None,
    )
