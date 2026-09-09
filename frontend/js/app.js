const STATUS_LABEL = {
  quero_ler: "Quero ler",
  lendo: "Lendo agora",
  lido: "Lido",
  abandonado: "Abandonado",
};

let livroSelecionadoId = null;
let filtroStatusAtual = "";
let abaAtiva = "progresso";

const shelfEl = document.getElementById("shelf");
const mainEl = document.getElementById("main");

// ---------- Estante (sidebar) ----------

async function carregarEstante() {
  const livros = await Api.listarLivros(filtroStatusAtual || undefined);
  shelfEl.innerHTML = "";

  if (livros.length === 0) {
    shelfEl.innerHTML = `<p style="color: var(--text-muted); font-size: 0.85rem;">Nenhum livro por aqui ainda.</p>`;
    return;
  }

  livros.forEach((livro) => {
    const item = document.createElement("button");
    item.className = "shelf-item" + (livro.id === livroSelecionadoId ? " active" : "");
    item.innerHTML = `
      <span class="titulo">${escapeHtml(livro.titulo)}</span>
      <span class="autor">${escapeHtml(livro.autor)}</span>
    `;
    item.addEventListener("click", () => selecionarLivro(livro.id));
    shelfEl.appendChild(item);
  });
}

document.querySelectorAll(".status-filters button").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".status-filters button").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    filtroStatusAtual = btn.dataset.status;
    carregarEstante();
  });
});

document.getElementById("btn-novo-livro").addEventListener("click", abrirFormNovoLivro);

// ---------- Formulário: novo livro ----------

function abrirFormNovoLivro() {
  livroSelecionadoId = null;
  mainEl.innerHTML = `
    <h2 style="margin-bottom: 20px;">Adicionar livro à estante</h2>
    <form id="form-novo-livro">
      <div class="form-row">
        <input name="titulo" placeholder="Título" required>
        <input name="autor" placeholder="Autor" required>
      </div>
      <div class="form-row">
        <input name="ano" type="number" placeholder="Ano">
        <input name="genero" placeholder="Gênero">
        <input name="total_paginas" type="number" placeholder="Total de páginas">
      </div>
      <div class="form-row">
        <select name="status">
          <option value="quero_ler">Quero ler</option>
          <option value="lendo">Lendo agora</option>
        </select>
        <button type="submit">Adicionar</button>
      </div>
    </form>
  `;

  document.getElementById("form-novo-livro").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const dados = {
      titulo: form.get("titulo"),
      autor: form.get("autor"),
      ano: form.get("ano") ? Number(form.get("ano")) : null,
      genero: form.get("genero") || null,
      total_paginas: form.get("total_paginas") ? Number(form.get("total_paginas")) : null,
      status: form.get("status"),
    };
    const livro = await Api.criarLivro(dados);
    await carregarEstante();
    selecionarLivro(livro.id);
  });
}

// ---------- Página do livro ----------

async function selecionarLivro(id) {
  livroSelecionadoId = id;
  abaAtiva = "progresso";
  await carregarEstante();
  await renderizarPaginaLivro();
}

async function renderizarPaginaLivro() {
  const livro = await Api.obterLivro(livroSelecionadoId);
  const progresso = await Api.listarProgresso(livroSelecionadoId);
  const ultimoProgresso = progresso.at(-1);
  const percentual = ultimoProgresso && livro.total_paginas
    ? Math.min(100, Math.round((ultimoProgresso.pagina_atual / livro.total_paginas) * 100))
    : 0;

  mainEl.innerHTML = `
    <div class="book-header">
      <div>
        <h2>${escapeHtml(livro.titulo)}</h2>
        <div class="autor">${escapeHtml(livro.autor)}${livro.ano ? ` · ${livro.ano}` : ""}${livro.genero ? ` · ${escapeHtml(livro.genero)}` : ""}</div>
        <span class="status-pill">${STATUS_LABEL[livro.status] || livro.status}</span>
      </div>
    </div>

    ${livro.total_paginas ? `
      <div style="margin-bottom: 24px;">
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:var(--text-muted);">
          <span>${ultimoProgresso ? ultimoProgresso.pagina_atual : 0} de ${livro.total_paginas} páginas</span>
          <span>${percentual}%</span>
        </div>
        <div class="progress-bar-track">
          <div class="progress-bar-fill" style="width:${percentual}%"></div>
        </div>
      </div>
    ` : ""}

    <div class="tabs">
      <button data-tab="progresso" class="${abaAtiva === "progresso" ? "active" : ""}">Progresso</button>
      <button data-tab="anotacoes" class="${abaAtiva === "anotacoes" ? "active" : ""}">Anotações</button>
      <button data-tab="trechos" class="${abaAtiva === "trechos" ? "active" : ""}">Trechos memoráveis</button>
      <button data-tab="avaliacao" class="${abaAtiva === "avaliacao" ? "active" : ""}">Avaliação</button>
    </div>

    <div id="tab-content"></div>
  `;

  mainEl.querySelectorAll(".tabs button").forEach((btn) => {
    btn.addEventListener("click", () => {
      abaAtiva = btn.dataset.tab;
      renderizarPaginaLivro();
    });
  });

  const tabContent = document.getElementById("tab-content");
  if (abaAtiva === "progresso") renderizarTabProgresso(tabContent, progresso);
  if (abaAtiva === "anotacoes") renderizarTabAnotacoes(tabContent);
  if (abaAtiva === "trechos") renderizarTabTrechos(tabContent);
  if (abaAtiva === "avaliacao") renderizarTabAvaliacao(tabContent, livro);
}

