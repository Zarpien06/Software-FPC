
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

// Función para mostrar/ocultar un chat
function toggleChat(chatId) {
  // Ocultar todos los chats
  const allChats = document.querySelectorAll('.chat-message');
  allChats.forEach(chat => {
    chat.style.display = 'none';
  });

  // Mostrar el chat seleccionado
  const selectedChat = document.getElementById(`chat-message-${chatId}`);
  if (selectedChat.style.display === 'none') {
    selectedChat.style.display = 'block';
  } else {
    selectedChat.style.display = 'none';
  }
}

// Función para cerrar un chat
function closeChat(chatId) {
  const chat = document.getElementById(`chat-message-${chatId}`);
  chat.style.display = 'none';
}
