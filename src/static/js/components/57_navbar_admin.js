document.addEventListener("DOMContentLoaded", () => {
  const navbarContainer = document.querySelector(".navbar-admin-container");

  if (navbarContainer) {
    fetch("/src/templates/components/57_navbar_admin.html")
      .then(response => {
        if (!response.ok) throw new Error("Error al cargar el navbar del admin");
        return response.text();
      })
      .then(data => {
        navbarContainer.innerHTML = data;

        // Cargar CSS dinámicamente
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = "/src/static/css/components/57_navbar_admin.css";
        document.head.appendChild(link);

        // Esperar un momento para asegurar que el HTML está en el DOM
        setTimeout(() => {
          const toggle = document.querySelector(".admin-navbar__toggle");
          const navList = document.querySelector(".admin-navbar__list");
          const links = document.querySelectorAll(".admin-navbar__link");

          if (!toggle || !navList) return;

          // Mostrar / ocultar menú lateral
          toggle.addEventListener("click", () => {
            navList.classList.toggle("admin-navbar__list--active");
          });

          // Cerrar menú al hacer clic en un enlace
          links.forEach(link => {
            link.addEventListener("click", () => {
              navList.classList.remove("admin-navbar__list--active");
            });
          });
        }, 200);
      })
      .catch(error => console.error(error));
  }
});
