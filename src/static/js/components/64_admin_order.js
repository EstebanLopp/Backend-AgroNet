document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".admin-orders");

  try {
    const res = await fetch("/src/templates/components/64_admin_order.html");
    if (!res.ok) throw new Error("Error al cargar el componente de pedidos");

    const html = await res.text();
    container.innerHTML = html;

    //Elementos principales
    const tableBody = container.querySelector(".admin-orders__body");
    const modal = container.querySelector(".admin-orders__modal");
    const modalBody = modal.querySelector(".admin-orders__modal-body");
    const closeModal = modal.querySelector(".admin-orders__btn--close");
    const searchInput = container.querySelector(".admin-orders__search");

    const confirmPopup = container.querySelector(".popup--confirm");
    const successPopup = container.querySelector(".popup--success");

    // Datos de ejemplo
    const orders = [
      { id: 1001, cliente: "Juan Pérez", fecha: "2025-10-25", estado: "Pendiente", total: 45000, pago: "Efectivo", direccion: "Calle 10 #15-30" },
      { id: 1002, cliente: "María Gómez", fecha: "2025-10-20", estado: "Enviado", total: 82000, pago: "Tarjeta", direccion: "Cra 5 #25-10" },
      { id: 1003, cliente: "Andrés Ruiz", fecha: "2025-10-18", estado: "Entregado", total: 23000, pago: "Transferencia", direccion: "Av 3 #40-22" },
      { id: 1004, cliente: "Sofía Martínez", fecha: "2025-10-15", estado: "Cancelado", total: 18000, pago: "Efectivo", direccion: "Cl 8 #12-20" },
      { id: 1004, cliente: "Sofía Martínez", fecha: "2025-10-15", estado: "Cancelado", total: 18000, pago: "Efectivo", direccion: "Cl 8 #12-20" },
      { id: 1004, cliente: "Sofía Martínez", fecha: "2025-10-15", estado: "Cancelado", total: 18000, pago: "Efectivo", direccion: "Cl 8 #12-20" },
      { id: 1004, cliente: "Sofía Martínez", fecha: "2025-10-15", estado: "Cancelado", total: 18000, pago: "Efectivo", direccion: "Cl 8 #12-20" },
    ];

    //Renderizar tabla
    function renderOrders(list) {
      tableBody.innerHTML = "";
      list.forEach((order, i) => {
        const row = `
          <tr class="admin-orders__row">
            <td class="admin-orders__cell">${order.id}</td>
            <td class="admin-orders__cell">${order.cliente}</td>
            <td class="admin-orders__cell">${order.fecha}</td>
            <td class="admin-orders__cell">${order.estado}</td>
            <td class="admin-orders__cell">$${order.total.toLocaleString()}</td>
            <td class="admin-orders__cell">${order.pago}</td>
            <td class="admin-orders__cell">${order.direccion}</td>
            <td class="admin-orders__cell">
              <div class="admin-orders__actions-btns">
                <button class="admin-orders__btn admin-orders__btn--view" data-index="${i}">
                  <i class="fa-solid fa-eye"></i>
                </button>
                <a href="/src/templates/admin-pages/form_edit_order.html" class="admin-orders__btn admin-orders__btn--edit" data-index="${i}">
                  <i class="fa-solid fa-pen"></i>
                </a>
                <button class="admin-orders__btn admin-orders__btn--delete" data-index="${i}">
                  <i class="fa-solid fa-xmark"></i>
                </button>
              </div>
            </td>
          </tr>
        `;
        tableBody.insertAdjacentHTML("beforeend", row);
      });
    }

    renderOrders(orders);

    // Filtro de búsqueda
    searchInput.addEventListener("input", (e) => {
      const value = e.target.value.toLowerCase();
      const filtered = orders.filter(o =>
        o.cliente.toLowerCase().includes(value) ||
        o.estado.toLowerCase().includes(value) ||
        o.pago.toLowerCase().includes(value)
      );
      renderOrders(filtered);
    });

    // Acciones de la tabla (ver y eliminar)
    tableBody.addEventListener("click", (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;
      const index = btn.dataset.index;
      const order = orders[index];

      // Ver detalles
      if (btn.classList.contains("admin-orders__btn--view")) {
        modalBody.innerHTML = `
          <p><strong>ID Pedido:</strong> ${order.id}</p>
          <p><strong>Cliente:</strong> ${order.cliente}</p>
          <p><strong>Fecha:</strong> ${order.fecha}</p>
          <p><strong>Estado:</strong> ${order.estado}</p>
          <p><strong>Total:</strong> $${order.total.toLocaleString()}</p>
          <p><strong>Método de pago:</strong> ${order.pago}</p>
          <p><strong>Dirección:</strong> ${order.direccion}</p>
        `;
        modal.classList.add("popup--show");
      }

      // Eliminar pedido (confirmación)
      if (btn.classList.contains("admin-orders__btn--delete")) {
        confirmPopup.classList.add("popup--show");

        const cancelBtn = confirmPopup.querySelector(".popup__btn--cancel");
        const acceptBtn = confirmPopup.querySelector(".popup__btn--accept");

        cancelBtn.onclick = () => confirmPopup.classList.remove("popup--show");
        acceptBtn.onclick = () => {
          confirmPopup.classList.remove("popup--show");
          successPopup.classList.add("popup--show");
        };
      }
    });

    // Cerrar modal
    closeModal.addEventListener("click", () => {
      modal.classList.remove("popup--show");
    });

    // Cerrar popups (confirmación y éxito)
    [confirmPopup, successPopup].forEach(popup => {
      popup.addEventListener("click", (e) => {
        const closeBtn = e.target.closest(".popup__close");
        if (e.target === popup || closeBtn) {
          popup.classList.remove("popup--show");
        }
      });
    });

  } catch (err) {
    console.error("Error al cargar pedidos:", err);
  }
});
