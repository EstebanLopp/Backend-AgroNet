
class EditProduct extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.loadTemplate();
  }

  async loadTemplate() {
    try {
      const [htmlRes, cssRes] = await Promise.all([
        fetch("/src/templates/components/63_edit_product.html"),
        fetch("/src/static/css/components/63_edit_product.css")
      ]);

      const html = await htmlRes.text();
      const css = await cssRes.text();

      const tempContainer = document.createElement("div");
      tempContainer.innerHTML = html.trim();

      const template = tempContainer.querySelector("template");
      if (!template) {
        console.error("❌ No se encontró el <template>");
        return;
      }

      const content = template.content.cloneNode(true);

      const style = document.createElement("style");
      style.textContent = css;

      const linkFA = document.createElement("link");
      linkFA.rel = "stylesheet";
      linkFA.href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css";

      this.shadowRoot.append(style, linkFA, content);

      setTimeout(() => {
        this.initDropdowns();
        this.initModals();
      }, 150);
    } catch (error) {
      console.error("Error al cargar el componente EditProduct:", error);
    }
  }

  initDropdowns() {
    const shadow = this.shadowRoot;
    const dropdowns = shadow.querySelectorAll(".edit-product__dropdown-wrapper");

    dropdowns.forEach((dropdown) => {
      const trigger = dropdown.querySelector(".edit-product__dropdown-trigger");
      const optionsBox = dropdown.querySelector(".edit-product__dropdown-options");
      const options = dropdown.querySelectorAll(".edit-product__dropdown-option");
      const select = dropdown.parentElement.querySelector("select");

      if (!trigger || !optionsBox || !options.length || !select) return;

      trigger.addEventListener("click", (e) => {
        e.stopPropagation();
        const isOpen = optionsBox.style.display === "flex";
        optionsBox.style.display = isOpen ? "none" : "flex";
      });

      options.forEach((option) => {
        option.addEventListener("click", () => {
          trigger.querySelector("span").textContent = option.textContent;
          select.value = option.dataset.value;
          optionsBox.style.display = "none";
        });
      });

      window.addEventListener("click", (e) => {
        if (!dropdown.contains(e.composedPath()[0])) {
          optionsBox.style.display = "none";
        }
      });
    });
  }

  initModals() {
    const shadow = this.shadowRoot;

    const editBtn = shadow.querySelector(".edit-product__btn-edit");
    const confirmModal = shadow.getElementById("edit-product__confirm-modal");
    const successModal = shadow.getElementById("edit-product__success-modal");

    const cancelBtn = shadow.getElementById("cancel_edit");
    const acceptBtn = shadow.getElementById("accept_edit");
    const closeSuccess = shadow.getElementById("close_edit_success");

    if (!editBtn || !confirmModal || !successModal) return;

    editBtn.addEventListener("click", () => confirmModal.classList.add("show"));
    cancelBtn.addEventListener("click", () => confirmModal.classList.remove("show"));

    acceptBtn.addEventListener("click", () => {
      confirmModal.classList.remove("show");
      successModal.classList.add("show");
    });

    const redirectURL = "/src/templates/seller-pages/my_products.html";

    closeSuccess.addEventListener("click", () => {
      successModal.classList.remove("show");
      window.location.href = redirectURL;
    });

    successModal.addEventListener("click", (e) => {
      if (e.target === successModal || e.target.closest(".edit-product__modal-content")) {
        successModal.classList.remove("show");
        window.location.href = redirectURL;
      }
    });
  }
}

customElements.define("edit-product", EditProduct);

