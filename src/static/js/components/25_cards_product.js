document.addEventListener("DOMContentLoaded", async function () {
  const contenedor = document.getElementById("products-detail");

  try {
    // Llamada al archivo JSON
    const response = await fetch("/static/data/cards-product.json");
    if (!response.ok) {
      throw new Error("Error al cargar los productos");
    }

    const data = await response.json();

    if (contenedor) {


      // Productos similares
      if (Array.isArray(data.similares)) {
        data.similares.forEach(prod => {
          const tarjeta = document.createElement("a");
          tarjeta.classList.add("product1");
          tarjeta.href = `/product/${prod.id}/`;

          tarjeta.innerHTML = `
            <img src="${prod.imagen}" alt="${prod.nombre}" class="product1__image">

            <div class="product1__info">
              <div class="product1__details">
                <p class="product1__price">${prod.precio}</p>
                <h3 class="product1__name">${prod.nombre}</h3>
                <p class="product1__category">${prod.categoria}</p>
              </div>

              <button class="product1__btn-add" type="button">
                <i class="fas fa-shopping-cart product1__icon-cart"></i> Añadir
              </button>
            </div>

          `;

          contenedor.appendChild(tarjeta);
        });
      }
    }
  } catch (error) {
    console.error("Hubo un problema cargando los productos:", error);
    if (contenedor) {
      contenedor.innerHTML = `<p style="color:red">No se pudieron cargar los productos.</p>`;
    }
  }
});

