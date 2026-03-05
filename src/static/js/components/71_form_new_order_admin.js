document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-order");

  if (container) {
    fetch("/src/templates/components/71_form_new_order_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        
        const form = container.querySelector(".form-datos__form");
        const popupSuccess = container.querySelector(".popup--success");

        if (form && popupSuccess) {
          
          form.addEventListener("submit", (e) => {
            e.preventDefault(); 
            popupSuccess.classList.add("show"); 
          });

          
          popupSuccess.addEventListener("click", (e) => {
            if (
              e.target.classList.contains("popup__close") || 
              e.target === popupSuccess 
            ) {
              popupSuccess.classList.remove("show");

              
              window.location.href = "/src/templates/admin-pages/orders.html";
            }
          });
        }
      })
      .catch(err => console.error("Error al cargar el componente:", err));
  }
});
