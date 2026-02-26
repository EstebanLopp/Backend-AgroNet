document.addEventListener("DOMContentLoaded", function () {

  const heroElement = document.querySelector(".recover-container");
  if (!heroElement) return;

  initRecoverForm(heroElement);

});


function initRecoverForm(scope) {

  const form = scope.querySelector(".recover__form");
  const popup = scope.querySelector(".recover-popup");

  if (!form || !popup) return;

  const closeBtn = popup.querySelector(".recover-popup__close");

  // Abrir popup
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    setTimeout(() => {
      popup.classList.add("show");
    }, 200);
  });

  // Cerrar popup
  popup.addEventListener("click", (e) => {

    const clickedOverlay = e.target.classList.contains("recover-popup");
    const clickedClose = e.target.closest(".recover-popup__close");

    if (clickedOverlay || clickedClose) {

      popup.classList.remove("show");

      setTimeout(() => {
        window.location.href = "/token-forgot-password/";
      }, 250);

    }

  });

}