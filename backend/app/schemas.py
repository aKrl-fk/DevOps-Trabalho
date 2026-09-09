from pydantic import BaseModel
from typing import Optional
from datetime import date


# ---------- Livro ----------
class LivroBase(BaseModel):
    titulo: str
    autor: str
    ano: Optional[int] = None
    genero: Optional[str] = None
    total_paginas: Optional[int] = None
    status: Optional[str] = "quero_ler"


class LivroCreate(LivroBase):
    pass


class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    genero: Optional[str] = None
    total_paginas: Optional[int] = None
    status: Optional[str] = None


class LivroOut(LivroBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Progresso ----------
class ProgressoCreate(BaseModel):
    pagina_atual: int


class ProgressoOut(ProgressoCreate):
    id: int
    livro_id: int
    data: date

    class Config:
        from_attributes = True


# ---------- Anotacao ----------
class AnotacaoCreate(BaseModel):
    texto: str
    pagina: Optional[int] = None


class AnotacaoOut(AnotacaoCreate):
    id: int
    livro_id: int
    data: date

    class Config:
        from_attributes = True


# ---------- Trecho ----------
class TrechoCreate(BaseModel):
    texto: str
    pagina: Optional[int] = None


class TrechoOut(TrechoCreate):
    id: int
    livro_id: int

    class Config:
        from_attributes = True


# ---------- Avaliacao ----------
class AvaliacaoCreate(BaseModel):
    nota: float
    resenha: Optional[str] = None


class AvaliacaoOut(AvaliacaoCreate):
    id: int
    livro_id: int
    data_conclusao: date

    class Config:
        from_attributes = True


# ---------- Meta ----------
class MetaCreate(BaseModel):
    ano: int
    quantidade_meta: int


class MetaOut(MetaCreate):
    id: int

    class Config:
        from_attributes = True


class MetaProgresso(BaseModel):
    ano: int
    quantidade_meta: int
    livros_lidos: int
    percentual: float


# ---------- Estatisticas ----------
class Estatisticas(BaseModel):
    total_livros: int
    total_lidos: int
    total_lendo: int
    paginas_lidas_mes_atual: int
    nota_media: Optional[float] = None
    genero_mais_lido: Optional[str] = None
