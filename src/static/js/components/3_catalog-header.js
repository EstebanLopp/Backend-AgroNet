document.addEventListener("DOMContentLoaded", () => {
  const dropdown = document.querySelector(".catalog-header__dropdown");
  if (!dropdown) return;

  const dropdownBtn = dropdown.querySelector(".catalog-header__dropdown__button");
  const list = dropdown.querySelector(".catalog-header__dropdown__list");

  dropdownBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("show");
  });

  // Cerrar al hacer click fuera
  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove("show");
    }
  });

  // Cerrar cuando selecciona un item (si hace click en enlaces)
  list.addEventListener("click", () => {
    dropdown.classList.remove("show");
  });
});