document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-category");

  if (container) {
    fetch("/src/templates/components/72_form_new_category_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        
        const form = container.querySelector(".form-datos__form");
        const popup = container.querySelector(".popup--success-category");

        form.addEventListener("submit", (e) => {
          e.preventDefault();
          popup.classList.add("show");
        });

        
        popup.addEventListener("click", (e) => {
          
          if (
            e.target.classList.contains("popup") || 
            e.target.closest(".popup__close")
          ) {
            popup.classList.remove("show");
            
            window.location.href = "/src/templates/admin-pages/categories.html";
          }
        });
      });
  }
});
