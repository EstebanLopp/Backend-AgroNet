class MyProducts extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: "open" });

    fetch("/src/templates/components/17_component_my_products.html")
      .then(res => res.text())
      .then(html => {
        const template = document.createElement("div");
        template.innerHTML = html;
        const content = template.querySelector("template").content.cloneNode(true);

        const styleLink = document.createElement("link");
        styleLink.setAttribute("rel", "stylesheet");
        styleLink.setAttribute("href", "/src/static/css/components/17_my_products.css");

        const faLink = document.createElement("link");
        faLink.setAttribute("rel", "stylesheet");
        faLink.setAttribute("href", "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css");

        shadow.appendChild(styleLink);
        shadow.appendChild(faLink);
        shadow.appendChild(content);

        this.renderProducts(shadow);
        this.setupDropdown(shadow);
        this.setupMenuCard(shadow);
        this.setupPopups(shadow);
        this.setupDetailsPopup(shadow);
      });
  }

  /* =============== RENDERIZAR PRODUCTOS =============== */
  renderProducts(shadow) {
    const products = [
      { name: "Manzana Gala", price: "$20 por kg", type: "fruta", stock: "24kg", image: "/src/static/assets/manzanagala.jpg" },
      { name: "Banano", price: "$20 por kg", type: "fruta", stock: "24kg", image: "/src/static/assets/huevos.jpg" },
      { name: "Banano", price: "$20 por kg", type: "fruta", stock: "24kg", image: "/src/static/assets/cebolla_larga.jpg" },
      { name: "Banano", price: "$20 por kg", type: "fruta", stock: "24kg", image: "/src/static/assets/lechuga.jpg"},
      { name: "Banano", price: "$20 por kg", type: "fruta", stock: "24kg", image: "/src/static/assets/papa.jpg" },
      { name: "Banano", price: "$20 por kg", type: "fruta", stock: "24kg", image: "/src/static/assets/platano.webp" },
      { name: "Banano", price: "$20 por kg", type: "fruta", stock: "24kg", image: "/src/static/assets/cafe.jpg" },
      { name: "Naranja", price: "$1.390 por und", type: "fruta", stock: "24kg", image: "/src/static/assets/banano.webp" }
    ];

    const container = shadow.querySelector(".my-products__grid");

    products.forEach((p, index) => {
      const card = document.createElement("article");
      card.classList.add("my-products__card");

      const checkboxId = `checkboxInput-${index}`;

      card.innerHTML = `
        <div class="my-products__menu-card">
          <button class="my-products__menu-card-toggle">
            <i class="fa-solid fa-ellipsis-vertical"></i>
          </button>
          <ul class="my-products__menu-card-options">
            <li class="my-products__menu-card-item" data-action="publish">Publicar</li>
            <li class="my-products__menu-card-item" data-action="edit">Editar</li>
            <li class="my-products__menu-card-item" data-action="view">Visualizar</li>
            <li class="my-products__menu-card-item" data-action="details">Ver detalles</li>
            <li class="my-products__menu-card-item" data-action="disable">Deshabilitar</li>
          </ul>
        </div>

        <img class="my-products__card-img" src="${p.image}" alt="${p.name}">
        <div class="my-products__card-info">
          <h3 class="my-products__card-name">Nombre del Producto: ${p.name}</h3>
          <p class="my-products__card-price">Precio: ${p.price}</p>
          <p class="my-products__card-type">Tipo de producto: <span>${p.type}</span></p>
          <p class="my-products__card-stock">Stock: <span>${p.stock}</span></p>

          <div class="my-products__card-toggle">
            <input type="checkbox" id="${checkboxId}">
            <label for="${checkboxId}" class="my-products__card-toggleSwitch"></label>
          </div>
        </div>
      `;

      container.appendChild(card);
    });
  }

  /* =============== DROPDOWN =============== */
  setupDropdown(shadow) {
    const toggle = shadow.querySelector(".my-products__dropdown-toggle");
    const menu = shadow.querySelector(".my-products__dropdown-menu");

    toggle.addEventListener("click", () => menu.classList.toggle("show"));

    shadow.addEventListener("click", e => {
      const inside = e.composedPath().includes(toggle);
      if (!inside) menu.classList.remove("show");
    });
  }

  /* =============== MENÚ DE CADA CARD =============== */
  setupMenuCard(shadow) {
    shadow.addEventListener("click", e => {
      const toggleBtn = e.composedPath().find(el => 
        el?.classList?.contains("my-products__menu-card-toggle")
      );

      const menus = shadow.querySelectorAll(".my-products__menu-card-options");

      if (toggleBtn) {
        const menu = toggleBtn.nextElementSibling;
        menus.forEach(m => m !== menu && m.classList.remove("show"));
        menu.classList.toggle("show");
      }

      const actionItem = e.composedPath().find(el =>
        el?.classList?.contains("my-products__menu-card-item")
      );

      if (!actionItem) return;

      const action = actionItem.dataset.action;
      const card = actionItem.closest(".my-products__card");

      menus.forEach(m => m.classList.remove("show"));

      if (action === "edit") {
        window.location.href = "/src/templates/seller-pages/edit_product.html";
      }

      if (action === "view") {
        window.location.href = "/src/templates/seller-pages/product_seller.html";
      }

      if (action === "publish") {
        this.showPopup(shadow, ".my-products__popup--publish-success");
      }

      if (action === "disable") {
        this.showPopup(shadow, ".my-products__popup--confirm-disable");
      }

      if (action === "details") {
        this.openDetailsPopup(shadow, card);
      }
    });
  }

  /* ============================================================
                     POPUPS GENERALES
  ============================================================ */
  setupPopups(shadow) {
    shadow.querySelectorAll(".my-products__popup").forEach(popup => {
      popup.addEventListener("click", e => {
        if (e.target.classList.contains("my-products__popup")) {
          popup.classList.remove("show");
        }
      });

      const close = popup.querySelector(".my-products__popup-close");
      if (close) {
        close.addEventListener("click", e => {
          e.stopPropagation();
          popup.classList.remove("show");
        });
      }
    });

    /* Confirmación de deshabilitar */
    const confirmPopup = shadow.querySelector(".my-products__popup--confirm-disable");
    if (confirmPopup) {
      const cancel = confirmPopup.querySelector(".my-products__popup-btn--cancel");
      const accept = confirmPopup.querySelector(".my-products__popup-btn--accept");

      cancel.addEventListener("click", () => confirmPopup.classList.remove("show"));

      accept.addEventListener("click", () => {
        confirmPopup.classList.remove("show");
        this.showPopup(shadow, ".my-products__popup--disable-success");
      });
    }
  }

  showPopup(shadow, selector) {
    const popup = shadow.querySelector(selector);
    if (popup) popup.classList.add("show");
  }

  /* ============================================================
                    POPUP DE DETALLES
  ============================================================ */
  setupDetailsPopup(shadow) {
    const popup = shadow.querySelector(".my-products__popup--details");

    const close = popup.querySelector(".my-products__popup-close");
    close.addEventListener("click", () => popup.classList.remove("show"));

    popup.addEventListener("click", e => {
      if (e.target.classList.contains("my-products__popup--details")) {
        popup.classList.remove("show");
      }
    });
  }

  openDetailsPopup(shadow, card) {
    const name = card.querySelector(".my-products__card-name")?.textContent.replace("Nombre del Producto: ", "");
    const type = card.querySelector(".my-products__card-type span")?.textContent;
    const price = card.querySelector(".my-products__card-price")?.textContent.replace("Precio: ", "");
    const stock = card.querySelector(".my-products__card-stock span")?.textContent;

    const popup = shadow.querySelector(".my-products__popup--details");

    popup.querySelector(".my-products__details-name").textContent = name;
    popup.querySelector(".my-products__details-type").textContent = type;
    popup.querySelector(".my-products__details-price").textContent = price;
    popup.querySelector(".my-products__details-stock").textContent = stock;

    popup.querySelector(".my-products__details-unit").textContent = "$10.000";
    popup.querySelector(".my-products__details-description").textContent = "Producto fresco de alta calidad.";
    popup.querySelector(".my-products__details-unit-weight").textContent = "Kilogramos";
    popup.querySelector(".my-products__details-weight").textContent = "24 kg";

    popup.classList.add("show");
  }
}

customElements.define("my-products", MyProducts);
