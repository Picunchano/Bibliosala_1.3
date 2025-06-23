# --- Archivo Completo: db_connection.py ---
# Este archivo contiene toda la lógica para la conexión a la base de datos,
# ejecución de consultas y la configuración inicial del esquema y datos por defecto.

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, ADMIN_USERNAME, ADMIN_PASSWORD, SALAS_DISPONIBLES_DEFAULT # 
import bcrypt # 

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG) # 
        return conn # 
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}") # 
        return None # 

def close_db_connection(conn):
    """Cierra la conexión a la base de datos si está abierta."""
    if conn and conn.is_connected(): # 
        conn.close() # 

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """
    Ejecuta una consulta SQL genérica.
    - query: La cadena de la consulta SQL. 
    - params: Una tupla o lista de parámetros para la consulta. 
    - fetch_one: Si es True, devuelve una sola fila. 
    - fetch_all: Si es True, devuelve todas las filas. 
    - commit: Si es True, guarda los cambios en la base de datos. 
    """
    conn = get_db_connection() # 
    if conn is None: # 
        return False # 
    
    # Usar un cursor de tipo diccionario para acceder a las columnas por su nombre
    cursor = conn.cursor(dictionary=True) # 
    try:
        cursor.execute(query, params) # 
        if commit: # 
            conn.commit() # 
            return True # 
        if fetch_one: # 
            return cursor.fetchone() # 
        if fetch_all: # 
            return cursor.fetchall() # 
        return True
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}") # 
        conn.rollback() # 
        return False # 
    finally:
        if 'cursor' in locals() and cursor: # 
            cursor.close() # 
        close_db_connection(conn) # 

def insert_default_salas(cursor):
    """
    Inserta salas por defecto en la tabla Sala si no existen. 
    """
    print("Verificando e insertando salas por defecto...") # 
    
    default_salas_data = [] # 
    for i, sala_numero_raw in enumerate(SALAS_DISPONIBLES_DEFAULT): # 
        sala_numero = sala_numero_raw # 
        capacidad = 10 # 
        tipo_sala = "Estudio" # 
        descripcion = f"Sala {sala_numero} de {tipo_sala.lower()}." # 
        
        # Se puede personalizar la capacidad y tipo de sala
        if sala_numero in ["A1", "A2", "A3"]: # 
            capacidad = 5 # 
            tipo_sala = "Individual" # 
        elif sala_numero in ["A4", "A5", "A6"]: # 
            capacidad = 15 # 
            tipo_sala = "Grupal" # 

        default_salas_data.append({ # 
            "numero_sala": sala_numero, # 
            "capacidad": capacidad, # 
            "tipo_sala": tipo_sala, # 
            "descripcion": descripcion # 
        })

    for sala in default_salas_data: # 
        try:
            cursor.execute("SELECT COUNT(*) AS count_salas FROM Sala WHERE numero_sala = %s", (sala['numero_sala'],)) # 
            if cursor.fetchone()['count_salas'] == 0: # 
                cursor.execute(
                    "INSERT INTO Sala (numero_sala, capacidad, tipo_sala, descripcion) VALUES (%s, %s, %s, %s)", # 
                    (sala['numero_sala'], sala['capacidad'], sala['tipo_sala'], sala['descripcion']) # 
                )
                print(f"Sala '{sala['numero_sala']}' insertada.") # 
            else:
                print(f"Sala '{sala['numero_sala']}' ya existe. Saltando inserción.") # 
        except Error as e:
            print(f"Error al insertar sala '{sala['numero_sala']}': {e}") # 

def setup_database():
    """
    Configura la base de datos, tablas y datos iniciales.
    Crea la DB si no existe y añade un usuario admin y salas por defecto.
    """
    conn = get_db_connection()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos para la configuración.")
        return False

    cursor = conn.cursor(dictionary=True)
    db_name = DB_CONFIG['database']

    try:
        cursor.execute(f"USE {db_name}")
        print(f"Conexión a la base de datos MySQL exitosa a {db_name} en {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    except Error as e:
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print(f"La base de datos '{db_name}' no existe. Creándola...")
            try:
                temp_conn = mysql.connector.connect(
                    host=DB_CONFIG['host'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    port=DB_CONFIG['port']
                )
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute(f"CREATE DATABASE {db_name}")
                temp_cursor.close()
                temp_conn.close()
                print(f"Base de datos '{db_name}' creada exitosamente.")
                
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                timestamp_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """) # 
        print("Tabla 'Usuario' verificada/creada.") # 

        cursor.execute("SELECT COUNT(*) AS count_users FROM Usuario WHERE username = %s", (ADMIN_USERNAME,)) # 
        if cursor.fetchone()['count_users'] == 0: # 
            print(f"Creando usuario administrador por defecto: {ADMIN_USERNAME}")
            hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO Usuario (username, password_hash) VALUES (%s, %s)",
                           (ADMIN_USERNAME, hashed_password))
            print("Usuario administrador por defecto creado.") # 
        else:
            print("Usuario administrador ya existe.") # 

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sala (
                id_sala INT AUTO_INCREMENT PRIMARY KEY,
                numero_sala VARCHAR(10) UNIQUE NOT NULL,
                capacidad INT NOT NULL,
                tipo_sala VARCHAR(50) NOT NULL,
                descripcion TEXT,
                timestamp_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """) # 
        print("Tabla 'Sala' verificada/creada.") # 

        insert_default_salas(cursor) # 
        conn.commit() # 

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alumno (
                rut_alumno VARCHAR(12) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                carrera VARCHAR(100),
                email VARCHAR(100),
                timestamp_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """) # 
        print("Tabla 'Alumno' verificada/creada.") # 

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
        """) # 
        print("Tabla 'Prestamo_Sala' verificada/creada.") # 

        conn.commit() # 
        print("Esquema de la base de datos configurado exitosamente.") # 
        return True # 

    except Error as e:
        print(f"Error al configurar el esquema de la base de datos: {e}") # 
        conn.rollback() # 
        return False # 
    finally:
        if cursor:
            cursor.close() # 
        close_db_connection(conn) #