README.md
Bibliosala - Sistema de Gestión de Salas
Bibliosala es una aplicación de escritorio desarrollada en Python con CustomTkinter para la gestión eficiente de reservas de salas de estudio en una biblioteca. Permite a los administradores registrar, visualizar y analizar el uso de las salas, ofreciendo una interfaz gráfica moderna e intuitiva.
Características Principales
Autenticación Segura: Sistema de inicio de sesión para administradores.
Gestión de Reservas: Creación, visualización y eliminación de reservas de salas.
Base de Datos MySQL: Toda la información se almacena de forma persistente en una base de datos MySQL.
Análisis de Datos: Módulo de estadísticas para visualizar salas más ocupadas, alumnos más activos y horarios de mayor demanda.
Registro Histórico: Ventana para consultar las últimas reservas que han finalizado.
Configuración Personalizable: Permite cambiar el tema de color de la aplicación y activar/desactivar los efectos de sonido.
Tutorial Integrado: Una guía dentro de la aplicación que explica paso a paso cómo usar cada una de sus funciones.
Uso del Programa
1. Inicio y Autenticación
Al ejecutar la aplicación, se mostrará una pantalla de carga seguida de una ventana de inicio de sesión. Debes ingresar las credenciales de administrador para acceder al sistema.
Usuario por defecto: admin 
Contraseña por defecto: 1234 
2. Menú Principal
Una vez iniciada la sesión, se presenta el menú principal, que es el centro de navegación de la aplicación. Desde aquí puedes acceder a todas las funcionalidades a través de los siguientes botones:
Nueva Reserva: Abre el formulario para registrar un nuevo préstamo de sala.
Ver Reservas: Muestra una tabla con todas las reservas activas y permite eliminarlas.
Registro de Desocupación: Muestra un historial de las últimas reservas finalizadas.
Análisis de Datos: Abre la ventana de estadísticas de uso.
Configuración: Permite personalizar la apariencia y el sonido de la aplicación.
Tutorial: Muestra una guía detallada sobre cómo utilizar el programa.


3. Funcionalidades Detalladas
Crear una Nueva Reserva:
Ingresa el RUT del alumno. Si ya existe, sus datos se cargarán automáticamente. Si es nuevo, deberás completar los campos de nombre, apellido, carrera y email.
Selecciona la sala, la fecha y las horas de inicio y fin.
Haz clic en "Guardar Reserva" para confirmar.
Gestionar Reservas Existentes:
En la ventana "Ver Reservas", puedes ver toda la información de los préstamos activos.
Para eliminar una o más reservas, haz clic sobre sus filas en la tabla para seleccionarlas.
Presiona el botón "Eliminar Seleccionadas" y confirma la acción.
Personalizar la Aplicación:


En "Configuración", puedes marcar o desmarcar la casilla para habilitar los sonidos.
Puedes cambiar el "Tema de Color" usando el menú desplegable.
Los cambios se guardan al hacer clic en "Guardar y Aplicar".

Estructura del Código
El proyecto está organizado en módulos, cada uno con una responsabilidad clara:
main_app.py: Es el punto de entrada principal. Inicia la aplicación, gestiona la secuencia de arranque (pantalla de carga -> login -> menú) y contiene la ventana principal. 6666
config.py: Archivo central que almacena variables de configuración importantes, como las credenciales de la base de datos, el usuario administrador por defecto y rutas a archivos. 7
db_connection.py: Contiene toda la lógica de bajo nivel para interactuar con la base de datos MySQL. Se encarga de establecer conexiones, ejecutar consultas (SELECT, INSERT, DELETE, etc.) y configurar el esquema de la base de datos la primera vez que se ejecuta. 888888888
data_manager.py: Actúa como una capa intermedia (un "gestor de datos") entre la interfaz de usuario y la base de datos. Procesa los datos crudos de la base de datos para que la UI pueda mostrarlos fácilmente y viceversa. 999999999
Módulos de UI (ui_*.py): Cada archivo se encarga de una ventana o componente visual específico de la aplicación.


ui_splash_screen.py: La pantalla de carga inicial.
ui_login.py: La ventana de inicio de sesión.
ui_main_menu.py: El menú principal con los botones de navegación.
ui_nueva_reserva.py: El formulario para crear una nueva reserva.
ui_ver_reservas.py: La tabla para visualizar y eliminar reservas.
ui_analisis_datos.py: La ventana que muestra las estadísticas.
ui_log_desocupacion.py: La ventana con el historial de salas desocupadas.
ui_settings.py: La ventana para configurar el tema y el sonido.
ui_tutorial.py: La ventana con la guía de uso del programa.
Requisitos
Para ejecutar este proyecto, necesitas tener instaladas las siguientes librerías de Python:
customtkinter
mysql-connector-python
bcrypt
Puedes instalarlas usando pip:
pip install customtkinter mysql-connector-python bcrypt




Instalación y Ejecución
Asegúrate de tener un servidor de MySQL en funcionamiento.
Modifica el archivo config.py con tus credenciales de la base de datos (host, usuario, contraseña, etc.).
Coloca los archivos de la aplicación en una carpeta.
Ejecuta el programa desde tu terminal
La primera vez que se ejecute, el programa creará la base de datos Prestamo_biblioteca y las tablas necesarias si no existen.

