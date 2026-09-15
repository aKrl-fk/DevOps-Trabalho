# 📖 Diário de Leitura

Aplicação web para acompanhar sua jornada de leitura: cadastre os livros que está lendo, registre seu progresso página a página, escreva anotações, guarde os trechos mais memoráveis e avalie cada livro ao terminar.

Projeto desenvolvido como atividade prática da disciplina **DevOps e Integração Contínua** (Centro Universitário Internacional Uninter), aplicando a Cultura DevOps sobre um cenário de consultoria fictício (CodeFactory Solutions).

## Objetivo

Demonstrar, na prática, a adoção de práticas DevOps em um projeto de software: versionamento com Git/GitHub, containerização com Docker e automação de pipeline com Integração Contínua.

## Funcionalidades

- Cadastro de livros com status (quero ler / lendo / lido / abandonado)
- Registro de progresso de leitura (página atual, histórico)
- Anotações por livro
- Registro de trechos memoráveis (citações)
- Avaliação do livro (nota + resenha) ao concluir a leitura
- Metas de leitura anuais
- Estatísticas gerais (livros lidos, páginas no mês, nota média, gênero mais lido)
- Interface com modo claro e escuro

## Tecnologias utilizadas

**Backend**
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL

**Frontend**
- HTML5, CSS3
 e JavaScript puro

**Infraestrutura**
- Docker e Docker Compose
- GitHub Actions (Integração Contínua)

## Estrutura de pastas

```
diario-leitura/
├── backend/
│   ├── app/
│   │   ├── routers/          # rotas da API (livros, progresso, anotações...)
│   │   ├── database.py       # configuração de conexão com o banco
│   │   ├── models.py         # modelos SQLAlchemy (tabelas)
│   │   ├── schemas.py        # schemas Pydantic (validação)
│   │   └── main.py           # ponto de entrada da API
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── css/                  # theme.css (tokens claro/escuro) e style.css
│   ├── js/                   # api.js, theme.js, app.js
│   ├── index.html
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Como instalar e executar

### Pré-requisitos
- [Docker](https://www.docker.com/) e Docker Compose instalados

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/<seu-usuario>/diario-leitura.git
   cd diario-leitura
   ```

2. Suba os containers:
   ```bash
   docker compose up --build
   ```

3. Acesse:
   - Frontend: [http://localhost:8080](http://localhost:8080)
   - API (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

### Rodando o backend sem Docker (opcional, para desenvolvimento)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Por que usar containers neste projeto?

O ambiente do Diário de Leitura depende de três peças (API, banco de dados e frontend) que precisam funcionar juntas de forma previsível. Usar Docker resolve exatamente os problemas descritos no cenário da CodeFactory Solutions: elimina o "na minha máquina funciona", já que qualquer pessoa da equipe sobe o projeto inteiro com um único comando (`docker compose up`), sem precisar instalar PostgreSQL, Python ou configurar variáveis manualmente. Isso também facilita a integração contínua, pois o mesmo ambiente do desenvolvedor é o que roda nos testes automatizados.

## Integração Contínua

O fluxo de CI (GitHub Actions) roda automaticamente a cada push, executando build e verificação da aplicação — detalhes e evidências no relatório da atividade.

## Autoria

Desnvolvido por Maria Karoline Pedro Barbosa, como atividade prática da disciplina de DevOps e Integração Contínua.

## Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.
