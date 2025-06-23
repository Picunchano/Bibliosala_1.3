# --- Archivo Actualizado y Corregido: data_manager.py ---
import datetime
import sys
import bcrypt
from mysql.connector import Error
from db_connection import execute_query, get_db_connection, close_db_connection
from config import SALAS_DISPONIBLES_DEFAULT, SOUND_EFFECT_PATH
from user import Usuario
from config_manager import current_settings

# Lógica para winsound multiplataforma
if sys.platform == "win32":
    import winsound
else:
    def placeholder_function(*args, **kwargs):
        pass
    winsound = type('winsound', (), {'PlaySound': placeholder_function})

# --- INICIO DE LA MODIFICACIÓN ---
def validate_user(username, password):
    """
    Valida las credenciales de un usuario.
    Ahora incluye una verificación de mayúsculas y minúsculas para el nombre de usuario.
    """
    # 1. La consulta a la DB sigue siendo case-insensitive, lo cual es útil para encontrar al usuario.
    query = "SELECT id_usuario, username, password_hash FROM Usuario WHERE username = %s"
    user_data = execute_query(query, (username,), fetch_one=True)

    if user_data:
        # 2. SEGUNDA VERIFICACIÓN: Comparamos el usuario guardado con el introducido.
        #    Esta comparación en Python SÍ distingue mayúsculas y minúsculas.
        stored_username = user_data.get('username')
        if stored_username != username:
            # Si el usuario introdujo "ADMIN" pero en la DB está "admin", no coinciden.
            # Se rechaza el inicio de sesión.
            return None

        # 3. Si los nombres de usuario coinciden exactamente, procedemos a verificar la contraseña.
        if 'password_hash' in user_data:
            stored_hash = user_data['password_hash'].encode('utf-8')
            provided_password = password.encode('utf-8')

            if bcrypt.checkpw(provided_password, stored_hash):
                # El usuario y la contraseña son correctos.
                return Usuario(id_usuario=user_data['id_usuario'], username=user_data['username'], role='user')

    # Si el usuario no se encontró, no coincidió el case, o la contraseña fue incorrecta.
    return None
# --- FIN DE LA MODIFICACIÓN ---

