document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".orders__profile");

  try {
    const htmlResponse = await fetch("/src/templates/components/51_historial_orders_customer.html");
    if (!htmlResponse.ok) throw new Error("No se pudo cargar el componente HTML");

    const html = await htmlResponse.text();
    container.insertAdjacentHTML("beforeend", html);

    // Seleccionar por class
    const ordersContainer = document.querySelector(".orders__container");
    const template = document.querySelector(".orders__template");

    const dataResponse = await fetch("/src/static/data/orders.json");
    if (!dataResponse.ok) throw new Error("No se pudo cargar el archivo JSON");

    const pedidos = await dataResponse.json();

    ordersContainer.innerHTML = "";

    pedidos.forEach(pedido => {
      const clone = template.content.cloneNode(true);

      clone.querySelector(".orders__article-id").textContent = `Naranja, Manzana Gala, Cafe`;

      const statusEl = clone.querySelector(".orders__article-status");
      statusEl.textContent = `Estado: ${pedido.estado}`;
      statusEl.classList.add(
        pedido.estado.toLowerCase() === "enviado"
          ? "orders__article-status--enviado"
          : "orders__article-status--pendiente"
      );

      ordersContainer.appendChild(clone);
    });

  } catch (error) {
    console.error("Error al cargar el historial de pedidos:", error);
  }
});
