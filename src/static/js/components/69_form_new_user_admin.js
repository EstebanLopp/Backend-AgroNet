document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-datos");

  if (container) {
    fetch("/src/templates/components/69_form_new_user_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        // Seleccionamos los elementos correctos
        const form = container.querySelector(".form-datos__form");
        const popup = container.querySelector(".popup");
        const closeBtn = container.querySelector(".popup__close");

        if (form && popup) {
          // Mostrar popup al enviar formulario
          form.addEventListener("submit", (e) => {
            e.preventDefault();
            popup.classList.add("popup--visible"); // Clase para mostrar
          });

          // Cerrar popup al hacer clic en la X
          if (closeBtn) {
            closeBtn.addEventListener("click", () => {
              popup.classList.remove("popup--visible");
              window.location.href = "/src/templates/admin-pages/users.html";
            });
          }

          // Cerrar popup al hacer clic fuera del contenido
          popup.addEventListener("click", (e) => {
            if (e.target === popup) {
              popup.classList.remove("popup--visible");
              window.location.href = "/src/templates/admin-pages/users.html";
            }
          });
        }
      })
      .catch(err => console.error("Error cargando el componente:", err));
  }
});
