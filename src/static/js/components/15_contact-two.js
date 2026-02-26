document.addEventListener("DOMContentLoaded", () => {

  const container = document.querySelector(".contact-two-container");
  if (!container) return;

  initContactTwoHandlers(container);

});


/* -----------------------
   Funciones para manejar botones
----------------------- */
function initContactTwoHandlers(scope) {

  const openBtn = scope.querySelector(".contact-two__open-maps");

  if (openBtn) {
    openBtn.addEventListener("click", (e) => {
      e.preventDefault();

      const coords = openBtn.dataset.coords || "4.836898701426531,-75.68093176016761";

      const url = `https://www.google.com/maps?q=${encodeURIComponent(coords)}`;

      window.open(url, "_blank", "noopener");
    });
  }

  const backBtn = scope.querySelector(".contact-two__back");

  if (backBtn) {
    backBtn.addEventListener("click", (e) => {
      e.preventDefault();

      if (window.history.length > 1) {
        window.history.back();
      } else {
        window.location.href = "/";
      }
    });
  }
}