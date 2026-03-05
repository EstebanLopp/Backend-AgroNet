document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-product");

  if (container) {
    fetch("/src/templates/components/70_form_new_product_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        
        const form = container.querySelector(".form-datos__form");
        const popup = container.querySelector(".popup");
        const closeBtn = container.querySelector(".popup__close");

        if (form && popup) {
          
          form.addEventListener("submit", (e) => {
            e.preventDefault(); 
            popup.classList.add("popup--visible"); 
          });

          
          if (closeBtn) {
            closeBtn.addEventListener("click", () => {
              popup.classList.remove("popup--visible");
              
              window.location.href = "/src/templates/admin-pages/products.html";
            });
          }

          
          popup.addEventListener("click", (e) => {
            if (e.target === popup) {
              popup.classList.remove("popup--visible");
              window.location.href = "/src/templates/admin-pages/products.html";
            }
          });
        }
      })
      .catch(err => console.error("Error cargando el componente:", err));
  }
});
