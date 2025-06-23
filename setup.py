# --- Archivo Actualizado: setup.py ---

import sys
from cx_Freeze import setup, Executable

# --- Opciones de Construcción ---
build_exe_options = {
    "packages": [
        "os", "tkinter", "customtkinter", "mysql.connector",
        "bcrypt", "PIL", "datetime", "collections"
    ],
    "includes": [
        "user", "data_manager", "db_connection", "config_manager",
        "config", "constants", "ui_login", "ui_main_menu",
        "ui_nueva_reserva", "ui_ver_reservas", "ui_analisis_datos",
        "ui_log_desocupacion", "ui_settings", "ui_splash_screen", "ui_tutorial"
    ],
    # --- INICIO DE LA MODIFICACIÓN ---
    # Actualizamos esta sección para incluir los archivos desde sus carpetas correctas.
    "include_files": [
        ("pictures/icono.ico", "pictures/icono.ico"),      # Incluye el ícono desde 'pictures'
        ("pictures/transp.png", "pictures/transp.png"),    # Incluye la imagen desde 'pictures'
        ("settings.json", "settings.json"),                # Incluye el archivo de configuración
        ("sound", "sound")                                 # Incluye la carpeta 'sound' completa
    ],
    # --- FIN DE LA MODIFICACIÓN ---
    "excludes": ["PyQt5", "PyQt6", "PySide2", "PySide6", "numpy", "pandas"],
}

# --- Configuración Base ---
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# --- Definición del Setup ---
setup(
    name="Bibliosala",
    version="1.2", # Actualizamos la versión
    description="Sistema de Gestión de Salas de Biblioteca",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main_app.py",
            base=base,
            # --- INICIO DE LA MODIFICACIÓN ---
            # Apuntamos a la ruta correcta del ícono para el .exe
            icon="pictures/icono.ico",
            # --- FIN DE LA MODIFICACIÓN ---
            target_name="Bibliosala.exe"
        )
    ]
)