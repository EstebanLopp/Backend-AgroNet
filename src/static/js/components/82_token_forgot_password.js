document.addEventListener("DOMContentLoaded", () => {

  const container = document.querySelector(".token-container");
  if (!container) return;

  initTokenHandlers(container);

});


function initTokenHandlers(scope) {

  const inputs = scope.querySelectorAll(".token__input");
  const form = scope.querySelector(".token__form");
  const resendLink = scope.querySelector(".token__resend-link");
  const popup = scope.querySelector(".popup--token-success");

  /* -------------------------
     Autoenfoque entre inputs
  ------------------------- */
  inputs.forEach((input, index) => {

    input.addEventListener("input", (e) => {
      if (e.target.value.length === 1 && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && !e.target.value && index > 0) {
        inputs[index - 1].focus();
      }
    });

  });


  /* -------------------------
     Reenviar código
  ------------------------- */
  if (resendLink && popup) {
    resendLink.addEventListener("click", (e) => {
      e.preventDefault();
      popup.classList.add("show");
    });
  }


  /* -------------------------
     Cerrar popup
  ------------------------- */
  if (popup) {
    popup.addEventListener("click", (e) => {

      const clickedOverlay = e.target.classList.contains("popup");
      const clickedClose = e.target.closest(".popup__close");

      if (clickedOverlay || clickedClose) {
        popup.classList.remove("show");
      }

    });
  }

}