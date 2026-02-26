document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector(".admin-view");

  try {
    const response = await fetch("/src/templates/components/61_admin_users.html");
    if (!response.ok) throw new Error("No se pudo cargar el componente de usuarios");

    const html = await response.text();
    container.innerHTML = html;

    const tableBody = document.querySelector(".admin-users__body");
    const modal = document.querySelector(".admin-users__modal");
    const modalBody = modal.querySelector(".admin-users__modal-body");
    const closeModal = modal.querySelector(".admin-users__btn--close");
    const searchInput = document.querySelector(".admin-users__search");

    const popupConfirm = document.querySelector(".admin-users__popup--confirm");
    const popupSuccess = document.querySelector(".admin-users__popup--success");
    const popupConfirmClose = popupConfirm.querySelector(".admin-users__popup-close");
    const popupSuccessClose = popupSuccess.querySelector(".admin-users__popup-close");

    const popupCancelBtn = popupConfirm.querySelector(".admin-users__popup-btn--cancel");
    const popupAcceptBtn = popupConfirm.querySelector(".admin-users__popup-btn--accept");

    const users = [
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" },
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" },
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" },
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" },
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" },
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" },
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" },
      { nombre: "Juan", apellido: "Pérez", usuario: "jperez", telefono: "3111234567", correo: "juanperez@mail.com", tipo_doc: "CC", numero: "123456789", direccion: "Calle 10 #15-30", departamento: "Risaralda", municipio: "Pereira", tipo_usuario: "Administrador", fecha_nac: "1995-05-20" }
      
    ];

    const renderUsers = (list) => {
      tableBody.innerHTML = "";
      list.forEach((user, i) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${user.nombre}</td>
          <td>${user.apellido}</td>
          <td>${user.usuario}</td>
          <td>${user.telefono}</td>
          <td>${user.correo}</td>
          <td>${user.tipo_doc}</td>
          <td>${user.numero}</td>
          <td>${user.direccion}</td>
          <td>${user.departamento}</td>
          <td>${user.municipio}</td>
          <td>${user.tipo_usuario}</td>
          <td>${user.fecha_nac}</td>
          <td class="admin-users__actions-btns">
            <button class="admin-users__btn admin-users__btn--view" data-index="${i}"><i class="fa-solid fa-eye"></i></button>
            <a href="/src/templats/admin-pages/form_edit_user.html" class="admin-users__btn admin-users__btn--edit"><i class="fa-solid fa-pen"></i></a>
            <button class="admin-users__btn admin-users__btn--delete" data-index="${i}"><i class="fa-solid fa-xmark"></i></button>
          </td>
        `;
        tableBody.appendChild(row);
      });
    };

    renderUsers(users);

    searchInput.addEventListener("input", (e) => {
      const value = e.target.value.toLowerCase();
      const filtered = users.filter(u =>
        u.nombre.toLowerCase().includes(value) ||
        u.apellido.toLowerCase().includes(value) ||
        u.usuario.toLowerCase().includes(value) ||
        u.correo.toLowerCase().includes(value) ||
        u.tipo_usuario.toLowerCase().includes(value)
      );
      renderUsers(filtered);
    });

    tableBody.addEventListener("click", (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;

      const index = btn.dataset.index;
      const user = users[index];

      if (btn.classList.contains("admin-users__btn--view")) {
        modalBody.innerHTML = `
          <p><strong>Nombre:</strong> ${user.nombre} ${user.apellido}</p>
          <p><strong>Usuario:</strong> ${user.usuario}</p>
          <p><strong>Correo:</strong> ${user.correo}</p>
          <p><strong>Teléfono:</strong> ${user.telefono}</p>
          <p><strong>Dirección:</strong> ${user.direccion}</p>
          <p><strong>Departamento:</strong> ${user.departamento}</p>
          <p><strong>Municipio:</strong> ${user.municipio}</p>
          <p><strong>Tipo de usuario:</strong> ${user.tipo_usuario}</p>
          <p><strong>Fecha de nacimiento:</strong> ${user.fecha_nac}</p>
          <p><strong>Tipo de documento:</strong> ${user.tipo_doc}</p>
          <p><strong>Número de documento:</strong> ${user.numero}</p>
        `;
        modal.style.display = "flex";
      }

      if (btn.classList.contains("admin-users__btn--delete")) {
        popupConfirm.classList.add("show");
      }
    });

    closeModal.addEventListener("click", () => (modal.style.display = "none"));
    popupConfirmClose.addEventListener("click", () => popupConfirm.classList.remove("show"));
    popupCancelBtn.addEventListener("click", () => popupConfirm.classList.remove("show"));

    popupAcceptBtn.addEventListener("click", () => {
      popupConfirm.classList.remove("show");
      popupSuccess.classList.add("show");
      setTimeout(() => popupSuccess.classList.remove("show"), 2500);
    });

    popupSuccessClose.addEventListener("click", () => popupSuccess.classList.remove("show"));

  } catch (error) {
    console.error("Error al cargar el componente de usuarios:", error);
  }
});
