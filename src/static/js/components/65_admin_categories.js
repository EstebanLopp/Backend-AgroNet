document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".admin-categories");

  try {
    const response = await fetch("/src/templates/components/65_admin_categories.html");
    if (!response.ok) throw new Error("No se pudo cargar el componente de categorías");

    const html = await response.text();
    container.innerHTML = html;

    const tableBody = container.querySelector(".admin-categories__body");
    const modal = container.querySelector(".admin-categories__modal");
    const modalBody = modal ? modal.querySelector(".admin-categories__modal-body") : null;
    const closeModal = modal ? modal.querySelector(".admin-categories__btn--close") : null;
    const searchInput = container.querySelector(".admin-categories__search");

    
    const popupConfirm = container.querySelector(".admin-categories__popup--confirm");
    const popupSuccess = container.querySelector(".admin-categories__popup--success");
    const popupCloseBtns = container.querySelectorAll(".admin-categories__popup-close");
    const popupCancelBtn = popupConfirm ? popupConfirm.querySelector(".admin-categories__popup-btn--cancel") : null;
    const popupAcceptBtn = popupConfirm ? popupConfirm.querySelector(".admin-categories__popup-btn--accept") : null;

    
    const categories = [
      { nombre: "Animal", descripcion: "Productos derivados de animales", productos: 8 },
      { nombre: "Granos", descripcion: "Legumbres, cereales y semillas naturales", productos: 12 },
      { nombre: "Verduras", descripcion: "Hortalizas frescas y saludables", productos: 15 },
      { nombre: "Frutas", descripcion: "Frutas nacionales y tropicales", productos: 20 },
    ];

    
    let pendingDeleteIndex = null;

    
    function renderCategories(list) {
      tableBody.innerHTML = "";
      list.forEach((cat, i) => {
        const row = `
          <tr>
            <td>${cat.nombre}</td>
            <td>${cat.descripcion}</td>
            <td>${cat.productos}</td>
            <td>
              <div class="admin-categories__actions-btns">
                <button class="admin-categories__btn admin-categories__btn--view" data-index="${i}">
                  <i class="fa-solid fa-eye"></i>
                </button>
                <a href="/src/templates/admin-pages/form_edit_category.html" 
                   class="admin-categories__btn admin-categories__btn--edit" data-index="${i}">
                  <i class="fa-solid fa-pen"></i>
                </a>
                <button class="admin-categories__btn admin-categories__btn--delete" data-index="${i}">
                  <i class="fa-solid fa-xmark"></i>
                </button>
              </div>
            </td>
          </tr>
        `;
        tableBody.insertAdjacentHTML("beforeend", row);
      });
    }

    renderCategories(categories);

    
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const value = e.target.value.toLowerCase();
        const filtered = categories.filter(c =>
          c.nombre.toLowerCase().includes(value) ||
          c.descripcion.toLowerCase().includes(value)
        );
        renderCategories(filtered);
      });
    }

    
    tableBody.addEventListener("click", (e) => {
      const btn = e.target.closest("button, a");
      if (!btn) return;

      const index = btn.dataset.index;
      
      const category = (typeof index !== "undefined") ? categories[index] : null;

      
      if (btn.classList.contains("admin-categories__btn--view") && category && modalBody && modal) {
        modalBody.innerHTML = `
          <p><strong>Nombre:</strong> ${category.nombre}</p>
          <p><strong>Descripción:</strong> ${category.descripcion}</p>
          <p><strong>Cantidad de productos:</strong> ${category.productos}</p>
        `;
        modal.classList.add("admin-categories__modal--show"); 
      }

      
      if (btn.classList.contains("admin-categories__btn--edit") && category) {
        
      }

      // Eliminar -> abrir popup de confirmación
      if (btn.classList.contains("admin-categories__btn--delete")) {
        pendingDeleteIndex = parseInt(btn.dataset.index, 10);
        if (popupConfirm) popupConfirm.classList.add("show");
      }
    });

    
    if (closeModal && modal) {
      closeModal.addEventListener("click", () => modal.classList.remove("admin-categories__modal--show"));
      
      modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.remove("admin-categories__modal--show");
      });
    }

    
    popupCloseBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        if (popupConfirm) popupConfirm.classList.remove("show");
        if (popupSuccess) popupSuccess.classList.remove("show");
      });
    });

    
    if (popupCancelBtn) {
      popupCancelBtn.addEventListener("click", () => {
        if (popupConfirm) popupConfirm.classList.remove("show");
        pendingDeleteIndex = null;
      });
    }

    
    if (popupAcceptBtn) {
      popupAcceptBtn.addEventListener("click", () => {
        if (pendingDeleteIndex !== null && Number.isInteger(pendingDeleteIndex)) {
          
          categories.splice(pendingDeleteIndex, 1);
          renderCategories(categories);
          pendingDeleteIndex = null;
        }
        if (popupConfirm) popupConfirm.classList.remove("show");
        if (popupSuccess) popupSuccess.classList.add("show");
      });
    }

    
    if (popupSuccess) {
      popupSuccess.addEventListener("click", (e) => {
        if (e.target === popupSuccess || e.target.closest(".admin-categories__popup-close")) {
          popupSuccess.classList.remove("show");
        }
      });
    }

    
    if (popupConfirm) {
      popupConfirm.addEventListener("click", (e) => {
        if (e.target === popupConfirm) {
          popupConfirm.classList.remove("show");
          pendingDeleteIndex = null;
        }
      });
    }

  } catch (error) {
    console.error("Error al cargar el componente de categorías:", error);
  }
});
