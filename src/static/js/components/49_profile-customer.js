document.addEventListener("DOMContentLoaded", () => {
  fetch("/src/templates/components/49_profile-customer.html")
    .then(response => response.text())
    .then(data => {
      const container = document.querySelector(".profile-container");
      if (!container) return;

      container.innerHTML = data;

      const addBtn = container.querySelector(".client-profile__edit-btn");
      const modal = container.querySelector(".client-profile__modal");
      const modalContent = container.querySelector(".client-profile__modal-content");
      const closeBtn = container.querySelector(".client-profile__modal-close");

      if (!addBtn || !modal || !modalContent || !closeBtn) {
        console.error("Elementos del modal no encontrados.");
        return;
      }

      // Abrir modal
      addBtn.addEventListener("click", () => {
        modal.classList.add("client-profile__modal--active");
      });

      // Cerrar modal (botón X)
      closeBtn.addEventListener("click", () => {
        cerrarModal();
      });

      // Cerrar si clic en fondo
      modal.addEventListener("click", (e) => {
        if (e.target === modal) cerrarModal();
      });

      function cerrarModal() {
        modal.classList.remove("client-profile__modal--active");
        marcarComoAgregado();
      }

      function marcarComoAgregado() {
        addBtn.textContent = "Agregado a la libreta";
        addBtn.classList.add("client-profile__edit-btn--added");
        addBtn.disabled = true;
      }
    })
    .catch(error => console.error("Error al cargar perfil del cliente:", error));
});
