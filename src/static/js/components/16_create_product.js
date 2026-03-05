class FormCreatedProduct extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: "open" });

    
    fetch("/src/templates/components/16_create_product.html")
      .then((res) => res.text())
      .then((html) => {
        const templateContainer = document.createElement("div");
        templateContainer.innerHTML = html;

        const template = templateContainer.querySelector("template");
        const content = template.content.cloneNode(true);
        shadow.appendChild(content);

        // CSS
        const linkStyle = document.createElement("link");
        linkStyle.rel = "stylesheet";
        linkStyle.href = "/src/static/css/components/16_create_product.css";
        shadow.appendChild(linkStyle);

        
        const linkFA = document.createElement("link");
        linkFA.rel = "stylesheet";
        linkFA.href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css";
        shadow.appendChild(linkFA);


        const dropdowns = shadow.querySelectorAll(".form-created-product__dropdown");

        dropdowns.forEach((dropdown) => {
          const trigger = dropdown.querySelector(".form-created-product__dropdown-trigger");
          const optionsBox = dropdown.querySelector(".form-created-product__dropdown-options");
          const options = dropdown.querySelectorAll(".form-created-product__dropdown-option");
          const select = dropdown.querySelector(".form-created-product__hidden-select");

          
          trigger.addEventListener("click", (e) => {
            e.stopPropagation();
            dropdown.classList.toggle("form-created-product__dropdown--open");
          });

          
          options.forEach((opt) => {
            opt.addEventListener("click", () => {
              trigger.querySelector("span").textContent = opt.textContent;
              select.value = opt.dataset.value;
              dropdown.classList.remove("form-created-product__dropdown--open");
            });
          });

          
          shadow.addEventListener("click", (e) => {
            if (!dropdown.contains(e.target)) {
              dropdown.classList.remove("form-created-product__dropdown--open");
            }
          });
        });

        

        const modal = shadow.querySelector(".form-created-product__modal");
        const modalContent = shadow.querySelector(".form-created-product__modal-content");
        const closeBtn = shadow.querySelector(".form-created-product__modal-close");
        const publishBtn = shadow.querySelector(".form-created-product__btn-publish-product");

        if (!modal || !modalContent || !closeBtn || !publishBtn) {
          console.error("Error: No se encontraron elementos del modal en el Shadow DOM");
          return;
        }

        
        publishBtn.addEventListener("click", () => {
          modal.classList.add("show");
        });

        
        closeBtn.addEventListener("click", () => {
          modal.classList.remove("show");
          window.location.href = "/src/templates/seller-pages/my_products.html";
        });

        
        modal.addEventListener("click", () => {
          modal.classList.remove("show");
          window.location.href = "/src/templates/seller-pages/my_products.html";
        });

        
        modalContent.addEventListener("click", (e) => e.stopPropagation());
              })
      .catch((err) => console.error("Error cargando el componente:", err));
  }
}

customElements.define("form-created-product", FormCreatedProduct);
