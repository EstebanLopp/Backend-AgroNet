document.addEventListener("DOMContentLoaded", function () {
  const heroElement = document.querySelector(".report__profile");

  // Si NO existe, nada funciona → por eso falla
  if (!heroElement) {
    console.warn("No se encontró .report__profile, inserta este contenedor en tu HTML");
    return;
  }

  fetch("/src/templates/components/38_generate_report.html")
    .then(response => response.text())
    .then(html => {
      heroElement.innerHTML = html;

      setTimeout(() => {
        const form = document.querySelector(".report__form");
        const popup = document.querySelector(".report__popup");
        const popupCancel = document.querySelector(".report__popup-btn--cancel");
        const popupAccept = document.querySelector(".report__popup-btn--accept");

        const modal = document.querySelector(".report__modal");
        const modalClose = document.querySelector(".report__modal-close");

        if (!form) return;

        form.addEventListener("submit", (e) => {
          e.preventDefault();
          popup.classList.add("report__popup--active");
        });

        popupCancel.addEventListener("click", () => {
          popup.classList.remove("report__popup--active");
        });

        popupAccept.addEventListener("click", () => {
          popup.classList.remove("report__popup--active");
          modal.classList.add("report__modal--active");
        });

        modalClose.addEventListener("click", () => {
          modal.classList.remove("report__modal--active");
          window.location.href = "/src/templates/customer-pages/generate_report.html";
        });

        popup.addEventListener("click", (e) => {
          if (e.target === popup) popup.classList.remove("report__popup--active");
        });

        modal.addEventListener("click", (e) => {
          if (e.target === modal) {
            modal.classList.remove("report__modal--active");
            window.location.href = "/src/templates/customer-pages/generate_report.html";
          }
        });

      }, 100);
    })
    .catch(error => console.log("Error al cargar el reporte:", error));
});
