document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-edit-order");

  if (container) {
    fetch("/src/templates/components/77_form_edit_order_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;
        setTimeout(() => initEditOrderPopups(), 100);
      })
      .catch(err => console.error("Error al cargar el formulario:", err));
  }
});

function initEditOrderPopups() {
  const form = document.querySelector(".form-datos__form");
  const confirmPopup = document.querySelector(".confirm_edit_popup");
  const successPopup = document.querySelector(".edit_success_popup");

  if (!form || !confirmPopup || !successPopup) {
    console.warn("No se encontraron los elementos del formulario o popups.");
    return;
  }

  const confirmAccept = confirmPopup.querySelector(".popup__btn--accept");
  const confirmCancel = confirmPopup.querySelector(".popup__btn--cancel");
  const confirmClose = confirmPopup.querySelector(".close-popup");
  const successClose = successPopup.querySelector(".close-popup");

  
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    confirmPopup.classList.add("show");
  });

  
  [confirmCancel, confirmClose].forEach(btn => {
    btn.addEventListener("click", () => confirmPopup.classList.remove("show"));
  });

  
  confirmAccept.addEventListener("click", () => {
    confirmPopup.classList.remove("show");
    successPopup.classList.add("show");
  });

  
  function closeSuccessAndRedirect() {
    successPopup.classList.remove("show");
    window.location.href = "/src/templates/admin-pages/orders.html";
  }

  
  successClose.addEventListener("click", closeSuccessAndRedirect);

  
  window.addEventListener("click", (e) => {
    if (e.target === confirmPopup) confirmPopup.classList.remove("show");
    if (e.target === successPopup) closeSuccessAndRedirect();
  });

  
  successPopup.addEventListener("click", closeSuccessAndRedirect);
}
