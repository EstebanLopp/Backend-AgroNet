document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".store-edit-container");

  if (container) {
    fetch("/src/templates/components/60_edit_store.html")
      .then(response => response.text())
      .then(data => {
        container.innerHTML = data;
        initializeStoreModals();
      })
      .catch(error => console.error("Error loading store form:", error));
  }
});

function initializeStoreModals() {
  const form = document.querySelector(".seller-form-e__form");
  const confirmModal = document.querySelector(".seller-form-e__modal--confirm");
  const successModal = document.querySelector(".modal--success");

  const cancelBtn = confirmModal.querySelector(".seller-form-e__modal-btn--cancel");
  const acceptBtn = confirmModal.querySelector(".seller-form-e__modal-btn--accept");
  const closeConfirm = confirmModal.querySelector(".seller-form-e__modal-close--confirm");
  const closeSuccess = successModal.querySelector(".seller-form-e__modal-close--success");

  if (!form || !confirmModal || !successModal) {
    console.error("Missing modals or form in loaded HTML.");
    return;
  }

  // MOSTRAR MODAL DE CONFIRMACIÓN
  form.addEventListener("submit", (e) => {
    e.preventDefault(); 
    confirmModal.classList.add("show");
  });

  // Cerrar confirmación

  cancelBtn.addEventListener("click", () => confirmModal.classList.remove("show"));
  closeConfirm.addEventListener("click", () => confirmModal.classList.remove("show"));
  confirmModal.addEventListener("click", (e) => {
    if (e.target === confirmModal) confirmModal.classList.remove("show");
  });

  // Aceptar → Mostrar modal de éxito
  acceptBtn.addEventListener("click", () => {
    confirmModal.classList.remove("show");
    successModal.classList.add("show");
  });

  // Redirección final
  const redirectURL = "/src/templates/views/seller-pages/profile_store.html";

  const closeAndRedirect = () => {
    successModal.classList.remove("show");
    window.location.href = redirectURL;
  };

  closeSuccess.addEventListener("click", closeAndRedirect);

  successModal.addEventListener("click", (e) => {
    if (e.target === successModal) closeAndRedirect();
  });
}