// ---------- Aba: Progresso ----------

function renderizarTabProgresso(container, progresso) {
  container.innerHTML = `
    <div class="form-row">
      <input id="input-pagina" type="number" placeholder="Página atual" min="0">
      <button id="btn-registrar-progresso">Registrar</button>
    </div>
    <div class="entry-list">
      ${progresso.slice().reverse().map((p) => `
        <div class="entry-card">
          <div class="meta">${formatarData(p.data)}</div>
          <div>Página ${p.pagina_atual}</div>
        </div>
      `).join("") || `<p style="color:var(--text-muted);">Nenhum progresso registrado ainda.</p>`}
    </div>
  `;

  document.getElementById("btn-registrar-progresso").addEventListener("click", async () => {
    const pagina = Number(document.getElementById("input-pagina").value);
    if (!pagina) return;
    await Api.registrarProgresso(livroSelecionadoId, { pagina_atual: pagina });
    await renderizarPaginaLivro();
  });
}

// ---------- Aba: Anotações ----------

async function renderizarTabAnotacoes(container) {
  const anotacoes = await Api.listarAnotacoes(livroSelecionadoId);
  container.innerHTML = `
    <div class="form-row">
      <input id="input-anotacao-pagina" type="number" placeholder="Página" style="max-width: 100px;">
      <textarea id="input-anotacao-texto" placeholder="Sua anotação..."></textarea>
      <button id="btn-add-anotacao">Salvar</button>
    </div>
    <div class="entry-list">
      ${anotacoes.slice().reverse().map((a) => `
        <div class="entry-card">
          <div class="meta">${formatarData(a.data)}${a.pagina ? ` · pág. ${a.pagina}` : ""}</div>
          <div>${escapeHtml(a.texto)}</div>
        </div>
      `).join("") || `<p style="color:var(--text-muted);">Nenhuma anotação ainda.</p>`}
    </div>
  `;

  document.getElementById("btn-add-anotacao").addEventListener("click", async () => {
    const texto = document.getElementById("input-anotacao-texto").value.trim();
    const pagina = document.getElementById("input-anotacao-pagina").value;
    if (!texto) return;
    await Api.criarAnotacao(livroSelecionadoId, {
      texto,
      pagina: pagina ? Number(pagina) : null,
    });
    renderizarTabAnotacoes(container);
  });
}

// ---------- Aba: Trechos ----------

async function renderizarTabTrechos(container) {
  const trechos = await Api.listarTrechos(livroSelecionadoId);
  container.innerHTML = `
    <div class="form-row">
      <input id="input-trecho-pagina" type="number" placeholder="Página" style="max-width: 100px;">
      <textarea id="input-trecho-texto" placeholder="Trecho memorável..."></textarea>
      <button id="btn-add-trecho">Salvar</button>
    </div>
    <div class="entry-list">
      ${trechos.slice().reverse().map((t) => `
        <div class="entry-card">
          ${t.pagina ? `<div class="meta">pág. ${t.pagina}</div>` : ""}
          <blockquote>"${escapeHtml(t.texto)}"</blockquote>
        </div>
      `).join("") || `<p style="color:var(--text-muted);">Nenhum trecho salvo ainda.</p>`}
    </div>
  `;

  document.getElementById("btn-add-trecho").addEventListener("click", async () => {
    const texto = document.getElementById("input-trecho-texto").value.trim();
    const pagina = document.getElementById("input-trecho-pagina").value;
    if (!texto) return;
    await Api.criarTrecho(livroSelecionadoId, {
      texto,
      pagina: pagina ? Number(pagina) : null,
    });
    renderizarTabTrechos(container);
  });
}

// ---------- Aba: Avaliação ----------

async function renderizarTabAvaliacao(container, livro) {
  const avaliacao = await Api.obterAvaliacao(livroSelecionadoId);

  if (avaliacao) {
    container.innerHTML = `
      <div class="entry-card">
        <div class="stars">${"★".repeat(Math.round(avaliacao.nota))}${"☆".repeat(5 - Math.round(avaliacao.nota))}</div>
        <div class="meta">Concluído em ${formatarData(avaliacao.data_conclusao)}</div>
        ${avaliacao.resenha ? `<p>${escapeHtml(avaliacao.resenha)}</p>` : ""}
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="form-row">
      <select id="input-nota">
        ${[5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1].map((n) => `<option value="${n}">${n} ★</option>`).join("")}
      </select>
    </div>
    <div class="form-row">
      <textarea id="input-resenha" placeholder="O que você achou do livro?"></textarea>
    </div>
    <div class="form-row">
      <button id="btn-avaliar">Finalizar avaliação</button>
    </div>
  `;

  document.getElementById("btn-avaliar").addEventListener("click", async () => {
    const nota = Number(document.getElementById("input-nota").value);
    const resenha = document.getElementById("input-resenha").value.trim();
    await Api.criarAvaliacao(livroSelecionadoId, { nota, resenha: resenha || null });
    await carregarEstante();
    renderizarPaginaLivro();
  });
}

// ---------- Utilitários ----------

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

function formatarData(dataStr) {
  const [ano, mes, dia] = dataStr.split("-");
  return `${dia}/${mes}/${ano}`;
}

// ---------- Inicialização ----------

carregarEstante();
