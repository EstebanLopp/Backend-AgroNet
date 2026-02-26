document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-order");

  if (container) {
    fetch("/src/templates/components/71_form_new_order_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        // Seleccionar el formulario y el popup con clases (no IDs)
        const form = container.querySelector(".form-datos__form");
        const popupSuccess = container.querySelector(".popup--success");

        if (form && popupSuccess) {
          // Mostrar el popup al enviar el formulario
          form.addEventListener("submit", (e) => {
            e.preventDefault(); // Evita la recarga
            popupSuccess.classList.add("show"); // Muestra el popup
          });

          // Cerrar el popup al hacer clic en X, fuera o dentro del contenido
          popupSuccess.addEventListener("click", (e) => {
            if (
              e.target.classList.contains("popup__close") || // Botón X
              e.target === popupSuccess // Fondo del popup
            ) {
              popupSuccess.classList.remove("show");

              //Redirigir después de cerrar (opcional)
              window.location.href = "/src/templates/admin-pages/orders.html";
            }
          });
        }
      })
      .catch(err => console.error("Error al cargar el componente:", err));
  }
});
