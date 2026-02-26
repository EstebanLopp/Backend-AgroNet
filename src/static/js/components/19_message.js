document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("mensaje-form__form");
  const modal = document.getElementById("modal-contact");

  if (!form || !modal) {
    console.error("No se encontró el formulario o el modal en el DOM");
    return;
  }

  const closeBtn = modal.querySelector(".close1");
  const okIcon = modal.querySelector(".ok");

  // Mostrar modal al enviar formulario
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    modal.classList.add("active");
  });

  function cerrarModal() {
    modal.classList.remove("active");
    form.reset();
  }

  closeBtn.addEventListener("click", cerrarModal);
  okIcon.addEventListener("click", cerrarModal);

  // Cerrar al hacer click fuera del contenido
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      cerrarModal();
    }
  });
});