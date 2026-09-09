from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
from .database import Base


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    ano = Column(Integer)
    genero = Column(String(100))
    total_paginas = Column(Integer)
    status = Column(String(20), default="quero_ler")  # quero_ler, lendo, lido, abandonado

    progressos = relationship("Progresso", back_populates="livro", cascade="all, delete-orphan")
    anotacoes = relationship("Anotacao", back_populates="livro", cascade="all, delete-orphan")
    trechos = relationship("Trecho", back_populates="livro", cascade="all, delete-orphan")
    avaliacao = relationship("Avaliacao", back_populates="livro", uselist=False, cascade="all, delete-orphan")


class Progresso(Base):
    __tablename__ = "progresso"

    id = Column(Integer, primary_key=True, index=True)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    pagina_atual = Column(Integer, nullable=False)
    data = Column(Date, default=date.today)

    livro = relationship("Livro", back_populates="progressos")


class Anotacao(Base):
    __tablename__ = "anotacoes"

    id = Column(Integer, primary_key=True, index=True)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    texto = Column(Text, nullable=False)
    pagina = Column(Integer)
    data = Column(Date, default=date.today)

    livro = relationship("Livro", back_populates="anotacoes")


class Trecho(Base):
    __tablename__ = "trechos"

    id = Column(Integer, primary_key=True, index=True)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    texto = Column(Text, nullable=False)
    pagina = Column(Integer)

    livro = relationship("Livro", back_populates="trechos")


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    livro_id = Column(Integer, ForeignKey("livros.id"), unique=True, nullable=False)
    nota = Column(Float, nullable=False)  # 0 a 5
    resenha = Column(Text)
    data_conclusao = Column(Date, default=date.today)

    livro = relationship("Livro", back_populates="avaliacao")


class Meta(Base):
    __tablename__ = "metas"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False, unique=True)
    quantidade_meta = Column(Integer, nullable=False)