def play_sound_if_enabled():
    """
    Reproduce un archivo de sonido .wav si la opción de sonido está habilitada.
    """
    if current_settings.get("sound_enabled", True):
        if sys.platform == "win32":
            try:
                winsound.PlaySound(SOUND_EFFECT_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                print(f"Aviso: No se pudo reproducir el archivo de sonido desde '{SOUND_EFFECT_PATH}'. Error: {e}")

# (El resto de las funciones en este archivo no necesitan cambios)

def get_all_reservations():
    query = """
    SELECT ps.idPrestamo, a.rut_alumno AS RUTAlumno, a.nombre AS NombreAlumno,
           a.apellido AS ApellidoAlumno, a.carrera AS CarreraAlumno, a.email AS EmailAlumno,
           s.numero_sala AS NumeroSala, ps.fecha_prestamo, ps.hora_inicio, ps.hora_fin,
           ps.individual_o_grupal
    FROM Prestamo_Sala ps
    JOIN Alumno a ON ps.rut_alumno = a.rut_alumno
    JOIN Sala s ON ps.id_sala = s.id_sala
    ORDER BY ps.fecha_prestamo DESC, ps.hora_inicio DESC
    """
    reservas = execute_query(query, fetch_all=True)
    if not reservas:
        return []

    processed_reservas = []
    for r in reservas:
        nombre_completo = f"{r.get('NombreAlumno', '')} {r.get('ApellidoAlumno', '')}".strip()
        hora_inicio_str = str(r.get('hora_inicio')) if r.get('hora_inicio') else 'N/A'
        hora_fin_str = str(r.get('hora_fin')) if r.get('hora_fin') else 'N/A'
        processed_reservas.append({
            'id_prestamo': r.get('idPrestamo'),
            'RUTAlumno': r.get('RUTAlumno', 'N/A'),
            'NombreAlumnoCompleto': nombre_completo,
            'CarreraAlumno': r.get('CarreraAlumno', 'N/A'),
            'EmailAlumno': r.get('EmailAlumno', 'N/A'),
            'NumeroSala': r.get('NumeroSala', 'N/A'),
            'FechaPrestamo': r.get('fecha_prestamo').strftime('%d/%m/%Y') if r.get('fecha_prestamo') else 'N/A',
            'HoraInicio': hora_inicio_str,
            'HoraFin': hora_fin_str,
            'IndividualOGrupal': r.get('individual_o_grupal', 'N/A')
        })
    return processed_reservas

def guardar_reserva(datos_reserva: dict):
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        rut_alumno = datos_reserva['RUTAlumno']
        nombre_alumno = datos_reserva['Nombre']
        apellido_alumno = datos_reserva['Apellido']
        carrera_alumno = datos_reserva['Carrera']
        email_alumno = datos_reserva['Email']
        cursor.execute("SELECT COUNT(*) FROM Alumno WHERE rut_alumno = %s", (rut_alumno,))
        if cursor.fetchone()[0] == 0:
            insert_alumno_query = "INSERT INTO Alumno (rut_alumno, nombre, apellido, carrera, email) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_alumno_query, (rut_alumno, nombre_alumno, apellido_alumno, carrera_alumno, email_alumno))
            conn.commit()
        
        numero_sala = datos_reserva['NumeroSala'].replace('Sala ', '')
        cursor.execute("SELECT id_sala FROM Sala WHERE numero_sala = %s", (numero_sala,))
        sala_result = cursor.fetchone()
        if not sala_result:
            return False
        id_sala = sala_result[0]

        fecha_prestamo = datetime.datetime.strptime(datos_reserva['FechaPrestamo'], "%d/%m/%Y").date()
        hora_inicio = datetime.datetime.strptime(datos_reserva['HoraInicio'], "%H:%M:%S").time()
        hora_fin = datetime.datetime.strptime(datos_reserva['HoraFin'], "%H:%M:%S").time()
        individual_o_grupal = datos_reserva['IndividualOGrupal']

        insert_reserva_query = "INSERT INTO Prestamo_Sala (rut_alumno, id_sala, fecha_prestamo, hora_inicio, hora_fin, individual_o_grupal) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_reserva_query, (rut_alumno, id_sala, fecha_prestamo, hora_inicio, hora_fin, individual_o_grupal))
        conn.commit()
        play_sound_if_enabled()
        return True

    except Error as e:
        print(f"Error al guardar la reserva: {e}")
        conn.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_db_connection(conn)


def eliminar_reservas_por_timestamps(ids_prestamo: list):
    if not ids_prestamo:
        return False
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        placeholders = ', '.join(['%s'] * len(ids_prestamo))
        delete_query = f"DELETE FROM Prestamo_Sala WHERE idPrestamo IN ({placeholders})"
        cursor.execute(delete_query, tuple(ids_prestamo))
        conn.commit()
        play_sound_if_enabled()
        return True
    except Error as e:
        print(f"Error al eliminar reservas: {e}")
        conn.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_db_connection(conn)


def cargar_salas_disponibles():
    query = "SELECT numero_sala FROM Sala ORDER BY numero_sala"
    salas = execute_query(query, fetch_all=True)
    if not salas:
        return [s.replace('A', 'Sala A') for s in SALAS_DISPONIBLES_DEFAULT]
    return [s['numero_sala'] for s in salas]

def cargar_reservas_finalizadas():
    query = """
    SELECT a.nombre AS NombreAlumno, a.apellido AS ApellidoAlumno, s.numero_sala AS NumeroSala,
           ps.fecha_prestamo, ps.hora_fin
    FROM Prestamo_Sala ps
    JOIN Alumno a ON ps.rut_alumno = a.rut_alumno
    JOIN Sala s ON ps.id_sala = s.id_sala
    WHERE CONCAT(ps.fecha_prestamo, ' ', ps.hora_fin) < NOW()
    ORDER BY ps.fecha_prestamo DESC, ps.hora_fin DESC
    LIMIT 100
    """
    reservas = execute_query(query, fetch_all=True)
    if not reservas:
        return []

    processed_reservas = []
    for r in reservas:
        hora_fin_str = str(r.get('hora_fin')) if r.get('hora_fin') else 'N/A'
        processed_reservas.append({
            'NombreAlumnoCompleto': f"{r.get('NombreAlumno', '')} {r.get('ApellidoAlumno', '')}".strip(),
            'NumeroSala': r.get('NumeroSala', 'N/A'),
            'FechaPrestamo': r.get('fecha_prestamo').strftime('%d/%m/%Y') if r.get('fecha_prestamo') else 'N/A',
            'HoraFin': hora_fin_str
        })
    return processed_reservas