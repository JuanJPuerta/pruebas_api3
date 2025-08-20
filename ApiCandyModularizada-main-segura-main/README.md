# implantacion_api

# Proyecto ApiCandy Modularizada

## Tabla de Contenidos
- [Descripción](#descripción)
- [Clases con pruebas unitarias](#clases-con-pruebas-unitarias)
- [Funcionalidades](#funcionalidades)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Despliegue](#despliegue)
- [Ejecución de pruebas unitarias](#ejecución-de-pruebas-unitarias)


---

## Descripción del Proyecto

CandySoft es un software desarrollado para el spa Candy Nails Spa el cual cuenta con un backend desarrollado en Python con Django REST Framework(DRF) este software permite la gestión integral del sistema administrativo y comercial del negocio.  
El proyecto está modularizado para facilidad de mantenimiento y escalabilidad, con validaciones y control de permisos.

---

## Tecnologías utilizadas

- Python 3.x
- Django 5.x
- Django REST Framework 3.16.0
- Pytest 7.4.0 para pruebas
- MySQL y mysqlclient para la base de datos
- MySQL Workbench (para administración de base de datos)
- django-cors-headers 4.7.0 para manejo de CORS 
- djangorestframework_simplejwt 5.5.0 para autenticación JWT
- python-dotenv y python-decouple para gestión de variables de entorno

Otros paquetes de soporte que puedes revisar en el archivo requirements.txt

---

## Funcionalidades

- Administración de roles y permisos con el módulo rol.
- Manejo de usuarios y autenticación con el módulo usuario.
- Sistema de recuperación de autenticación con el módulo authrecuperacion.
- Gestión de proveedores a través del módulo proveedor.
- Gestión integral del abastecimiento, controlando insumos y su suministro.
- Control de compra de insumos.
- Administración completa de insumos incluyendo stock y marcas.
- Gestión y administración de los servicios prestados.
- Gestión y control de la actividad de los manicuristas dentro del sistema.
- Gestión y control de citas con agendamiento, estados y servicios asociados.

---

## Clases con pruebas unitarias

Se incluyen pruebas unitarias automáticas en Pytest para asegurar el correcto funcionamiento en las siguientes clases de modelo:

- **Usuario:** Manejo de creación, actualización y validación de usuarios con roles.
- **Cliente:** Gestión del estado, datos personales y vinculación con el usuario.
- **Insumo:** Control de stock, cambios de estado automáticos y validaciones.
- **Marca:** Validaciones sobre la entidad de marca para insumos.
- **Servicio:** Manejo de servicios ofrecidos, cambio de estado y control de citas asociadas.

Las pruebas cubren validaciones, creación, actualización, destrucción condicional y acciones personalizadas.

## Despliegue

### Requisitos previos

- Python 3.x instalado
- MySQL servidor y cliente instalados
- Git instalado

### Pasos para desplegar

1. - Descargar el proyecto comprimido .zip desde el repositorio
   - Descomprimir el proyecto
   - Abrir Visual Studio Code y seleccionar la carpeta descomprimida del proyecto


2. Crear y activar entorno virtual (opcional pero recomendado):
- ve a la terminar en visual estudio e ingresa los siguientes scripts dependiendo de tu sistema operativo: 

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows


3. Instalar dependencias:
- En la terminal en la ubicado en la carpeta que contiene el manage.py, colocar el siguiente script: 

pip install -r requirements.txt

4. Crear la base de datos en MySQL:
- En una consulta de MYSQL colocar el siguiente script:
CREATE DATABASE IF NOT EXISTS CandySoftApi2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

5. Configurar la conexión a base de datos en `settings.py` o variables de entorno apuntando a la base creada.

6. Ejecutar migraciones para crear las tablas necesarias:
- En la terminal de VSC ejecutar el siguiente script:

python manage.py migrate

7. Ejecutar servidor local:
python manage.py runserver


---

## Ejecución de pruebas unitarias

Para ejecutar los tests con Pytest y validar el correcto funcionamiento:

1. Asegúrate de tener el entorno virtual activado y dependencias instaladas.

2. Ejecuta el siguiente comando en la raíz del proyecto (donde está `manage.py`):

pytest