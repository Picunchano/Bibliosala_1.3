# db_connection.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, ADMIN_USERNAME, ADMIN_PASSWORD, SALAS_DISPONIBLES_DEFAULT # Asegúrate de importar SALAS_DISPONIBLES_DEFAULT
from user import Usuario # Importa la clase Usuario

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_db_connection(conn):
    """Cierra la conexión a la base de datos si está abierta."""
    if conn and conn.is_connected():
        conn.close()

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """
    Ejecuta una consulta SQL.
    - query: La cadena de la consulta SQL.
    - params: Una tupla o lista de parámetros para la consulta.
    - fetch_one: Si es True, devuelve una sola fila.
    - fetch_all: Si es True, devuelve todas las filas.
    - commit: Si es True, guarda los cambios en la base de datos.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor(dictionary=True) # Ya usa dictionary=True aquí
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return True
        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        return True # Para consultas que no devuelven datos (ej. INSERT, UPDATE)
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        conn.rollback() # Deshace cualquier cambio si hay un error
        return False
    finally:
        if 'cursor' in locals() and cursor: # Asegura que el cursor exista antes de intentar cerrarlo
            cursor.close()
        close_db_connection(conn)

def insert_default_salas(cursor):
    """Inserta salas por defecto en la tabla Sala si no existen, basándose en SALAS_DISPONIBLES_DEFAULT."""
    print("Verificando e insertando salas por defecto...")
    
    default_salas_data = []
    for i, sala_numero in enumerate(SALAS_DISPONIBLES_DEFAULT):
        capacidad = 10 # Capacidad por defecto para todas
        tipo_sala = "Estudio" # Tipo por defecto para todas
        descripcion = f"Sala {sala_numero} de {tipo_sala.lower()}."
        
        # Puedes ajustar la capacidad, tipo y descripción de forma más específica si lo deseas.
        # Por ejemplo:
        if sala_numero in ["A1", "A2", "A3"]:
            capacidad = 5
            tipo_sala = "Individual"
        elif sala_numero in ["A4", "A5", "A6"]:
            capacidad = 15
            tipo_sala = "Grupal"
        # etc.

        default_salas_data.append({
            "numero_sala": sala_numero,
            "capacidad": capacidad,
            "tipo_sala": tipo_sala,
            "descripcion": descripcion
        })

    for sala in default_salas_data:
        try:
            # Ahora que el cursor es de diccionario, usamos un alias para COUNT(*) y accedemos por nombre
            cursor.execute("SELECT COUNT(*) AS count_salas FROM Sala WHERE numero_sala = %s", (sala['numero_sala'],))
            if cursor.fetchone()['count_salas'] == 0: # ¡CORREGIDO! Acceso por nombre de columna
                cursor.execute(
                    "INSERT INTO Sala (numero_sala, capacidad, tipo_sala, descripcion) VALUES (%s, %s, %s, %s)",
                    (sala['numero_sala'], sala['capacidad'], sala['tipo_sala'], sala['descripcion'])
                )
                print(f"Sala '{sala['numero_sala']}' insertada.")
            else:
                print(f"Sala '{sala['numero_sala']}' ya existe. Saltando inserción.")
        except Error as e:
            print(f"Error al insertar sala '{sala['numero_sala']}': {e}")


def setup_database():
    """
    Configura la base de datos y sus tablas, incluyendo la creación
    de la base de datos si no existe y un usuario administrador por defecto.
    """
    conn = get_db_connection()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos para la configuración.")
        return False

    # ¡CORREGIDO! Ahora el cursor de setup_database también es de diccionario
    cursor = conn.cursor(dictionary=True) 
    db_name = DB_CONFIG['database']

    try:
        # Intentar seleccionar la base de datos
        cursor.execute(f"USE {db_name}")
        print(f"Conexión a la base de datos MySQL exitosa a {db_name} en {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    except Error as e:
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            # Si la base de datos no existe, crearla
            print(f"La base de datos '{db_name}' no existe. Creándola...")
            try:
                temp_conn = mysql.connector.connect(
                    host=DB_CONFIG['host'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    port=DB_CONFIG['port']
                )
                temp_cursor = temp_conn.cursor() # Este cursor está bien porque solo se usa para CREATE DATABASE
                temp_cursor.execute(f"CREATE DATABASE {db_name}")
                temp_cursor.close()
                temp_conn.close()
                print(f"Base de datos '{db_name}' creada exitosamente.")
                # ¡CORREGIDO! Re-inicializar el cursor principal como diccionario después de reconectar
                conn.reconnect()
                cursor = conn.cursor(dictionary=True)
                cursor.execute(f"USE {db_name}")
            except Error as create_db_error:
                print(f"Error al crear la base de datos: {create_db_error}")
                close_db_connection(conn)
                return False
        else:
            print(f"Error al usar la base de datos: {e}")
            close_db_connection(conn)
            return False

    try:
        # Crear tabla Usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                timestamp_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tabla 'Usuario' verificada/creada.")

        # Insertar usuario administrador si no existe
        # Ahora que el cursor es de diccionario, usamos un alias para COUNT(*) y accedemos por nombre
        cursor.execute("SELECT COUNT(*) AS count_users FROM Usuario WHERE username = %s", (ADMIN_USERNAME,))
        if cursor.fetchone()['count_users'] == 0: # ¡CORREGIDO! Acceso por nombre de columna
            admin_user = Usuario.crear_nuevo_usuario(ADMIN_USERNAME, ADMIN_PASSWORD)
            cursor.execute("INSERT INTO Usuario (username, password_hash) VALUES (%s, %s)",
                           (admin_user.username, admin_user.password_hash))
            conn.commit()
            print("Usuario administrador por defecto creado.")
        else:
            print("Usuario administrador ya existe.") # Mensaje para cuando ya está creado

        # Crear tabla Sala
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sala (
                id_sala INT AUTO_INCREMENT PRIMARY KEY,
                numero_sala VARCHAR(10) UNIQUE NOT NULL,
                capacidad INT NOT NULL,
                tipo_sala VARCHAR(50) NOT NULL,
                descripcion TEXT,
                timestamp_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tabla 'Sala' verificada/creada.")

        # Insertar salas por defecto después de crear la tabla Sala
        insert_default_salas(cursor)
        conn.commit() # Asegura que las salas insertadas se guarden

        # Crear tabla Alumno
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alumno (
                rut_alumno VARCHAR(12) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                carrera VARCHAR(100),
                email VARCHAR(100),
                timestamp_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tabla 'Alumno' verificada/creada.")

        # Crear tabla Prestamo_Sala
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Prestamo_Sala (
                idPrestamo INT AUTO_INCREMENT PRIMARY KEY,
                rut_alumno VARCHAR(12) NOT NULL,
                id_sala INT NOT NULL,
                fecha_prestamo DATE NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                individual_o_grupal VARCHAR(10) NOT NULL,
                timestamp_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rut_alumno) REFERENCES Alumno(rut_alumno),
                FOREIGN KEY (id_sala) REFERENCES Sala(id_sala)
            )
        """)
        print("Tabla 'Prestamo_Sala' verificada/creada.")

        conn.commit()
        print("Esquema de la base de datos configurado exitosamente.")
        return True

    except Error as e:
        print(f"Error al configurar el esquema de la base de datos: {e}")
        conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        close_db_connection(conn)