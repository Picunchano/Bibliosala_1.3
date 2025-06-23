# --- Archivo Actualizado y Mejorado: config.py ---

import sys
import os

# --- INICIO DE LA MODIFICACIÓN ---
# Esta lógica determina la ruta base de la aplicación, ya sea que se ejecute
# como un script .py o como un .exe "congelado" por cx_Freeze.

if getattr(sys, 'frozen', False):
    # Si la aplicación es un .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Si la aplicación es un script .py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# --- FIN DE LA MODIFICACIÓN ---


# --- Configuración de la Base de Datos ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'Prestamo_biblioteca',
    'port': 3306,
}

# --- Credenciales del Administrador por Defecto ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"


# --- INICIO DE LA MODIFICACIÓN ---
# Ahora construimos las rutas completas a los archivos usando la ruta base (BASE_DIR).
# Esto asegura que el programa siempre los encontrará.

ICON_PATH = os.path.join(BASE_DIR, "pictures", "icono.ico")
LOGO_PATH = os.path.join(BASE_DIR, "pictures", "transp.png")
SOUND_EFFECT_PATH = os.path.join(BASE_DIR, "sound", "ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.wav")
# --- FIN DE LA MODIFICACIÓN ---


# --- Configuración de Salas por Defecto ---
SALAS_DISPONIBLES_DEFAULT = [f"A{i}" for i in range(1, 15)]