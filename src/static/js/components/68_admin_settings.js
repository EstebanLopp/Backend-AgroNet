document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".settings-container");

  if (container) {
    fetch("/src/templates/components/68_admin_settings.html")
      .then(response => {
        if (!response.ok) throw new Error("Error al cargar componente settings");
        return response.text();
      })
      .then(data => {
        container.innerHTML = data;

        // Inicializamos pasando el root principal
        const root = container.querySelector(".admin-settings");
        initSettingsPopups(root);
      })
      .catch(error => console.error("Error al cargar el componente Settings:", error));
  }
});

function initSettingsPopups(root) {
  if (!root) return;

  // --- Botones principales del formulario ---
  const btnGuardar = root.querySelector(".admin-settings__btn--save");
  const btnPassword = root.querySelector(".admin-settings__btn--secure");

  // --- Popups ---
  const popupConfirm = document.querySelector(".admin-settings__popup--confirm");
  const popupSuccess = document.querySelector(".admin-settings__popup--success");

  // Clase que controla la visibilidad del popup
  const SHOW_CLASS = "admin-settings__popup--show";

  // --- Botones internos ---
  const cancelBtn = popupConfirm?.querySelector(".admin-settings__popup-btn--cancel");
  const acceptBtn = popupConfirm?.querySelector(".admin-settings__popup-btn--accept");
  const closeBtns = document.querySelectorAll(".admin-settings__popup-close");

  // Si no existen los popups, detener ejecución
  if (!popupConfirm || !popupSuccess) {
    console.warn("⚠️ No se encontraron los popups en el HTML — revisa las clases BEM.");
    return;
  }

  // ---  Funciones para abrir/cerrar popups ---
  function openConfirm() {
    popupConfirm.classList.add(SHOW_CLASS);
  }

  function closeConfirm() {
    popupConfirm.classList.remove(SHOW_CLASS);
  }

  function openSuccess() {
    popupSuccess.classList.add(SHOW_CLASS);
  }

  function closeSuccess() {
    popupSuccess.classList.remove(SHOW_CLASS);
  }

  // ---  Abrir confirmación al hacer clic en guardar o actualizar contraseña ---
  [btnGuardar, btnPassword].forEach(btn => {
    if (!btn) return;
    btn.addEventListener("click", e => {
      e.preventDefault();
      openConfirm();
    });
  });

  // ---  Botón "Cancelar" cierra confirmación ---
  cancelBtn?.addEventListener("click", e => {
    e.preventDefault();
    closeConfirm();
  });

  // --- Botón "Aceptar" muestra popup de éxito ---
  acceptBtn?.addEventListener("click", e => {
    e.preventDefault();
    closeConfirm();
    setTimeout(openSuccess, 250); // leve retardo visual
  });

  // --- Cerrar con la X ---
  closeBtns.forEach(btn => {
    btn.addEventListener("click", e => {
      const popupRoot = btn.closest(".admin-settings__popup");
      if (!popupRoot) return;
      popupRoot.classList.remove(SHOW_CLASS);

      // Si se cierra el popup de éxito, recarga o redirige
      if (popupRoot.classList.contains("admin-settings__popup--success")) {
        window.location.href = "/src/templates/admin-pages/settings.html";
      }
    });
  });

  // --- Cerrar si se hace clic fuera del contenido ---
  [popupConfirm, popupSuccess].forEach(popup => {
    popup.addEventListener("click", e => {
      if (e.target === popup) {
        popup.classList.remove(SHOW_CLASS);
        if (popup === popupSuccess) {
          window.location.href = "/src/templates/admin-pages/settings.html";
        }
      }
    });

    // Evitar cierre al hacer clic dentro del contenido
    const content = popup.querySelector(".admin-settings__popup-content");
    content?.addEventListener("click", e => e.stopPropagation());
  });

  // --- Cerrar con tecla ESC ---
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      closeConfirm();
      closeSuccess();
    }
  });
}
