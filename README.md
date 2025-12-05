# MeetFit 🏃‍♀️🤝  
Plataforma para encontrar gente con la que entrenar cerca de ti

MeetFit es una aplicación web **full-stack** que conecta a personas que quieren hacer deporte en compañía: puedes crear eventos deportivos, unirte a entrenamientos en grupo y gestionar tu perfil como deportista.

Este proyecto está desarrollado con:

- **Frontend:** React + Vite, React Router, Context API, React Bootstrap / MUI  
- **Backend:** Python, Flask, SQLAlchemy, JWT, Flask-Mail  
- **Base de datos:** PostgreSQL (o cualquier motor compatible vía `DATABASE_URL`)

---

## 👀 Por qué este proyecto es interesante para recruiters

En este proyecto he trabajado de principio a fin tanto el **lado producto** como la **parte técnica**:

- He diseñado un flujo completo de **autenticación con JWT** (registro, login, logout, cambio y recuperación de contraseña por email).
- He modelado la base de datos con **relaciones muchos-a-muchos** entre usuarios y actividades deportivas.
- He creado una **API REST** en Flask consumida desde un frontend en React con manejo de estado global y protección de rutas privadas.
- He integrado funcionalidades “de producto real”: newsletter, reportes y bloqueo de usuarios, enlace con Google Maps, sistema de rating preparado, etc.
- He cuidado la **arquitectura del código** para que sea mantenible (separación clara entre modelos, rutas, lógica de negocio y componentes de UI).

Si estás evaluando mi perfil, este repo resume bien cómo trabajo cuando construyo algo que podría usar un usuario final.

---

## 🌟 Funcionalidades principales (vista producto)

### 🏠 Área pública

Sin necesidad de registrarse, cualquier usuario puede:

- Ver la **landing page** con una petición a `/api/hello` para mostrar un mensaje dinámico.
- Consultar la página **“Sobre MeetFit”** donde explico el propósito de la plataforma.
- Navegar por un **listado de eventos deportivos**, con:
  - Tarjetas de cada actividad (título, descripción, deporte, plazas…).
  - Filtro por deporte y búsqueda por texto.
  - Acceso a una página de **detalle de evento**.
- Acceder a la sección de **preguntas frecuentes (FAQ)**.
- Revisar **Términos y Condiciones** y **Política de Privacidad**.
- **Suscribirse a la newsletter** introduciendo su email, que se almacena en un fichero en el servidor.

### 👤 Área privada (usuario registrado)

Tras registrarse y hacer login, el usuario puede:

- **Gestionar su perfil**:
  - Ver sus datos básicos (nombre, email, bio, deporte favorito, nivel…).
  - Editar parte de su información desde el frontend (con componente dedicado).
  - Cerrar sesión (limpieza de JWT y datos en `localStorage`).
  - Eliminar su cuenta desde el perfil.

- **Crear y gestionar eventos deportivos**:
  - Crear actividades indicando deporte, descripción, fecha, capacidad, ubicación (lat/long…).
  - Ver un detalle completo del evento, incluyendo:
    - Plazas ocupadas / máximas.
    - Creador/administrador del evento.
    - Enlace directo a **Google Maps** utilizando las coordenadas de la actividad.
  - Unirse a actividades de otros usuarios o abandonarlas.
  - Visualizar:
    - Eventos que **ha creado**.
    - Eventos a los que **se ha unido**.

- **Interacciones avanzadas**:
  - Reportar a otros usuarios.
  - (Preparado) sistema de rating de actividades (valoración con estrellas).

---

## 🧠 Lo que resuelve a nivel técnico

### Autenticación y seguridad

- Autenticación con **JSON Web Tokens (JWT)** usando `flask-jwt-extended`.
- Protección de rutas privadas en la API (`@jwt_required`) y consumo desde React con headers `Authorization`.
- Persistencia de sesión en `localStorage` con una clave dedicada para el token y otra para el usuario.
- Campos de seguridad en la base de datos:
  - `is_blocked` y contador de `reports` en el modelo de usuario.
  - Endpoints para **reportar** y **bloquear** usuarios.

### Recuperación y cambio de contraseña

- Flujo completo de *“olvidé mi contraseña”*:
  - Endpoint para solicitar recuperación: genera un token y envía un email con enlace.
  - Endpoint para resetear la contraseña a partir del token.
  - Endpoint adicional para **cambiar contraseña** desde la cuenta autenticada.
- Integración con **Flask-Mail** y configuración vía variables de entorno (`MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`).

### Modelo de datos y lógica de dominio

- Modelo `User` con:
  - Datos personales básicos.
  - Información deportiva (bio, deporte favorito, nivel).
  - Campos de administración (reportes, bloqueos).
