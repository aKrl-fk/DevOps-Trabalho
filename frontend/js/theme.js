(function () {
  const root = document.documentElement;
  const toggleBtn = document.getElementById("theme-toggle");
  const salvo = localStorage.getItem("diario-tema");

  function aplicarTema(tema) {
    if (tema === "dark") {
      root.setAttribute("data-theme", "dark");
      toggleBtn.textContent = "☀️";
    } else {
      root.removeAttribute("data-theme");
      toggleBtn.textContent = "🌙";
    }
  }

  const preferencia = salvo || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  aplicarTema(preferencia);

  toggleBtn.addEventListener("click", () => {
    const atual = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
    const proximo = atual === "dark" ? "light" : "dark";
    aplicarTema(proximo);
    localStorage.setItem("diario-tema", proximo);
  });
})();
