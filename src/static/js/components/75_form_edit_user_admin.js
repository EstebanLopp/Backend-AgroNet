document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-edit-datos");
  if (container) {
    fetch("/src/templates/components/75_form_edit_user_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;
        setTimeout(() => initEditUserPopups(), 100);
      });
  }
});

function initEditUserPopups() {
  const form = document.querySelector(".form-datos__form");
  const confirmPopup = document.querySelector(".confirm_edit_popup");
  const successPopup = document.querySelector(".edit_success_popup");

  if (!form || !confirmPopup || !successPopup) {
    console.warn("⚠️ No se encontraron los elementos del formulario o popups.");
    return;
  }

  const confirmAccept = confirmPopup.querySelector(".popup__btn--accept");
  const confirmCancel = confirmPopup.querySelector(".popup__btn--cancel");
  const confirmClose = confirmPopup.querySelector(".close-popup");
  const successClose = successPopup.querySelector(".close-popup");

  // Mostrar popup de confirmación
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    confirmPopup.classList.add("show");
  });

  // Cerrar popup de confirmación
  [confirmCancel, confirmClose].forEach(btn => {
    btn.addEventListener("click", () => confirmPopup.classList.remove("show"));
  });

  // Confirmar → Mostrar popup de éxito
  confirmAccept.addEventListener("click", () => {
    confirmPopup.classList.remove("show");
    successPopup.classList.add("show");
  });

  // Cerrar popup de éxito manualmente y redirigir
  successClose.addEventListener("click", () => {
    successPopup.classList.remove("show");
    window.location.href = "/src/templates/admin-pages/users.html";
  });

  // Cerrar popups al hacer clic fuera
  window.addEventListener("click", (e) => {
    if (e.target === confirmPopup) confirmPopup.classList.remove("show");
    if (e.target === successPopup) {
      successPopup.classList.remove("show");
      window.location.href = "/src/templates/admin-pages/users.html";
    }
  });

  // Cerrar también si se hace clic dentro del popup
  [confirmPopup, successPopup].forEach(popup => {
    popup.addEventListener("click", () => {
      popup.classList.remove("show");
      if (popup === successPopup) {
        window.location.href = "/src/templates/admin-pages/users.html";
      }
    });
  });
}