- Modelo `Activity` con:
  - Título, deporte, descripción, fecha, capacidad máxima.
  - Ubicación (latitud, longitud).
  - Creador de la actividad.
- Relación **muchos-a-muchos** entre `User` y `Activity` mediante tabla intermedia:
  - Lista de usuarios que participan en cada actividad.
  - Lista de actividades a las que está apuntado cada usuario.
- Modelo de token para recuperación de contraseña.

### Frontend: estructura y estado

- SPA en **React + Vite** con:
  - Rutas públicas (home, about, eventos, FAQ, terms, privacy, login, register, reset…).
  - Rutas privadas protegidas para perfil y gestión de eventos.
- Gestión de estado global con **Context API + useReducer**:
  - Usuario actual.
  - Token JWT.
  - Listas de eventos creados / unidos.
- UI con **React Bootstrap** y algunos componentes de **Material UI** para tarjetas de eventos.
- Notificaciones de estado (exitoso / error) con **React Toastify**.
- Llamadas a la API encapsuladas y manejo de errores (con fallback de datos de demo para el listado de eventos).

---

## 🧱 Arquitectura del proyecto

Estructura resumida:

- Backend (Flask):
  - `src/app.py` → configuración de la app, CORS, JWT, mail, rutas y newsletter.
  - `src/api/models.py` → modelos de datos (User, Activity, etc.).
  - `src/api/commands.py` → comandos de utilidad (migraciones, datos de prueba…).
  - `src/api/utils.py`, `src/api/admin.py`, `src/api/routes.py` → utils, admin, rutas adicionales.
  - `src/newsletter/newsletter.txt` → almacenamiento de emails de suscripción.

- Frontend (React):
  - `src/front/main.jsx` → entrada principal de la app React.
  - `src/front/routes.jsx` → configuración de rutas.
  - `src/front/store.js` → Context + reducer global.
  - `src/front/components/` → Navbar, Footer, EventDetails, JoinedEvents, CreatedEvents, etc.
  - `src/front/pages/` → Home, About, Eventos, Profile, Login, Register, Forgot, Reset, Terms, Privacy, FAQ…

---

## ⚙️ Stack técnico

**Frontend**

- React
- Vite
- React Router
- Context API + useReducer
- React Bootstrap / Bootstrap
- Material UI (tarjetas de eventos)
- React Toastify

**Backend**

- Python 3.10+
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended (JWT)
- Flask-Mail (emails)
- Bcrypt / Werkzeug (hash de contraseñas)

**Infraestructura / otros**

- Variables de entorno vía `.env`
- `Pipenv` para gestión de dependencias de Python
- Soporte para despliegue en plataformas tipo Render
- Estructura preparada para usar PostgreSQL u otros motores compatibles

---

## 🚀 Cómo ejecutar el proyecto localmente

> Resumen rápido para que cualquiera pueda probar la app en local.

### 1. Backend (Flask API)

1. Instalar dependencias (Python):

       pipenv install

2. Crear archivo de entorno:

       cp .env.example .env

3. Configurar en `.env`:

   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
   - Opcional: `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`, `GOOGLE_MAPS_API_KEY`

4. Migrar base de datos:

       pipenv run migrate
       pipenv run upgrade

5. Levantar el servidor:

       pipenv run start

   Por defecto: `http://localhost:3001`

---

### 2. Frontend (React + Vite)

1. Instalar dependencias:

       npm install

2. Asegurarse de que `VITE_BACKEND_URL` en `.env` apunta al backend (por ejemplo `http://localhost:3001`).

3. Iniciar el servidor de desarrollo:

       npm run dev

   Por defecto: `http://localhost:3000`

---

## 🔮 Próximos pasos e ideas de mejora

- Completar la vista de **mapa interactivo** integrando completamente la API de Google Maps.
- Implementar un panel de **administración** para gestionar usuarios reportados / bloqueados.
- Añadir **tests automatizados** (unitarios e integrados) tanto en backend como en frontend.
- Mejorar el sistema de **valoraciones y comentarios** sobre eventos.

---

## 👋 Sobre mí

Soy **desarrollador Full Stack** orientado a producto, me gusta:

- Construir aplicaciones que realmente podrían usar usuarios reales.
- Diseñar flujos completos (desde la base de datos y la API hasta la experiencia de usuario en el navegador).
- Cuidar la arquitectura para que el código sea mantenible y escalable.

Si te interesa este proyecto o mi perfil, estaré encantado de hablar contigo 🙂  
Puedes contactarme a través de mi perfil de GitHub o LinkedIn.
