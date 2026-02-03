# 🌍 GoTrip - Sistema de Gestión de Reservas

Este es un proyecto **monolítico** desarrollado con **FastAPI** para la gestión de reservas de una agencia de viajes. El objetivo es demostrar el uso de un CRUD completo utilizando **SQL directo** (sin ORM) y validaciones avanzadas con **Pydantic**, cumpliendo con los requisitos del taller de **2º de DAW**.

## 🛠️ Tecnologías utilizadas

* **Backend:** FastAPI (Python 3.12+)
* **Frontend:** Jinja2 Templates, Bootstrap 5, Bootstrap Icons
* **Base de Datos:** MySQL (Sentencias SQL nativas)
* **Validación:** Pydantic
* **Servidor:** Uvicorn

---

## 📂 Estructura del Proyecto

```text
GOTRIP/
├── app/                  # Núcleo de la aplicación
│   ├── static/           # CSS, Imágenes y JavaScript de cliente
│   ├── templates/        # Plantillas HTML dinámicas (Jinja2)
│   ├── database.py       # Conexión a MySQL y funciones SQL
│   └── main.py           # Rutas, controladores y lógica principal
├── docs/                 # Documentación, capturas y script SQL
├── venv/                 # Entorno virtual de Python
├── .env                  # Variables de entorno (Credenciales DB)
├── requirements.txt      # Listado de dependencias del proyecto
└── README.md             # Guía de instalación y uso

🚀 Instalación y Puesta en Marcha
Sigue estos pasos para ejecutar el proyecto en tu máquina local:

1. Preparar el entorno
# Crear el entorno virtual
python -m venv venv

# Activar el entorno (Windows)
.\venv\Scripts\activate

# Instalar todas las librerías necesarias
pip install -r requirements.txt

2. Configurar la Base de Datos
Accede a tu gestor de base de datos (phpMyAdmin, MySQL Workbench, etc.).

Importa y ejecuta el script situado en docs/init_db.sql.

Configura tus credenciales en el archivo .env:
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=go_trip

3. Lanzar la aplicación

# Ejecutar desde la carpeta raíz del proyecto
uvicorn app.main:app --reload

La aplicación estará disponible en: http://127.0.0.1:8000

📋 Características Técnicas
Arquitectura Monolítica: El backend y el frontend están integrados, sirviendo HTML renderizado desde el servidor mediante Jinja2.

Acceso a Datos: Uso estricto de SQL directo para las operaciones CRUD, manteniendo la lógica separada en un módulo independiente.

Validación en el Backend: Implementación de modelos Pydantic para asegurar que los datos de las reservas sean coherentes y seguros.

Documentación Interactiva: Integración nativa con Swagger UI disponible en la ruta /docs.

Interfaz Responsiva: Diseño adaptado a diferentes dispositivos gracias a Bootstrap 5.

✒️ Autor
Sara Reina - Estudiante de 2º DAW
