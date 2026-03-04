document.addEventListener("DOMContentLoaded", async () => {

  const grid = document.querySelector(".profile-photo__grid");

  if (!grid) {
    console.error("No existe .profile-photo__grid");
    return;
  }

  let photos = [];

  try {

    // 🔥 Usamos la variable enviada por Django
    const resJSON = await fetch(profilePhotoURL);

    if (!resJSON.ok) {
      throw new Error("No se pudo cargar el JSON");
    }

    photos = await resJSON.json();

  } catch (error) {
    console.error("Error cargando JSON:", error);
    return;
  }

  photos.forEach((photo) => {

    const card = document.createElement("div");
    card.classList.add("profile-photo__card");

    card.innerHTML = `
      <img src="${photo.url}" alt="${photo.name}" class="profile-photo__card-img" />
      <div class="profile-photo__card-body">
        <h3 class="profile-photo__card-title">${photo.name}</h3>
        <div class="profile-photo__card-buttons">
          <button class="profile-photo__btn profile-photo__btn--grid" data-id="${photo.id}">
            Seleccionar
          </button>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

});