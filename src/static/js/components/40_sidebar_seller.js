async function cargarMensaje() {
  const contenedor = document.querySelector(".sidebar-container");

  const res = await fetch("/src/templates/components/40_sidebar_seller.html");
  const html = await res.text();

  const div = document.createElement("div");
  div.innerHTML = html;
  contenedor.appendChild(div);

  //  Espera a que el sidebar esté cargado y aplica el comportamiento de "activo"
  activarSidebarLinks(div);
  activarSidebarDesplegable(div); 

}


// Función que agrega el comportamiento de selección activa
function activarSidebarLinks(rootElement) {
  const menuLinks = rootElement.querySelectorAll(".sidebar__menu a");

  menuLinks.forEach(link => {
    link.addEventListener("click", () => {
      // Quita "active" de todos los enlaces
      menuLinks.forEach(l => l.classList.remove("active"));
      // Agrega "active" solo al enlace clicado
      link.classList.add("active");
    });
  });
}

// función: menú desplegable
function activarSidebarDesplegable(rootElement) {
  const subtitle = rootElement.querySelector(".sidebar__list");
  const menu = rootElement.querySelector(".sidebar__menu");

  if (!subtitle || !menu) return;

  subtitle.addEventListener("click", () => {
    menu.classList.toggle("sidebar__menu--visible");
    subtitle.classList.toggle("sidebar__subtitle--active");
  });
}

cargarMensaje();
