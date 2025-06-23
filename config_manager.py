# --- config_manager.py (NUEVO) ---
import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound_enabled": True, #
    "color_theme": "dark-blue" # Opciones: "blue", "dark-blue", "green"
}

def load_settings():
    """
    Carga la configuración desde settings.json. Si no existe o está corrupto,
    crea/regenera el archivo con valores por defecto.
    """
    if not os.path.exists(SETTINGS_FILE): #
        with open(SETTINGS_FILE, 'w') as f: #
            json.dump(DEFAULT_SETTINGS, f, indent=4) #
        return DEFAULT_SETTINGS #
    try:
        with open(SETTINGS_FILE, 'r') as f: #
            return json.load(f) #
    except (json.JSONDecodeError, IOError): #
        # Si el archivo está corrupto o hay un error de E/S, se regenera
        print(f"Advertencia: Archivo de configuración '{SETTINGS_FILE}' corrupto o ilegible. Regenerando con valores por defecto.")
        with open(SETTINGS_FILE, 'w') as f: #
            json.dump(DEFAULT_SETTINGS, f, indent=4) #
        return DEFAULT_SETTINGS #

def save_settings(settings):
    """Guarda la configuración proporcionada en settings.json."""
    try:
        with open(SETTINGS_FILE, 'w') as f: #
            json.dump(settings, f, indent=4) #
    except IOError as e:
        print(f"Error al guardar la configuración en '{SETTINGS_FILE}': {e}")

# Cargar la configuración al iniciar el módulo
current_settings = load_settings() #