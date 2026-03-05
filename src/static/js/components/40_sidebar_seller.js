async function cargarMensaje() {
  const contenedor = document.querySelector(".sidebar-container");

  const res = await fetch("/src/templates/components/40_sidebar_seller.html");
  const html = await res.text();

  const div = document.createElement("div");
  div.innerHTML = html;
  contenedor.appendChild(div);

  
  activarSidebarLinks(div);
  activarSidebarDesplegable(div); 

}



function activarSidebarLinks(rootElement) {
  const menuLinks = rootElement.querySelectorAll(".sidebar__menu a");

  menuLinks.forEach(link => {
    link.addEventListener("click", () => {
      
      menuLinks.forEach(l => l.classList.remove("active"));
      
      link.classList.add("active");
    });
  });
}


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
