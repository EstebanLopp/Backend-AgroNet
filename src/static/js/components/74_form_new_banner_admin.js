document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".new-banner-container");

  if (container) {
    fetch("/src/templates/components/74_form_new_banner_admin.html")
      .then(res => res.text())
      .then(html => {
        container.innerHTML = html;
      })
      .then(() => initNewBannerForm());
  }
});

function initNewBannerForm() {
  const form = document.querySelector(".form-datos__form");
  const inputFile = form.querySelector(".form-datos__file-input");
  const btnFile = form.querySelector(".form-datos__file-btn");
  const fileText = form.querySelector(".form-datos__file-text");
  const popupSuccess = document.querySelector(".popup--banner-success");

  if (!form || !inputFile || !btnFile || !fileText || !popupSuccess) return;

  // Botón para abrir el selector de archivos
  btnFile.addEventListener("click", () => inputFile.click());

  // Mostrar nombre del archivo seleccionado
  inputFile.addEventListener("change", () => {
    const fileName = inputFile.files.length
      ? inputFile.files[0].name
      : "Ningún archivo seleccionado";
    fileText.textContent = fileName;
  });

  //  Envío del formulario con popup
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      const res = await fetch("/api/banners", {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error("Error al guardar el banner");

      // Mostrar popup de éxito
      popupSuccess.classList.add("show");

    } catch (error) {
      alert("Ocurrió un error al guardar el banner");
    }
  });

  // Cerrar popup al hacer clic en el fondo o en la X
  popupSuccess.addEventListener("click", (e) => {
    if (
      e.target.classList.contains("popup") ||       // clic en el fondo
      e.target.closest(".popup__close")            // clic en la X
    ) {
      popupSuccess.classList.remove("show");

      // Redirigir después de cerrar el popup
      window.location.href = "/src/templates/admin-pages/banners.html";
    }
  });
}
