document.addEventListener("DOMContentLoaded", () => {
  // Crear contenedor del popup
  const container = document.createElement("div");
  container.id = "logout_popup_container";
  document.body.appendChild(container);

  // Cargar el HTML del popup
  fetch("/src/templates/components/39_logout_popup.html")
    .then(response => response.text())
    .then(html => {
      container.innerHTML = html;
      inicializarLogoutPopup();
    })
    .catch(err => console.error("Error al cargar logout_popup:", err));
});

function inicializarLogoutPopup() {
  const popup = document.getElementById("logout_popup");
  const modal = document.getElementById("logout_success_modal");

  document.addEventListener("click", (e) => {
    // Abrir popup principal
    if (e.target.closest("#logoutBtn")) {
      e.preventDefault();
      popup.style.display = "flex";
    }

    // Cancelar popup
    if (e.target.closest("#logout_cancel")) {
      popup.style.display = "none";
    }

    // Aceptar  cerrar popup y mostrar modal
    if (e.target.closest("#logout_accept")) {
      popup.style.display = "none";
      mostrarModalCierre();
    }

    // Cerrar popup si se hace clic fuera del contenido
    if (e.target === popup) {
      popup.style.display = "none";
    }
  });
}

// --- Modal de cierre de sesión ---
function mostrarModalCierre() {
  const modal = document.getElementById("logout_success_modal");

  if (!modal) {
    console.error("No se encontró el modal logout_success_modal");
    return;
  }

  modal.style.display = "flex";

  // Esperar un momento a que el contenido esté disponible
  setTimeout(() => {
    const closeModalBtn = modal.querySelector(".close");
    const modalContent = modal.querySelector(".modal-content");

    const redirect = () => {
      window.location.href = "/src/templates/pages-general/index.html";
    };

    // Clic en x
    if (closeModalBtn) {
      closeModalBtn.addEventListener("click", redirect);
    }

    // Clic en fondo oscuro
    modal.addEventListener("click", (e) => {
      if (e.target === modal) redirect();
    });

    // Clic en bloque blanco (contenido)
    if (modalContent) {
      modalContent.addEventListener("click", (e) => {
        e.stopPropagation(); // evita conflicto con el fondo
        redirect();
      });
    }
  }, 50); 
}
