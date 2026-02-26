document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-category");

  if (container) {
    fetch("/src/templates/components/72_form_new_category_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        // Seleccionamos el formulario y el popup usando clases BEM
        const form = container.querySelector(".form-datos__form");
        const popup = container.querySelector(".popup--success-category");

        form.addEventListener("submit", (e) => {
          e.preventDefault();
          popup.classList.add("show");
        });

        // Cerrar popup y redirigir
        popup.addEventListener("click", (e) => {
          // Cerrar si clic en fondo o en botón de cerrar
          if (
            e.target.classList.contains("popup") || 
            e.target.closest(".popup__close")
          ) {
            popup.classList.remove("show");
            // Redirigir después de cerrar
            window.location.href = "/src/templates/admin-pages/categories.html";
          }
        });
      });
  }
});
