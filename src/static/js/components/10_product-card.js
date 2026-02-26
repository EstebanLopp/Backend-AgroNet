document.addEventListener("DOMContentLoaded", async function () {
  const contenedor = document.getElementById("products-container");

  try {
    //  Llamada al archivo JSON con fetch
    const response = await fetch("/static/data/products.json");
    if (!response.ok) {
      throw new Error("Error al cargar los productos");
    }

    const products = await response.json(); // Convertimos a objeto JS

    // Renderizado de productos
    if (contenedor) {
      products.forEach(prod => {
        const tarjeta = document.createElement("a");
        tarjeta.classList.add("product");
        tarjeta.href = `/product/${prod.id}/`;

        tarjeta.innerHTML = `
          <img src="${prod.imagen}" alt="${prod.nombre}" class="product__image">

          <div class="product__info">
            <div class="product__details">
              <p class="product__price">${prod.precio}</p>
              <h3 class="product__name">${prod.nombre}</h3>
              <p class="product__category">${prod.categoria}</p>
            </div>

            <button class="product__btn-add" onclick="event.preventDefault()">
              <i class="fas fa-shopping-cart product__icon-cart"></i> Añadir
            </button>
          </div>
        `;

        contenedor.appendChild(tarjeta);
      });
    }
  } catch (error) {
    console.error("Hubo un problema cargando los productos:", error);
    if (contenedor) {
      contenedor.innerHTML = `<p style="color:red">No se pudieron cargar los productos.</p>`;
    }
  }
});
