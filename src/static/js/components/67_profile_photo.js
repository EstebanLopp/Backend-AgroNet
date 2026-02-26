document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".container-profile-photo");

  // Cargar el HTML del componente
  const res = await fetch("/src/templates/components/67_profile_photo.html");
  const html = await res.text();
  const div = document.createElement("div");
  div.innerHTML = html;
  const template = div.querySelector("#template-profile-photo");
  container.appendChild(template.content.cloneNode(true));

  const grid = document.querySelector(".profile-photo__grid");

  // Cargar las fotos del JSON
  const resJSON = await fetch("/src/static/data/profile_photo.json");
  const photos = await resJSON.json();

  photos.forEach((photo) => {
    const card = document.createElement("div");
    card.classList.add("profile-photo__card");

    card.innerHTML = `
      <img src="${photo.url}" alt="${photo.name}" class="profile-photo__card-img" />
      <div class="profile-photo__card-body">
        <h3 class="profile-photo__card-title">${photo.name}</h3>
        <div class="profile-photo__card-buttons">
          <button class="profile-photo__btn profile-photo__btn--grid" data-id="${photo.id}">Seleccionar</button>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

  // Referencias al modal
  const modal = document.getElementById("profile-photo__modal");
const closeModal = document.getElementById("profile-photo__close");
const cancelBtn = document.getElementById("profile-photo__cancel");
const acceptBtn = document.getElementById("profile-photo__accept");
const modalText = document.getElementById("profile-photo__text");
  let selectedPhoto = null;

  // Escuchar clicks en “Seleccionar”
  grid.addEventListener("click", (e) => {
    if (e.target.classList.contains("profile-photo__btn")) {
      const id = e.target.dataset.id;
      selectedPhoto = photos.find((p) => p.id == id);

      // Mostrar modal con el nombre de la foto
      modalText.textContent = `¿Deseas establecer "${selectedPhoto.name}" como tu foto de perfil?`;
      modal.style.display = "flex";
    }
  });

  // Cerrar modal
  const close = () => (modal.style.display = "none");
  closeModal.addEventListener("click", close);
  cancelBtn.addEventListener("click", close);

  // Confirmar selección
  acceptBtn.addEventListener("click", () => {
    if (selectedPhoto) {
      // Marcar la seleccionada visualmente
      document.querySelectorAll(".profile-photo__btn--grid").forEach((btn) => {
        btn.textContent = "Seleccionar";
        btn.classList.remove("profile-photo__btn--selected");
      });

      const selectedBtn = document.querySelector(`.profile-photo__btn--grid[data-id="${selectedPhoto.id}"]`);
      selectedBtn.textContent = "Seleccionado";
      selectedBtn.classList.add("profile-photo__btn--selected");
    }

    close();
  });

  // Cerrar al hacer clic fuera
  window.addEventListener("click", (e) => {
    if (e.target === modal) close();
  });
});
