document.addEventListener("DOMContentLoaded", function () {

  const heroElement = document.querySelector(".register-container");
  if (!heroElement) return;

  const steps = heroElement.querySelectorAll(".register-form__step");
  const nextBtns = heroElement.querySelectorAll(".register-form__button--next");
  const prevBtns = heroElement.querySelectorAll(".register-form__button--prev");
  const form = heroElement.querySelector(".register-form");

  if (!form) return;

  let currentStep = 0;

  function updateSteps() {
    steps.forEach((step, i) => {
      step.classList.toggle("register-form__step--active", i === currentStep);
    });
  }

  updateSteps();

  nextBtns.forEach(btn =>
    btn.addEventListener("click", () => {
      const inputs = steps[currentStep].querySelectorAll("input, select");

      for (let input of inputs) {
        if (!input.checkValidity()) {
          input.reportValidity();
          return;
        }
      }

      if (currentStep < steps.length - 1) {
        currentStep++;
        updateSteps();
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    })
  );

  prevBtns.forEach(btn =>
    btn.addEventListener("click", () => {
      if (currentStep > 0) {
        currentStep--;
        updateSteps();
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    })
  );

  form.addEventListener("submit", e => {
    e.preventDefault();

    const modal = heroElement.querySelector(".register-form__success-modal");
    const closeBtn = modal.querySelector(".register-form__success-modal-close");

    modal.classList.add("show");

    function closeModal() {
      modal.classList.remove("show");
      window.location.href = "/login/";
    }

    closeBtn.addEventListener("click", closeModal);

    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
  });

});