document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".seller-form-container");
  if (container) {
    fetch("/src/templates/components/36_seller_form.html")
      .then(response => response.text())
      .then(data => {
        container.innerHTML = data;

        // Seleccionar el formulario con BEM 
        const form = container.querySelector(".seller-form__form");

        // Modal BEM
        const modal = container.querySelector(".seller-form__modal");
        const closeBtn = container.querySelector(".seller-form__modal-close");
        const modalContent = container.querySelector(".seller-form__modal-content");

        // Mostrar modal al enviar formulario
        form.addEventListener("submit", (e) => {
          e.preventDefault();
          modal.classList.add("seller-form__modal--visible");
        });

        // Cerrar modal al hacer clic en la X
        closeBtn.addEventListener("click", () => {
          modal.classList.remove("seller-form__modal--visible");
        });

        // Cerrar modal haciendo clic fuera del contenido
        modal.addEventListener("click", (e) => {
          if (e.target === modal) {
            modal.classList.remove("seller-form__modal--visible");
          }
        });

        // Redirigir al hacer clic en el contenido
        modalContent.addEventListener("click", () => {
          modal.classList.remove("seller-form__modal--visible");
          window.location.href = "/src/templates/pages-general/profile_store.html";
        });

      })
      .catch(error => console.error("Error al cargar el formulario de vendedor:", error));
  }
});
