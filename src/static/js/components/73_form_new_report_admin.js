document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-report");

  if (container) {
    fetch("/src/templates/components/73_form_new_report_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        // Seleccionamos el formulario y el popup usando clases BEM
        const form = container.querySelector(".form-datos__form");
        const popupSuccess = container.querySelector(".popup--report-success");

        if (form && popupSuccess) {
          // Mostrar popup al enviar el formulario
          form.addEventListener("submit", (e) => {
            e.preventDefault(); // Evita el envío real
            popupSuccess.classList.add("show"); // Muestra el popup
          });

          // Cerrar popup al hacer clic en el fondo o en la X
          popupSuccess.addEventListener("click", (e) => {
            if (
              e.target.classList.contains("popup") ||       // clic en el fondo
              e.target.closest(".popup__close")            // clic en la X
            ) {
              popupSuccess.classList.remove("show");

              // Redirigir después de cerrar
              window.location.href = "/src/templates/admin-pages/reports.html";
            }
          });
        }
      });
  }
});
