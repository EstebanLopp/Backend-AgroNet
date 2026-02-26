document.addEventListener("DOMContentLoaded", () => {

  const container = document.querySelector(".new-password-container");
  if (!container) return;

  initNewPasswordHandlers(container);

});


function initNewPasswordHandlers(scope) {

  const form = scope.querySelector(".new-password__form");
  const inputs = scope.querySelectorAll(".new-password__input");
  const toggles = scope.querySelectorAll(".new-password__toggle");
  const popup = scope.querySelector(".popup--password-success");

  if (!form || inputs.length < 2 || !popup) return;

  const passwordInput = inputs[0];
  const confirmInput = inputs[1];

  /* -------------------------
     Toggle visibilidad password
  ------------------------- */
  toggles.forEach((toggle) => {

    toggle.addEventListener("click", () => {

      const input = toggle.previousElementSibling;
      const icon = toggle.querySelector("i");

      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye", "fa-eye-slash");
      } else {
        input.type = "password";
        icon.classList.replace("fa-eye-slash", "fa-eye");
      }

    });

  });


  /* -------------------------
     Validación formulario
  ------------------------- */
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const password = passwordInput.value.trim();
    const confirm = confirmInput.value.trim();

    if (password.length < 6) {
      alert("La contraseña debe tener al menos 6 caracteres.");
      return;
    }

    if (password !== confirm) {
      alert("Las contraseñas no coinciden.");
      return;
    }

    popup.classList.add("show");
  });


  /* -------------------------
     Cerrar popup
  ------------------------- */
  popup.addEventListener("click", (e) => {

    const clickedOverlay = e.target.classList.contains("popup");
    const clickedClose = e.target.closest(".popup__close");

    if (clickedOverlay || clickedClose) {
      popup.classList.remove("show");

      // Ruta Django real
      window.location.href = "/login/";
    }

  });

}