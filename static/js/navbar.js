const navbar = document.querySelector(".navbar");
const botaoMenu = navbar.querySelector(".navbar-toggle");
const menu = navbar.querySelector(".navbar-nav");

function definirMenu(aberto) {
  menu.classList.toggle("aberto", aberto);
  botaoMenu.setAttribute("aria-expanded", String(aberto));
  botaoMenu.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
}

navbar.classList.add("navbar--interativa");

botaoMenu.addEventListener("click", () => {
  definirMenu(!menu.classList.contains("aberto"));
});

navbar.addEventListener("keydown", (evento) => {
  if (evento.key === "Escape" && menu.classList.contains("aberto")) {
    definirMenu(false);
    botaoMenu.focus();
  }
});