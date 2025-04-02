// Manejar el clic en "Administrar Usuario"
document.getElementById('adminUsuarioToggle').addEventListener('click', function(event) {
  event.preventDefault(); // Prevenir la redirección
  const submenu = document.getElementById('userSubmenu');
  // Alternar la visibilidad del submenú
  submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
});

document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle");
  const barraLateral = document.querySelector(".barra-lateral");

  // Evento para alternar la visibilidad de la barra lateral
  menuToggle.addEventListener("click", () => {
      barraLateral.classList.toggle("visible");
  });
});

// Función para mostrar un chat como alerta
function toggleChat(chatId) {
  // Definir el mensaje del chat
  let chatMessage = '';
  switch (chatId) {
      case 1:
          chatMessage = "Chat 1: Hola buenas tardes, quisiera saber como va mi automovil.";
          break;
      case 2:
          chatMessage = "Chat 2: Hola buenas tardes quisiera saber cuanto me valdria polarizarlo despues de pintarlo.";
          break;
      case 3:
          chatMessage = "Chat 3: Oye, ¿viste el partido de ayer?";
          break;
      default:
          chatMessage = "Chat no encontrado.";
  }

  // Mostrar el chat como una alerta
  alert(chatMessage);
}

// Función para cerrar un chat (no es necesaria si usamos alertas)
function closeChat(chatId) {
  // No se necesita implementar ya que las alertas se cierran automáticamente
}