document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("product-detail-customer-container");

  //  Ruta corregida según ubicación actual de product.html
  fetch("/src/templates/components/35_product_detail_customer.html")
    .then(response => {
      console.log("Estado del fetch:", response.status, "Ruta usada:", response.url);
      if (!response.ok) throw new Error("No se pudo cargar el componente");
      return response.text();
    })
    .then(html => {
      container.innerHTML = html;
    })
    .catch(error => {
      console.error("Error al cargar el componente:", error);
      container.innerHTML = "<p>Error al cargar el detalle del producto.</p>";
    });
});
