document.addEventListener("DOMContentLoaded", () => {
  const confirmBtn = document.querySelector(".checkout-summary__confirm-btn--js");
  const confirmPopup = document.querySelector(".checkout-summary__popup--confirm");
  const successPopup = document.querySelector(".checkout-summary__popup--success");

  if (!confirmBtn || !confirmPopup || !successPopup) return;

  const closeConfirm = confirmPopup.querySelector(".checkout-summary__popup-close");
  const cancelBtn = confirmPopup.querySelector(".checkout-summary__btn--cancel");
  const acceptBtn = confirmPopup.querySelector(".checkout-summary__btn--accept");
  const confirmContent = confirmPopup.querySelector(".checkout-summary__popup-content");

  const closeSuccess = successPopup.querySelector(".checkout-summary__popup-close");
  const successContent = successPopup.querySelector(".checkout-summary__popup-content");

  const form = document.getElementById("checkout-confirm-form");

  // Abre popup confirmación
  confirmBtn.addEventListener("click", () => {
    confirmPopup.classList.add("checkout-summary__popup--show");
  });

  // Cerrar confirmación
  [closeConfirm, cancelBtn].forEach(btn => {
    if (!btn) return;
    btn.addEventListener("click", () => {
      confirmPopup.classList.remove("checkout-summary__popup--show");
    });
  });

  confirmPopup.addEventListener("click", e => {
    if (e.target === confirmPopup) confirmPopup.classList.remove("checkout-summary__popup--show");
  });

  if (confirmContent) confirmContent.addEventListener("click", e => e.stopPropagation());

  // Aceptar: enviar POST real (no mostramos success local, dejamos que Django redirija)
  acceptBtn.addEventListener("click", () => {
    if (!form) return;
    form.submit();
  });

  // Estos handlers quedan por si tu pantalla de éxito reutiliza el popup
  if (closeSuccess) {
    closeSuccess.addEventListener("click", () => {
      successPopup.classList.remove("checkout-summary__popup--show");
    });
  }
  if (successContent) successContent.addEventListener("click", e => e.stopPropagation());
});