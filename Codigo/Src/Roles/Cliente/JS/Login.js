// Animations
const registerButton = document.getElementById("register");
const loginButton = document.getElementById("login");
const container = document.getElementById("container");

registerButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});
loginButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

// Selecciona los contenedores
const registerSection = document.getElementById('register-section');
const loginSection = document.getElementById('login-section');

// Asegura que la sección de registro sea visible por defecto
window.onload = () => {
  registerSection.style.display = 'block'; // Mostrar registro
  loginSection.style.display = 'none';    // Ocultar inicio de sesión
};

// Check Register Error
const form = document.querySelector('form');
const username = document.getElementById('username');
const usernameError = document.querySelector("#username-error");
const email = document.getElementById('email');
const emailError = document.querySelector("#email-error");
const password = document.getElementById('password');
const passwordError = document.querySelector("#password-error");

// Show input error message
function showError(input, message) {
  const formControl = input.parentElement;
  formControl.className = 'form-control error';
  const small = formControl.querySelector('small');
  small.innerText = message;
}

// Show success outline
function showSuccess(input) {
  const formControl = input.parentElement;
  formControl.className = 'form-control success';
  const small = formControl.querySelector('small');
  small.innerText = '';
}

// Check email is valid
function checkEmail(email) {
  const emailRegex = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
  return emailRegex.test(email);
}

email.addEventListener("input", function () {
  if (!checkEmail(email.value)) {
    emailError.textContent = "*Email is not valid";
  } else {
    emailError.textContent = "";
  }
});

// Check length input user name
username.addEventListener("input", function () {
  if (username.value.length < 4) {
    usernameError.textContent = "*Username must be at least 8 characters.";
  } else if (username.value.length > 20) {
    usernameError.textContent = "*Username must be less than 20 characters.";
  } else {
    usernameError.textContent = "";
  }
});

// Check length input password
password.addEventListener("input", function () {
  if (password.value.length < 8) {
    passwordError.textContent = "*Password must be at least 8 characters.";
  } else if (password.value.length > 20) {
    passwordError.textContent = "*Password must be less than 20 characters.";
  } else {
    passwordError.textContent = "";
  }
});

// Check required fields
function checkRequired(inputArr) {
  let isRequired = false;
  inputArr.forEach(function (input) {
    if (input.value.trim() === '') {
      showError(input, `*${getFieldName(input)} is required`);
      isRequired = true;
    } else {
      showSuccess(input);
    }
  });
  return isRequired;
}

// Get fieldname
function getFieldName(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}

// Event listeners
form.addEventListener('submit', function (e) {
  e.preventDefault();
  if (!checkRequired([username, email, password])) {
    // checkLength(username, 3, 15)
    // checkLength(password, 6, 25)
    // checkEmail(email)
  }
});

// Check Login Error
let lgForm = document.querySelector('.form-lg');
let lgEmail = document.querySelector('.email-2');
let lgEmailError = document.querySelector(".email-error-2");
let lgPassword = document.querySelector('.password-2');
let lgPasswordError = document.querySelector(".password-error-2");

function showError2(input, message) {
  const formControl2 = input.parentElement;
  formControl2.className = 'form-control2 error';
  const small2 = formControl2.querySelector('small');
  small2.innerText = message;
}

function showSuccess2(input) {
  const formControl2 = input.parentElement;
  formControl2.className = 'form-control2 success';
  const small2 = formControl2.querySelector('small');
  small2.innerText = '';
}

// Check email is valid
function checkEmail2(lgEmail) {
  const emailRegex2 = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
  return emailRegex2.test(lgEmail);
}

lgEmail.addEventListener("input", function () {
  if (!checkEmail2(lgEmail.value)) {
    lgEmailError.textContent = "*Email is not valid";
  } else {
    lgEmailError.textContent = "";
  }
});

// Check length input password
lgPassword.addEventListener("input", function () {
  if (lgPassword.value.length < 8) {
    lgPasswordError.textContent = "*Password must be at least 8 characters.";
  } else if (lgPassword.value.length > 20) {
    lgPasswordError.textContent = "*Password must be less than 20 characters.";
  } else {
    lgPasswordError.textContent = "";
  }
});

function checkRequiredLg(inputArr2) {
  let isRequiredLg = false;
  inputArr2.forEach(function (input) {
    if (input.value.trim() === '') {
      showError2(input, `*${getFieldNameLg(input)} Please enter your information in this field`);
      isRequiredLg = true;
    } else {
      showSuccess2(input);
    }
  });
  return isRequiredLg;
}

function getFieldNameLg(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}

lgForm.addEventListener('submit', function (e) {
  e.preventDefault();
  if (!checkRequiredLg([lgEmail, lgPassword])) {
    checkEmail2(lgEmail);
    // Verificar credenciales
    if (lgEmail.value === 'oscarcruzsena2006@gmail.com' && lgPassword.value === '12345678') {
      window.location.href = 'maquetacion FPC/Cliente/IndexCliente.html';

    }else if(lgEmail.value === '../johandanielmirandamoreno@gmail.com' && lgPassword.value === '12345678')
    {
      window.location.href = '../maquetacion FPC/Administrador/adminPrincipal.html';
    }
    else if(lgEmail.value === 'empleado@gmail.com' && lgPassword.value === '12345678')
      {
        window.location.href = '../maquetacion FPC/Empleado/empleado.html';
      }
     else {
      lgPasswordError.textContent = "*Email o contraseña incorrectos";
    }
  }
});

function updatePlaceholder() {
  const idType = document.getElementById('id-type').value;
  const idNumberInput = document.getElementById('id-number');

  // Cambia el placeholder según el tipo de identificación
  if (idType === 'cc') {
      idNumberInput.placeholder = 'Número de Cédula de Ciudadanía';
  } else if (idType === 'ti') {
      idNumberInput.placeholder = 'Número de Tarjeta de Identidad';
  } else if (idType === 'ce') {
      idNumberInput.placeholder = 'Número de Cédula de Extranjería';
  } else if (idType === 'pp') {
      idNumberInput.placeholder = 'Número de Pasaporte';
  } else {
      idNumberInput.placeholder = 'Número de Identificación';
  }
}

