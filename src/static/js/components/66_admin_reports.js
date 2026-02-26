document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".admin-reports");

  try {
    const response = await fetch("/src/templates/components/66_admin_reports.html");
    if (!response.ok) throw new Error("No se pudo cargar el componente de reportes");

    const html = await response.text();
    container.innerHTML = html;

    const tableBody = document.querySelector(".admin-reports__body");
    const modal = document.querySelector(".admin-reports__modal");
    const modalBody = modal.querySelector(".admin-reports__modal-body");
    const closeModal = modal.querySelector(".admin-reports__btn--close");
    const searchInput = document.querySelector(".admin-reports__search");

    // Popups sin ID — usando clases BEM
    const popupConfirm = document.querySelector(".admin-reports__popup--confirm");
    const popupSuccess = document.querySelector(".admin-reports__popup--success");

    // Datos simulados
    const reports = [
      {
        asunto: "Problema con pedido",
        especificacion: "El pedido llegó incompleto",
        mensaje: "Faltó un producto en la entrega de ayer.",
        tipo_usuario: "Cliente",
        fecha: "2025-10-25",
        estado: "Pendiente",
      },
      {
        asunto: "Error en facturación",
        especificacion: "Monto incorrecto",
        mensaje: "El valor facturado no coincide con el pedido.",
        tipo_usuario: "Vendedor",
        fecha: "2025-10-24",
        estado: "Pendiente",
      },
      {
        asunto: "Actualización del sistema",
        especificacion: "Reporte interno",
        mensaje: "Se implementó mejora en el módulo de productos.",
        tipo_usuario: "Administrador",
        fecha: "2025-10-23",
        estado: "Resuelto",
      },
    ];

    // Renderizar reportes
    function renderReports(list) {
      tableBody.innerHTML = "";
      list.forEach((r, i) => {
        const row = `
          <tr>
            <td>${r.asunto}</td>
            <td>${r.especificacion}</td>
            <td>${r.mensaje}</td>
            <td>${r.tipo_usuario}</td>
            <td>${r.fecha}</td>
            <td>${r.estado}</td>
            <td>
              <div class="admin-reports__actions-btns">
                <button class="admin-reports__btn admin-reports__btn--view" data-index="${i}">
                  <i class="fa-solid fa-eye"></i>
                </button>
                <button class="admin-reports__btn admin-reports__btn--resolve" data-index="${i}">
                  <i class="fa-solid fa-check"></i>
                </button>
                <button class="admin-reports__btn admin-reports__btn--delete" data-index="${i}">
                  <i class="fa-solid fa-xmark"></i>
                </button>
              </div>
            </td>
          </tr>
        `;
        tableBody.insertAdjacentHTML("beforeend", row);
      });
    }

    renderReports(reports);

    // Buscar reporte
    searchInput.addEventListener("input", (e) => {
      const value = e.target.value.toLowerCase();
      const filtered = reports.filter(
        (r) =>
          r.asunto.toLowerCase().includes(value) ||
          r.tipo_usuario.toLowerCase().includes(value) ||
          r.mensaje.toLowerCase().includes(value)
      );
      renderReports(filtered);
    });

    // Acciones de tabla
    let indexToDelete = null;

    tableBody.addEventListener("click", (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;
      const index = btn.dataset.index;
      const report = reports[index];

      if (btn.classList.contains("admin-reports__btn--view")) {
        modalBody.innerHTML = `
          <p><strong>Asunto:</strong> ${report.asunto}</p>
          <p><strong>Especificación:</strong> ${report.especificacion}</p>
          <p><strong>Mensaje:</strong> ${report.mensaje}</p>
          <p><strong>Usuario:</strong> ${report.tipo_usuario}</p>
          <p><strong>Fecha:</strong> ${report.fecha}</p>
          <p><strong>Estado:</strong> ${report.estado}</p>
        `;
        modal.classList.add("show");
      }

      if (btn.classList.contains("admin-reports__btn--resolve")) {
        report.estado = "Resuelto";
        renderReports(reports);
      }

      if (btn.classList.contains("admin-reports__btn--delete")) {
        indexToDelete = index;
        popupConfirm.classList.add("show");
      }
    });

    // Cerrar modal
    closeModal.addEventListener("click", () => modal.classList.remove("show"));

    // Cerrar popups al hacer clic fuera
    [popupConfirm, popupSuccess].forEach((popup) => {
      popup.addEventListener("click", () => popup.classList.remove("show"));
    });

    // Evitar cierre al hacer clic dentro del contenido
    document.querySelectorAll(".admin-reports__popup-content").forEach((content) => {
      content.addEventListener("click", (e) => e.stopPropagation());
    });

    // Botones de confirmación
    const btnCancel = popupConfirm.querySelector(".admin-reports__popup-btn--cancel");
    const btnAccept = popupConfirm.querySelector(".admin-reports__popup-btn--accept");

    btnCancel.addEventListener("click", () => popupConfirm.classList.remove("show"));

    btnAccept.addEventListener("click", () => {
      reports.splice(indexToDelete, 1);
      renderReports(reports);
      popupConfirm.classList.remove("show");
      popupSuccess.classList.add("show");
    });

  } catch (error) {
    console.error("Error al cargar el componente de reportes:", error);
  }
});
