document.addEventListener("DOMContentLoaded", async () => {
  const containerPage = document.querySelector(".disabled-product-container");

  if (containerPage) {
    try {
      const response = await fetch("/src/templates/components/42_disabled_products.html");
      const data = await response.text();

      containerPage.insertAdjacentHTML("beforeend", data);

      await loadDisabledProducts();
    } catch (error) {
      console.error("Error al cargar componente:", error);
    }
  }
});

async function loadDisabledProducts() {

  const container = document.querySelector(".disabled_product_container");
  const template = document.querySelector(".disabled_product__template");

  if (!container || !template) {
    console.error("No se encontraron el contenedor o el template");
    return;
  }

  try {
    const res = await fetch("/src/static/data/disabled_products.json");
    const productos = await res.json();

    productos.forEach((producto) => {

      const clone = template.content.cloneNode(true);

      clone.querySelector(".disabled-product__image").src = producto.imagen;
      clone.querySelector(".disabled-product__name").textContent = `Nombre del Producto: ${producto.nombre}`;
      clone.querySelector(".disabled-product__price").textContent = `Precio: ${producto.precio}`;
      clone.querySelector(".disabled-product__type").textContent = `Tipo de producto: ${producto.tipo}`;

      const boton = clone.querySelector(".disabled-product__btn");

      boton.addEventListener("click", () => {
        const modal = document.querySelector(".disabled-product__modal");
        const closeBtn = modal.querySelector(".disabled-product__modal-close");

        modal.style.display = "flex";

        const closeModal = (e) => {
          if (e.target === modal || e.target === closeBtn || closeBtn.contains(e.target)) {
            modal.style.display = "none";
            modal.removeEventListener("click", closeModal);
            closeBtn.removeEventListener("click", closeModal);
          }
        };

        closeBtn.addEventListener("click", closeModal);
        modal.addEventListener("click", closeModal);
      });

      container.appendChild(clone);
    });

  } catch (err) {
    console.error("Error al cargar los productos:", err);
  }
}
