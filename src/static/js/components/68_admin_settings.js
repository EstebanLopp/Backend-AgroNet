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

        
        const root = container.querySelector(".admin-settings");
        initSettingsPopups(root);
      })
      .catch(error => console.error("Error al cargar el componente Settings:", error));
  }
});

function initSettingsPopups(root) {
  if (!root) return;

  
  const btnGuardar = root.querySelector(".admin-settings__btn--save");
  const btnPassword = root.querySelector(".admin-settings__btn--secure");

  
  const popupConfirm = document.querySelector(".admin-settings__popup--confirm");
  const popupSuccess = document.querySelector(".admin-settings__popup--success");

  
  const SHOW_CLASS = "admin-settings__popup--show";

  
  const cancelBtn = popupConfirm?.querySelector(".admin-settings__popup-btn--cancel");
  const acceptBtn = popupConfirm?.querySelector(".admin-settings__popup-btn--accept");
  const closeBtns = document.querySelectorAll(".admin-settings__popup-close");

  
  if (!popupConfirm || !popupSuccess) {
    console.warn("⚠️ No se encontraron los popups en el HTML — revisa las clases BEM.");
    return;
  }

  
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

  
  [btnGuardar, btnPassword].forEach(btn => {
    if (!btn) return;
    btn.addEventListener("click", e => {
      e.preventDefault();
      openConfirm();
    });
  });

  
  cancelBtn?.addEventListener("click", e => {
    e.preventDefault();
    closeConfirm();
  });

  
  acceptBtn?.addEventListener("click", e => {
    e.preventDefault();
    closeConfirm();
    setTimeout(openSuccess, 250); 
  });

  
  closeBtns.forEach(btn => {
    btn.addEventListener("click", e => {
      const popupRoot = btn.closest(".admin-settings__popup");
      if (!popupRoot) return;
      popupRoot.classList.remove(SHOW_CLASS);

      
      if (popupRoot.classList.contains("admin-settings__popup--success")) {
        window.location.href = "/src/templates/admin-pages/settings.html";
      }
    });
  });

  
  [popupConfirm, popupSuccess].forEach(popup => {
    popup.addEventListener("click", e => {
      if (e.target === popup) {
        popup.classList.remove(SHOW_CLASS);
        if (popup === popupSuccess) {
          window.location.href = "/src/templates/admin-pages/settings.html";
        }
      }
    });

    
    const content = popup.querySelector(".admin-settings__popup-content");
    content?.addEventListener("click", e => e.stopPropagation());
  });

  
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      closeConfirm();
      closeSuccess();
    }
  });
}
