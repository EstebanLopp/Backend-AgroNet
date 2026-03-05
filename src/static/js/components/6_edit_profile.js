document.addEventListener("DOMContentLoaded", function() {
  const heroElement = document.querySelector(".register-container");

  if (heroElement) {
    fetch("/src/templates/components/6_edit_profile.html")
      .then(response => response.text())
      .then(data => {
        heroElement.innerHTML = data;

        setTimeout(() => {

          const steps = Array.from(heroElement.querySelectorAll(".register-form__step"));
          const nextBtns = heroElement.querySelectorAll(".register-form__button--next");
          const prevBtns = heroElement.querySelectorAll(".register-form__button--prev");
          const form = heroElement.querySelector(".register-form");

          let currentStep = 0;

          
          const popup = heroElement.querySelector(".register-form__confirm-popup");
          const successModal = heroElement.querySelector(".register-form__success-modal");

          
          const btnCancel = popup ? popup.querySelector(".register-form__confirm-popup-btn--cancel") : null;
          const btnAccept = popup ? popup.querySelector(".register-form__confirm-popup-btn--accept") : null;
          const btnCloseSuccess = successModal ? successModal.querySelector(".register-form__success-modal-close") : null;

          
          steps.forEach((step, i) => {
            step.classList.toggle("register-form__step--active", i === currentStep);
          });

          
          nextBtns.forEach(btn => {
            btn.addEventListener("click", () => {
              const inputs = steps[currentStep].querySelectorAll("input, select");

              for (let input of inputs) {
                if (!input.checkValidity()) {
                  input.reportValidity();
                  return;
                }
              }

              if (currentStep < steps.length - 1) {
                
                steps[currentStep].classList.remove("register-form__step--active");
                currentStep++;
                steps[currentStep].classList.add("register-form__step--active");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }
            });
          });

          
          prevBtns.forEach(btn => {
            btn.addEventListener("click", () => {
              if (currentStep > 0) {
                steps[currentStep].classList.remove("register-form__step--active");
                currentStep--;
                steps[currentStep].classList.add("register-form__step--active");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }
            });
          });

          
          if (form) {
            form.addEventListener("submit", e => {
              e.preventDefault();
              if (popup) {
                popup.classList.add("show");
              } else if (successModal) {
                
                successModal.classList.add("show");
              } else {
                
                window.location.href = "/src/templates/customer-pages/my_profile.html";
              }
            });
          }

          
          if (popup) {
            
            if (btnCancel) {
              btnCancel.addEventListener("click", () => {
                popup.classList.remove("show");
              });
            }

            
            if (btnAccept) {
              btnAccept.addEventListener("click", () => {
                popup.classList.remove("show");
                if (successModal) successModal.classList.add("show");
              });
            }

            
            popup.addEventListener("click", (e) => {
              if (e.target.classList.contains("register-form__confirm-popup")) {
                popup.classList.remove("show");
              }
            });
          }

          
          if (successModal) {
            if (btnCloseSuccess) {
              btnCloseSuccess.addEventListener("click", () => {
                successModal.classList.remove("show");
                window.location.href = "/src/templates/customer-pages/my_profile.html";
              });
            }

            
            successModal.addEventListener("click", (e) => {
              if (e.target.classList.contains("register-form__success-modal")) {
                successModal.classList.remove("show");
                window.location.href = "/src/templates/customer-pages/my_profile.html";
              }
            });
          }

        }, 300);
      })
      .catch(error => console.log("Error al cargar la cuenta:", error));
  }
});
