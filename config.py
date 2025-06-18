# config.py

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'Prestamo_biblioteca',
    'port': 3306,
}

# Define un usuario administrador inicial que se creará una sola vez.
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

LOGO_PATH = "logo.png"

# ¡NUEVO! Las salas por defecto ahora serán de A1 a A14
SALAS_DISPONIBLES_DEFAULT = [f"A{i}" for i in range(1, 15)] # Genera A1, A2, ..., A14