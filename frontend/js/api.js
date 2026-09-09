const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://localhost:8000"
  : "/api";

async function apiRequest(path, options = {}) {
  const resp = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!resp.ok) {
    const erro = await resp.json().catch(() => ({}));
    throw new Error(erro.detail || `Erro na requisição: ${resp.status}`);
  }
  if (resp.status === 204) return null;
  return resp.json();
}

const Api = {
  listarLivros: (status) => apiRequest(`/livros${status ? `?status=${status}` : ""}`),
  obterLivro: (id) => apiRequest(`/livros/${id}`),
  criarLivro: (dados) => apiRequest("/livros", { method: "POST", body: JSON.stringify(dados) }),
  removerLivro: (id) => apiRequest(`/livros/${id}`, { method: "DELETE" }),

  listarProgresso: (livroId) => apiRequest(`/livros/${livroId}/progresso`),
  registrarProgresso: (livroId, dados) =>
    apiRequest(`/livros/${livroId}/progresso`, { method: "POST", body: JSON.stringify(dados) }),

  listarAnotacoes: (livroId) => apiRequest(`/livros/${livroId}/anotacoes`),
  criarAnotacao: (livroId, dados) =>
    apiRequest(`/livros/${livroId}/anotacoes`, { method: "POST", body: JSON.stringify(dados) }),

  listarTrechos: (livroId) => apiRequest(`/livros/${livroId}/trechos`),
  criarTrecho: (livroId, dados) =>
    apiRequest(`/livros/${livroId}/trechos`, { method: "POST", body: JSON.stringify(dados) }),

  obterAvaliacao: (livroId) => apiRequest(`/livros/${livroId}/avaliacao`).catch(() => null),
  criarAvaliacao: (livroId, dados) =>
    apiRequest(`/livros/${livroId}/avaliacao`, { method: "POST", body: JSON.stringify(dados) }),

  estatisticas: () => apiRequest("/estatisticas"),
};
