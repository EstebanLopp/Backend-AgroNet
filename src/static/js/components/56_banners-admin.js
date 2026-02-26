
document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".admin-view");

  try {
    const htmlResponse = await fetch("/src/templates/components/56_banners-admin.html");
    if (!htmlResponse.ok) throw new Error("No se pudo cargar el componente HTML");

    const html = await htmlResponse.text();
    container.insertAdjacentHTML("beforeend", html);

    const grid = document.querySelector(".admin-banners__grid");

    // Cargar banners desde JSON simulado
    const dataResponse = await fetch("/src/static/data/admin_banners.json");
    if (!dataResponse.ok) throw new Error("No se pudo cargar los banners");

    const banners = await dataResponse.json();

    grid.innerHTML = "";
    banners.forEach(banner => {
      const card = document.createElement("article");
      card.classList.add("admin-banners__card");
      card.innerHTML = `
        <div class="admin-banners__image-container">
          <img src="${banner.image}" alt="${banner.name}" class="admin-banners__image" />
        </div>
        <div class="admin-banners__info">
          <h3 class="admin-banners__name">${banner.name}</h3>
          <p class="admin-banners__description">${banner.description}</p>
          <div class="admin-banners__actions">
            <button class="admin-banners__btn admin-banners__btn--edit">Editar</button>
            <button class="admin-banners__btn admin-banners__btn--delete">Eliminar</button>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });

    // Popups
    const popupConfirm = document.querySelector(".admin-banners__popup--confirm");
    const popupSuccess = document.querySelector(".admin-banners__popup--success");

    grid.addEventListener("click", (e) => {
      if (e.target.classList.contains("admin-banners__btn--delete")) {
        popupConfirm.classList.add("show");
      }
    });

    popupConfirm.addEventListener("click", (e) => {
      if (
        e.target.closest(".admin-banners__popup-close") ||
        e.target.classList.contains("admin-banners__popup") ||
        e.target.classList.contains("admin-banners__btn--cancel")
      ) {
        popupConfirm.classList.remove("show");
      }

      if (e.target.classList.contains("admin-banners__btn--accept")) {
        popupConfirm.classList.remove("show");
        popupSuccess.classList.add("show");
      }
    });

    popupSuccess.addEventListener("click", (e) => {
      if (
        e.target.classList.contains("admin-banners__popup-close") ||
        e.target.classList.contains("admin-banners__popup")
      ) {
        popupSuccess.classList.remove("show");
      }
    });

  } catch (error) {
    console.error("Error al cargar los banners:", error);
  }
});

