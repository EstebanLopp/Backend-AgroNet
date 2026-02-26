document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".catalog-header-container");

  if (!container) return;

  try {
    const response = await fetch("/static/data/categories.json");
    if (!response.ok) throw new Error("Error al cargar categorías");

    const categories = await response.json();
    const itemsHTML = categories
      .map(cat => `<li class="catalog-header__dropdown__item">${cat}</li>`)
      .join("");

    container.innerHTML = `
      <div class="catalog-header__dropdown">
        <button class="catalog-header__dropdown__button">
          <span class="catalog-header__dropdown__text"><em>Categoría</em></span>
          <i class="fa-solid fa-chevron-down catalog-header__dropdown__icon"></i>
        </button>
        <ul class="catalog-header__dropdown__list">
          ${itemsHTML}
        </ul>
      </div>
    `;

    const dropdown = container.querySelector(".catalog-header__dropdown");
    const dropdownBtn = dropdown.querySelector(".catalog-header__dropdown__button");
    const items = dropdown.querySelectorAll(".catalog-header__dropdown__item");

    // Mostrar / ocultar lista
    dropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation(); // evita cerrar inmediatamente por el click global
      dropdown.classList.toggle("show");
    });

    // Cerrar cuando selecciona un item
    items.forEach(item => {
      item.addEventListener("click", () => {
        dropdown.classList.remove("show");
      });
    });

    // Cerrar si hace clic fuera
    document.addEventListener("click", (e) => {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("show");
      }
    });

  } catch (error) {
    console.error("Hubo un problema cargando las categorías:", error);
    container.innerHTML = `<p style="color:red">No se pudieron cargar las categorías.</p>`;
  }
});
