# data_manager.py
import datetime
import sys
from mysql.connector import Error
from db_connection import execute_query, get_db_connection, close_db_connection
from config import SALAS_DISPONIBLES_DEFAULT
from user import Usuario # Necesario para get_user_by_username

# Lógica para winsound multiplataforma
if sys.platform == "win32":
    import winsound
else:
    # Si no es Windows, define una función simulada para winsound.Beep
    def winsound_Beep(frequency, duration):
        pass
    # Crea un objeto mock para winsound que tenga el método Beep
    winsound = type('winsound', (), {'Beep': winsound_Beep})

def play_sound():
    """Reproduce un sonido de sistema."""
    try:
        if sys.platform == "win32":
            winsound.Beep(440, 150) # Frecuencia 440 Hz, duración 150 ms
    except Exception as e:
        print(f"No se pudo reproducir el sonido: {e}")

def get_user_by_username(username: str):
    """Obtiene un objeto Usuario de la base de datos por su nombre de usuario."""
    query = "SELECT id_usuario, username, password_hash FROM Usuario WHERE username = %s"
    user_data = execute_query(query, (username,), fetch_one=True)
    if user_data:
        return Usuario(user_data['id_usuario'], user_data['username'], user_data['password_hash'])
    return None

def cargar_reservas():
    """
    Carga todas las reservas desde la base de datos, uniendo información
    de Alumno y Sala, y las formatea para su visualización.
    """
    query = """
    SELECT
        ps.idPrestamo,
        ps.timestamp_creacion, -- Asegúrate de que esta columna exista en tu tabla Prestamo_Sala
        a.rut_alumno AS RUTAlumno,
        a.nombre AS NombreAlumno,
        a.apellido AS ApellidoAlumno,
        a.carrera AS CarreraAlumno,
        a.email AS EmailAlumno,
        s.numero_sala AS NumeroSala,
        s.capacidad AS CapacidadSala,
        s.tipo_sala AS TipoSala,
        ps.fecha_prestamo,
        ps.hora_inicio,
        ps.hora_fin,
        ps.individual_o_grupal
    FROM Prestamo_Sala ps
    JOIN Alumno a ON ps.rut_alumno = a.rut_alumno
    JOIN Sala s ON ps.id_sala = s.id_sala
    ORDER BY ps.fecha_prestamo DESC, ps.hora_inicio DESC
    """
    reservas = execute_query(query, fetch_all=True)
    if reservas is False:
        print("Error al cargar las reservas de la base de datos.")
        return []

    processed_reservas = []
    for r in reservas:
        try:
            nombre_completo_alumno = f"{r.get('NombreAlumno', '')} {r.get('ApellidoAlumno', '')}".strip()

            processed_reservas.append({
                'id_prestamo': r.get('idPrestamo'),
                # Convertir a timestamp de UNIX si timestamp_creacion existe y es de tipo datetime
                'TimestampReserva': r.get('timestamp_creacion').timestamp() if isinstance(r.get('timestamp_creacion'), datetime.datetime) else None,
                'RUTAlumno': r.get('RUTAlumno', 'N/A'),
                'NombreAlumnoCompleto': nombre_completo_alumno,
                'NombreAlumno': r.get('NombreAlumno', 'N/A'),
                'ApellidoAlumno': r.get('ApellidoAlumno', 'N/A'),
                'CarreraAlumno': r.get('CarreraAlumno', 'N/A'),
                'EmailAlumno': r.get('EmailAlumno', 'N/A'),
                'NumeroSala': r.get('NumeroSala', 'N/A'),
                'CapacidadSala': r.get('CapacidadSala', 0),
                'TipoSala': r.get('TipoSala', 'N/A'),
                # Formatear fechas y horas a cadenas específicas para la UI
                'FechaPrestamo': r.get('fecha_prestamo').strftime('%d/%m/%Y') if isinstance(r.get('fecha_prestamo'), datetime.date) else str(r.get('fecha_prestamo')),
                'HoraInicio': r.get('hora_inicio').strftime('%H:%M:%S') if isinstance(r.get('hora_inicio'), datetime.time) else str(r.get('hora_inicio')),
                'HoraFin': r.get('hora_fin').strftime('%H:%M:%S') if isinstance(r.get('hora_fin'), datetime.time) else str(r.get('hora_fin')),
                'IndividualOGrupal': r.get('individual_o_grupal', 'N/A')
            })
        except KeyError as ke:
            print(f"Error en cargar_reservas: Clave faltante en el resultado de la DB: {ke} en registro: {r}")
            continue
        except Exception as ex:
            print(f"Error procesando reserva cargada: {ex} en registro: {r}")
            continue
    return processed_reservas


