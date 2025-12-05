# MeetFit

MeetFit es una plantilla/proyecto que combina un frontend en React con un backend en Python + Flask, permitiendo crear aplicaciones web completas (full-stack). Compatible con entornos como Gitpod/Codespaces para facilitar el desarrollo desde la nube.

---

## 🛠 Características

- Frontend con **React.js**
- Backend con **Python + Flask** y **SQLAlchemy**
- Gestión de dependencias backend con **Pipenv**
- Preparado para despliegue (Render / Heroku)
- Soporte para archivo **.env**
- Estructura modular para construir APIs REST
- Compatible con entornos de desarrollo en la nube (Gitpod / Codespaces)

---

## 🚀 Instalación y uso

### Backend

**Instalación y arranque:**
pipenv install
cp .env.example .env
pipenv run migrate
pipenv run upgrade
pipenv run start


**Crear usuarios de prueba (opcional):**
flask insert-test-users 5


---

### Frontend

**Instalación y ejecución:**
npm install
npm run start

---

## ⚙️ Estructura del proyecto

/src → Código del frontend (React)
/dist → Build final del frontend
/src/api → Backend (Flask: rutas, modelos, controladores)
/public → Archivos estáticos accesibles públicamente
.env.example → Ejemplo de configuración de entorno
Docker/devcontainer → Configuración para contenedores



## 📦 Dependencias principales

- Python 3.10+
- Flask
- SQLAlchemy
- Pipenv
- Node.js + NPM
- React.js

---

## 🎯 Casos de uso

Este proyecto es ideal para:

- Construir aplicaciones web **full-stack**
- Crear **APIs REST** y consumirlas con React
- Prototipos rápidos de productos digitales
- Practicar integración frontend / backend
- Deploy sencillo en la nube

---

## 🤝 Contribuciones

1. Haz un **fork** del repositorio
2. Crea una rama para tu mejora o corrección
3. Mantén un estilo de código consistente
4. Abre un **pull request**

---


## ℹ️ Créditos

Basado en estructura de proyectos de 4Geeks Academy.
