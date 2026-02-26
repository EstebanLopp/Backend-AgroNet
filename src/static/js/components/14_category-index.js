// document.addEventListener("DOMContentLoaded", () => {
//   const container = document.querySelector(".category-index");
//   if (container) {
//     fetch("/src/templates/components/14_category-index.html")
//       .then(response => {
//         if (!response.ok) {
//           throw new Error("Error al cargar el componente: " + response.status);
//         }
//         return response.text();
//       })
//       .then(data => {
//         container.innerHTML = data;
//       })
//       .catch(error => {
//         console.error("Error cargando category-index:", error);
//       });
//   }
// });
