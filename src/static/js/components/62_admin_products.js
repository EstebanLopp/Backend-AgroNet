document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".products-admin");

  try {
    const response = await fetch("/src/templates/components/62_admin_products.html");
    if (!response.ok) throw new Error("No se pudo cargar el componente de productos");

    const html = await response.text();
    container.innerHTML = html;

    const tableBody = document.querySelector(".products-admin__table-body");
    const modal = document.querySelector(".products-admin__modal");
    const modalBody = modal.querySelector(".products-admin__modal-body");
    const closeModal = modal.querySelector(".products-admin__btn--close");
    const searchInput = document.querySelector(".products-admin__search");

    // Popups
    const popupConfirm = document.querySelector(".popup--confirm");
    const popupSuccess = document.querySelector(".popup--success");

    const products = [
      { usuario: "jperez", nombre: "Tomate Chonto", categoria: "Verdura", precio: 2500, valor_unitario: 2500, stock: 120, descripcion: "Tomates frescos de alta calidad", unidad_peso: "kg", peso: 1, tipo_envio: "Normal" },
      { usuario: "mgomez", nombre: "Leche Entera", categoria: "Lácteos", precio: 4500, valor_unitario: 4500, stock: 85, descripcion: "Leche entera pasteurizada 1L", unidad_peso: "L", peso: 1, tipo_envio: "Refrigerado" },
      { usuario: "aruiz", nombre: "Café Supremo", categoria: "Bebida", precio: 18000, valor_unitario: 9000, stock: 40, descripcion: "Café colombiano premium", unidad_peso: "g", peso: 500, tipo_envio: "Normal" },
      { usuario: "aruiz", nombre: "Café Supremo", categoria: "Bebida", precio: 18000, valor_unitario: 9000, stock: 40, descripcion: "Café colombiano premium", unidad_peso: "g", peso: 500, tipo_envio: "Normal" },
      { usuario: "aruiz", nombre: "Café Supremo", categoria: "Bebida", precio: 18000, valor_unitario: 9000, stock: 40, descripcion: "Café colombiano premium", unidad_peso: "g", peso: 500, tipo_envio: "Normal" },
      { usuario: "aruiz", nombre: "Café Supremo", categoria: "Bebida", precio: 18000, valor_unitario: 9000, stock: 40, descripcion: "Café colombiano premium", unidad_peso: "g", peso: 500, tipo_envio: "Normal" },
      { usuario: "vtorres", nombre: "Papa Criolla", categoria: "Verdura", precio: 2000, valor_unitario: 2000, stock: 150, descripcion: "Papa criolla amarilla", unidad_peso: "kg", peso: 1, tipo_envio: "Normal" }
    ];

    function renderProducts(list) {
      tableBody.innerHTML = "";
      list.forEach((p, i) => {
        tableBody.insertAdjacentHTML(
          "beforeend",
          `
            <tr>
              <td>${p.usuario}</td>
              <td>${p.nombre}</td>
              <td>${p.categoria}</td>
              <td>$${p.precio.toLocaleString()}</td>
              <td>$${p.valor_unitario.toLocaleString()}</td>
              <td>${p.stock}</td>
              <td>${p.descripcion}</td>
              <td>${p.unidad_peso}</td>
              <td>${p.peso}</td>
              <td>${p.tipo_envio}</td>
              <td>
                <div class="products-admin__table-actions">
                  <button class="products-admin__btn products-admin__btn--view" data-index="${i}">
                    <i class="fa-solid fa-eye"></i>
                  </button>
                  <a href="/src/templates/admin-pages/form_edit_product.html" class="products-admin__btn products-admin__btn--edit" data-index="${i}">
                    <i class="fa-solid fa-pen"></i>
                  </a>
                  <button class="products-admin__btn products-admin__btn--delete" data-index="${i}">
                    <i class="fa-solid fa-xmark"></i>
                  </button>
                </div>
              </td>
            </tr>`
        );
      });
    }

    renderProducts(products);

    searchInput.addEventListener("input", (e) => {
      const value = e.target.value.toLowerCase();
      const filtered = products.filter(p =>
        p.usuario.toLowerCase().includes(value) ||
        p.nombre.toLowerCase().includes(value) ||
        p.categoria.toLowerCase().includes(value) ||
        p.descripcion.toLowerCase().includes(value)
      );
      renderProducts(filtered);
    });

    tableBody.addEventListener("click", (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;
      const index = btn.dataset.index;
      const product = products[index];

      if (btn.classList.contains("products-admin__btn--view")) {
        modalBody.innerHTML = `
          <p><strong>Usuario:</strong> ${product.usuario}</p>
          <p><strong>Nombre:</strong> ${product.nombre}</p>
          <p><strong>Categoría:</strong> ${product.categoria}</p>
          <p><strong>Precio:</strong> $${product.precio.toLocaleString()}</p>
          <p><strong>Valor unitario:</strong> $${product.valor_unitario.toLocaleString()}</p>
          <p><strong>Stock:</strong> ${product.stock}</p>
          <p><strong>Descripción:</strong> ${product.descripcion}</p>
          <p><strong>Unidad de peso:</strong> ${product.unidad_peso}</p>
          <p><strong>Peso:</strong> ${product.peso}</p>
          <p><strong>Tipo de envío:</strong> ${product.tipo_envio}</p>
        `;
        modal.style.display = "flex";
      }

      if (btn.classList.contains("products-admin__btn--delete")) {
        popupConfirm.classList.add("show");
        popupConfirm.dataset.index = index;
      }
    });

    closeModal.addEventListener("click", () => (modal.style.display = "none"));

    popupConfirm.addEventListener("click", (e) => {
      if (e.target.classList.contains("popup__close") || e.target.classList.contains("popup__btn--cancel")) {
        popupConfirm.classList.remove("show");
      }

      if (e.target.classList.contains("popup__btn--accept")) {
        const index = popupConfirm.dataset.index;
        products.splice(index, 1);
        renderProducts(products);
        popupConfirm.classList.remove("show");
        popupSuccess.classList.add("show");
      }
    });

    popupSuccess.addEventListener("click", (e) => {
      if (e.target.classList.contains("popup__close") || e.target === popupSuccess) {
        popupSuccess.classList.remove("show");
      }
    });

  } catch (error) {
    console.error("Error al cargar productos:", error);
  }
});
