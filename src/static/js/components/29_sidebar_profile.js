async function cargarSidebar() {
  const contenedor = document.querySelector(".sidebar-container");

  if (!contenedor) return;

  try {
    const res = await fetch("/src/templates/components/29_sidebar_profile.html");
    if (!res.ok) throw new Error("Error al cargar el sidebar");

    const html = await res.text();

    // Insertar el sidebar
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = html.trim();
    contenedor.appendChild(tempDiv);

    // Activar comportamientos
    activarSidebarLinks(tempDiv);
    activarSidebarDesplegable(tempDiv);
    activarLogoutPopup(tempDiv); 
  } catch (error) {
    console.error("Error al cargar el sidebar:", error);
  }
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

function activarLogoutPopup(rootElement) {
  const logoutBtn = rootElement.querySelector(".sidebar__option-logoutBtn");

  const popupConfirm = document.querySelector(".sidebar__popup--confirm");
  const popupSuccess = document.querySelector(".sidebar__popup--success");

  if (!logoutBtn || !popupConfirm || !popupSuccess) return;

  const btnCancel = popupConfirm.querySelector(".sidebar__popup__btn--cancel");
  const btnAccept = popupConfirm.querySelector(".sidebar__popup__btn--accept");

  logoutBtn.addEventListener("click", (e) => {
    e.preventDefault();
    popupConfirm.classList.add("sidebar__popup--active");
  });

  btnCancel.addEventListener("click", () => {
    popupConfirm.classList.remove("sidebar__popup--active");
  });

  btnAccept.addEventListener("click", () => {
    popupConfirm.classList.remove("sidebar__popup--active");
    popupSuccess.classList.add("sidebar__popup--active");

    setTimeout(() => {
      popupSuccess.classList.remove("sidebar__popup--active");
      window.location.href = "/src/templates/pages-general/index.html";
    }, 2000);
  });
}


cargarSidebar();
