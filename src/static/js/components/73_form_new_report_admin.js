document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container-form-report");

  if (container) {
    fetch("/src/templates/components/73_form_new_report_admin.html")
      .then(res => res.text())
      .then(component => {
        container.innerHTML = component;

        
        const form = container.querySelector(".form-datos__form");
        const popupSuccess = container.querySelector(".popup--report-success");

        if (form && popupSuccess) {
          
          form.addEventListener("submit", (e) => {
            e.preventDefault(); 
            popupSuccess.classList.add("show"); 
          });

          
          popupSuccess.addEventListener("click", (e) => {
            if (
              e.target.classList.contains("popup") ||       
              e.target.closest(".popup__close")            
            ) {
              popupSuccess.classList.remove("show");

              
              window.location.href = "/src/templates/admin-pages/reports.html";
            }
          });
        }
      });
  }
});
