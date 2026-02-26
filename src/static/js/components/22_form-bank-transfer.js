// class FormBankTransfer extends HTMLElement {
//   constructor() {
//     super();
//   }

//   connectedCallback() {
//     fetch("/frontend/public/data/form-bank-transfer.json")
//       .then(response => response.json())
//       .then(data => {
//         this.innerHTML = `
//           <section class="form-bank-transfer">
//             <button class="form-bank-transfer__back-btn bank-transfer__btn" type="button" onclick="window.history.back()">
//               Atrás
//             </button>
//             <div class="form-bank-transfer__inner">

//               <div class="form-bank-transfer__header">
//                 <h2 class="form-bank-transfer__title">${data.title}</h2>
//               </div>

//               <form class="form-bank-transfer__form">
//                 ${data.fields.map(field => `
//                   <div class="form-bank-transfer__group">
//                     <label for="${field.id}" class="form-bank-transfer__label">${field.label}</label>
//                     <input 
//                       type="${field.type}" 
//                       id="${field.id}" 
//                       name="${field.name}" 
//                       placeholder="${field.placeholder}" 
//                       ${field.required ? "required" : ""} 
//                       class="form-bank-transfer__input">
//                   </div>
//                 `).join("")}
//                 <div class="bank-transfer__actions">
//                   <button type="submit" class="bank-transfer__btn">${data.submitText}</button>
//                 </div>
//               </form>
//             </div>
//           </section>
//         `;
//       })
//       .catch(error => {
//         console.error("Error cargando el JSON del formulario:", error);
//         this.innerHTML = `<p style="color:red;">Error al cargar el formulario.</p>`;
//       });
//   }
// }

// customElements.define("form-bank-transfer", FormBankTransfer);
