document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".store-profile-container");

  if (container) {
    fetch("/src/templates/components/37_profile_store.html")
      .then(response => response.text())
      .then(data => {
        container.innerHTML = data;

        // Esperar a que el DOM realmente cargue el HTML insertado
        requestAnimationFrame(() => {
          initStoreProfileModals(); // SOLO esta función
        });
      })
      .catch(error => console.error("Error loading store profile:", error));
  }
});


/* ==========================================================
   MÉTODOS DE PAGO - MODALES
=========================================================== */

function initStoreProfileModals() {
  const btnDisable = document.querySelector(".store-profile__button--disable-store");
  const modalConfirm = document.querySelector(".store-profile__modal--confirm");
  const modalSuccess = document.querySelector(".store-profile__modal--success");

  if (!btnDisable || !modalConfirm || !modalSuccess) return;

  const btnCancel = modalConfirm.querySelector(".store-profile__modal-button--cancel");
  const btnAccept = modalConfirm.querySelector(".store-profile__modal-button--accept");
  const btnCloseSuccess = modalSuccess.querySelector(".store-profile__modal-close--success");
  const btnCloseConfirm = modalConfirm.querySelector(".store-profile__modal-close");

  /* -------------------------
     Abrir modal de confirmación
  -------------------------- */
  btnDisable.addEventListener("click", () => {
    modalConfirm.classList.add("store-profile__modal--active");
  });

  /* -------------------------
     Botón cerrar en confirmación (X)
  -------------------------- */
  btnCloseConfirm.addEventListener("click", () => {
    modalConfirm.classList.remove("store-profile__modal--active");
  });

  /* -------------------------
     Cancelar confirmación
  -------------------------- */
  btnCancel.addEventListener("click", () => {
    modalConfirm.classList.remove("store-profile__modal--active");
  });

  /* -------------------------
     Aceptar → abrir modal de éxito
  -------------------------- */
  btnAccept.addEventListener("click", () => {
    modalConfirm.classList.remove("store-profile__modal--active");
    modalSuccess.classList.add("store-profile__modal--active");
  });

  /* -------------------------
     Cerrar modal de éxito
  -------------------------- */
  btnCloseSuccess.addEventListener("click", () => {
    modalSuccess.classList.remove("store-profile__modal--active");
    window.location.href = "/src/static/customer-pages/start_sales.html"; 
  });

  /* -------------------------
     Cerrar confirmación al hacer clic fuera
  -------------------------- */
  modalConfirm.addEventListener("click", (e) => {
    if (e.target === modalConfirm) {
      modalConfirm.classList.remove("store-profile__modal--active");
    }
  });

  /* -------------------------
     Cerrar éxito al hacer clic fuera
  -------------------------- */
  modalSuccess.addEventListener("click", (e) => {
    if (e.target === modalSuccess) {
      modalSuccess.classList.remove("store-profile__modal--active");
    }
  });

  /* -------------------------
     Evitar cierre al hacer clic dentro del contenido
  -------------------------- */
  modalConfirm.querySelector(".store-profile__modal-content")
    .addEventListener("click", (e) => e.stopPropagation());

  modalSuccess.querySelector(".store-profile__modal-content")
    .addEventListener("click", (e) => e.stopPropagation());
}