def guardar_reserva(datos_reserva: dict):
    """
    Guarda una nueva reserva en la base de datos, o actualiza un alumno existente.
    Realiza validaciones y verifica solapamiento de reservas.
    """
    rut_alumno = datos_reserva.get('RUTAlumno')
    nombre_alumno = datos_reserva.get('Nombre')
    apellido_alumno = datos_reserva.get('Apellido')
    carrera_alumno = datos_reserva.get('Carrera', '')
    email_alumno = datos_reserva.get('Email', '')
    numero_sala = datos_reserva.get('NumeroSala')
    fecha_prestamo_str = datos_reserva.get('FechaPrestamo')
    hora_inicio_str = datos_reserva.get('HoraInicio')
    hora_fin_str = datos_reserva.get('HoraFin')
    individual_o_grupal = datos_reserva.get('IndividualOGrupal', 'Individual')

    # Validación básica de datos
    if not all([rut_alumno, nombre_alumno, apellido_alumno, numero_sala, fecha_prestamo_str, hora_inicio_str, hora_fin_str]):
        print("Error (data_manager): Datos de reserva incompletos.")
        return False

    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor(dictionary=True)
        conn.start_transaction() # Inicia una transacción para asegurar la atomicidad

        # 1. Gestionar Alumno (usando rut_alumno como PK)
        cursor.execute("SELECT rut_alumno FROM Alumno WHERE rut_alumno = %s", (rut_alumno,))
        existing_alumno = cursor.fetchone()

        if existing_alumno:
            # Actualizar datos del alumno si ya existe
            cursor.execute("UPDATE Alumno SET nombre = %s, apellido = %s, carrera = %s, email = %s WHERE rut_alumno = %s",
                           (nombre_alumno, apellido_alumno, carrera_alumno, email_alumno, rut_alumno))
        else:
            # Insertar nuevo alumno
            cursor.execute("INSERT INTO Alumno (rut_alumno, nombre, apellido, carrera, email) VALUES (%s, %s, %s, %s, %s)",
                           (rut_alumno, nombre_alumno, apellido_alumno, carrera_alumno, email_alumno))

        # 2. Obtener ID de Sala (usando numero_sala)
        sala_id = None
        cursor.execute("SELECT id_sala FROM Sala WHERE numero_sala = %s", (numero_sala,))
        existing_sala = cursor.fetchone()
        if existing_sala:
            sala_id = existing_sala['id_sala']
        else:
            # Si la sala no existe, no se puede reservar
            raise ValueError(f"La sala '{numero_sala}' no existe en la base de datos.")

        # 3. Validar y parsear Fechas/Horas
        try:
            fecha_obj = datetime.datetime.strptime(fecha_prestamo_str, "%d/%m/%Y").date()

            # --- ¡DEBUG PRINTS CLAVE AQUÍ! ---
            print(f"DEBUG: Parsing HoraInicio string: '{hora_inicio_str}'")
            print(f"DEBUG: Parsing HoraFin string: '{hora_fin_str}'")
            # --- FIN DEBUG PRINTS ---

            # Parsear horas, esperando formato HH:MM:SS
            hora_inicio_obj = datetime.datetime.strptime(hora_inicio_str, "%H:%M:%S").time()
            hora_fin_obj = datetime.datetime.strptime(hora_fin_str, "%H:%M:%S").time()
        except ValueError as e:
            # Captura errores de formato de fecha/hora y lanza una excepción más descriptiva
            raise ValueError(f"Formato de fecha/hora inválido: {e}. Asegúrate de usar DD/MM/YYYY para la fecha y HH:MM:SS para la hora.")

        # Validación lógica de horas
        if hora_inicio_obj >= hora_fin_obj:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin.")

        # 4. Verificar Solapamiento de Reserva (Importante para evitar dobles reservas)
        overlap_query = """
        SELECT COUNT(*)
        FROM Prestamo_Sala
        WHERE id_sala = %s
          AND fecha_prestamo = %s
          AND (
                (hora_inicio < %s AND hora_fin > %s) OR -- La nueva reserva empieza antes y termina después de una existente
                (%s < hora_fin AND %s > hora_inicio)    -- La nueva reserva empieza durante una existente
              )
        """
        overlap_params = (
            sala_id, fecha_obj,
            hora_fin_obj, hora_inicio_obj, # Para el primer OR
            hora_inicio_obj, hora_fin_obj  # Para el segundo OR
        )

        cursor.execute(overlap_query, overlap_params)
        overlap_count = cursor.fetchone()['COUNT(*)']

        if overlap_count > 0:
            raise ValueError(f"La sala '{numero_sala}' ya está reservada en el horario {hora_inicio_str}-{hora_fin_str} para la fecha {fecha_prestamo_str}.")

        # 5. Insertar la Reserva
        insert_prestamo_query = """
        INSERT INTO Prestamo_Sala (rut_alumno, id_sala, fecha_prestamo, hora_inicio, hora_fin, individual_o_grupal)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (rut_alumno, sala_id, fecha_obj, hora_inicio_obj, hora_fin_obj, individual_o_grupal)
        cursor.execute(insert_prestamo_query, params)

        conn.commit() # Confirma todos los cambios en la transacción
        play_sound() # Reproduce sonido de éxito
        return True

    except Error as e:
        print(f"Error de base de datos al guardar la reserva: {e}")
        conn.rollback() # Deshace todos los cambios de la transacción
        return False
    except ValueError as e:
        print(f"Error de validación al guardar la reserva: {e}")
        conn.rollback() # Deshace todos los cambios de la transacción
        return False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_db_connection(conn)


def eliminar_reservas_por_timestamps(ids_prestamo: list):
    """Elimina reservas de la base de datos por sus IDs de préstamo."""
    if not ids_prestamo:
        return True

    try:
        # Asegúrate de que los IDs sean enteros válidos
        ids_to_delete = [int(id_val) for id_val in ids_prestamo]
    except ValueError:
        print("Error (data_manager): IDs de reserva inválidos para eliminar.")
        return False

    # Crea una cadena de marcadores de posición para la cláusula IN
    placeholders = ', '.join(['%s'] * len(ids_to_delete))
    query = f"DELETE FROM Prestamo_Sala WHERE idPrestamo IN ({placeholders})"

    result = execute_query(query, tuple(ids_to_delete), commit=True)
    if result:
        play_sound() # Reproduce sonido de éxito
    return result

def cargar_salas_disponibles():
    """Carga los números de sala disponibles desde la base de datos."""
    query = "SELECT numero_sala FROM Sala ORDER BY numero_sala"
    salas = execute_query(query, fetch_all=True)
    if salas is False:
        print("Error al cargar salas disponibles. Usando lista por defecto.")
        return SALAS_DISPONIBLES_DEFAULT

    if salas:
        return [s['numero_sala'] for s in salas]
    else:
        # Si no hay salas en la DB, devuelve las por defecto
        return SALAS_DISPONIBLES_DEFAULT