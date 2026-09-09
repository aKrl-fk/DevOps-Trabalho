from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import livros, progresso, anotacoes, trechos, avaliacoes, metas, estatisticas

# Cria as tabelas no banco (se ainda não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Diário de Leitura API",
    description="API para registrar livros, progresso de leitura, anotações, trechos memoráveis e avaliações.",
    version="1.0.0",
)

# Libera acesso do frontend (ajustar em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(livros.router)
app.include_router(progresso.router)
app.include_router(anotacoes.router)
app.include_router(trechos.router)
app.include_router(avaliacoes.router)
app.include_router(metas.router)
app.include_router(estatisticas.router)


@app.get("/")
def raiz():
    return {"mensagem": "API do Diário de Leitura está no ar 📚"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
