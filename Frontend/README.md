# 🚘 Frontend FPC (Full Paint Cars)

Frontend desarrollado con **React**, **TypeScript** y **Vite** para el sistema de gestión de servicios automotrices **FPC**.

Este frontend forma parte de una solución completa donde los usuarios pueden **registrarse, iniciar sesión y visualizar información** sobre los servicios de la empresa, así como interactuar según su rol (cliente, empleado o administrador).

---

## 🚀 Tecnologías utilizadas

- ⚛️ **React** — Librería principal para la interfaz
- 🟦 **TypeScript** — Tipado estático para robustez en desarrollo
- ⚡ **Vite** — Herramienta de construcción ultrarrápida
- 🎨 **CSS Modular** — Archivos `.css` separados por componente
- 📁 **Arquitectura por componentes** — Separación clara de vistas, componentes y estilos

---

## 📁 Estructura del proyecto

```

Frontend-FPC/
├── public/
├── src/
│   ├── assets/
│   │   ├── css/
│   │   │   ├── Navbar.css
│   │   │   ├── Footer.css
│   │   │   └── ...otros estilos
│   │   ├── logo.png
│   │   └── react.svg
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   └── ...otros componentes
│   ├── Pages/
│   │   ├── Login.tsx
│   │   └── Registro.tsx
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   ├── index.css
│   └── vite-env.d.ts
├── index.html
├── package.json
└── vite.config.ts

````
## 📂 Creación de la estructura desde cero (PowerShell)

Si deseas replicar la estructura de este proyecto manualmente usando PowerShell:

```powershell
# Crear carpeta principal del proyecto
mkdir "Frontend-FPC"
cd "Frontend-FPC"

# Inicializar proyecto Vite con React + TypeScript
npm create vite@latest . -- --template react-ts

# Instalar dependencias
npm install

# Crear carpetas adicionales
mkdir src\assets
mkdir src\assets\css
mkdir src\components
mkdir src\Pages

# Crear archivos principales en src
New-Item src\App.tsx -ItemType File
New-Item src\App.css -ItemType File
New-Item src\main.tsx -ItemType File
New-Item src\index.css -ItemType File
New-Item src\vite-env.d.ts -ItemType File

# Crear archivos en src\Pages
New-Item src\Pages\Login.tsx -ItemType File
New-Item src\Pages\Registro.tsx -ItemType File

# Crear archivos en src\components
New-Item src\components\Navbar.tsx -ItemType File
New-Item src\components\Footer.tsx -ItemType File
New-Item src\components\HeroSections.tsx -ItemType File
New-Item src\components\Features.tsx -ItemType File
New-Item src\components\HowItWorks.tsx -ItemType File
New-Item src\components\Benefits.tsx -ItemType File

# Crear archivos CSS por componente en assets/css
New-Item src\assets\css\Navbar.css -ItemType File
New-Item src\assets\css\Footer.css -ItemType File
New-Item src\assets\css\HeroSection.css -ItemType File
New-Item src\assets\css\Features.css -ItemType File
New-Item src\assets\css\HowItWorks.css -ItemType File
New-Item src\assets\css\Benefits.css -ItemType File
New-Item src\assets\css\FormAuth.css -ItemType File

# Agregar imágenes ejemplo (manual o con comandos)
New-Item src\assets\logo.png -ItemType File
New-Item src\assets\react.svg -ItemType File

# Confirmación
Write-Host "`n✅ Estructura del proyecto Frontend FPC creada correctamente." -ForegroundColor Green

´´´´


## 🧪 Funcionalidades actuales

- ✅ Navbar fija con detección de scroll
- ✅ Footer global
- ✅ Página principal con:
  - Sección de bienvenida (`HeroSections`)
  - Beneficios (`Benefits`)
  - Cómo funciona (`HowItWorks`)
  - Características (`Features`)
- ✅ Sistema de autenticación visual (login y registro en desarrollo)
- ✅ Estructura modular lista para conexión con backend



## 🛠️ Instalación del proyecto

1. **Clona este repositorio:**

```bash
git clone https://github.com/tu_usuario/Frontend-FPC.git
cd Frontend-FPC


2. **Instala las dependencias:**

```bash
npm install
```

3. **Ejecuta el servidor de desarrollo:**

```bash
npm run dev
```

---

## 📝 Consideraciones

* El sistema está preparado para integrarse con un backend (por ejemplo, desarrollado en Flask o FastAPI).
* Se recomienda manejar las variables sensibles (si aplican en el futuro) desde un archivo `.env` (aunque en Vite deben estar prefijadas con `VITE_`).

---

## 📦 Scripts disponibles

| Comando           | Descripción                      |
| ----------------- | -------------------------------- |
| `npm run dev`     | Inicia la app en modo desarrollo |
| `npm run build`   | Compila la app para producción   |
| `npm run preview` | Previsualiza la app ya compilada |

---

## 🤝 Autores y créditos

* 👨‍💻 **Oscar Mauricio Cruz Figueroa** – Fullstack / Documentación
* 🧠 **Maicol Steven Espitia** – Backend principal
* 🎨 **Ronny Borda Ardila** – Frontend principal

---

## 📌 Estado del proyecto

🟡 **Fase de desarrollo inicial**
✔️ Base estructural terminada
🚧 Conexión con backend pendiente
📦 Pronto se agregarán funcionalidades dinámicas

---

## 📬 Contacto

¿Dudas o sugerencias? Puedes escribir a:

📧 [oscar.cruz.fpc@correo.com](mailto:oscar.cruz.fpc@correo.com)
📞 +57 3227813912

---

## 📝 Licencia

Este proyecto está bajo la **MIT License**. Puedes usarlo, modificarlo y adaptarlo libremente. Se agradece mantener los créditos si es reutilizado públicamente.

---

```


¿Deseas que se mencione algún API o endpoint en particular si ya tienes definido el backend? También puedo ayudarte con un README unificado entre frontend y backend si estás planeando empaquetar todo.
```strictTypeChecked,
      // Optionally, add this for stylistic rules
      ...tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
