# --- analysis.py ---
import collections
from datetime import datetime

def _filtrar_reservas_por_fecha(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    """
    Filtra una lista de reservas por año, mes y/o día.
    Si no se proporcionan filtros de fecha, devuelve una copia de todas las reservas.
    """
    if anio is None and mes is None and dia is None:
        return list(reservas) # Retorna una copia para evitar modificar el original

    reservas_filtradas = []
    for reserva in reservas:
        try:
            # Asume que 'FechaSolicitud' está en formato "DD/MM/YYYY"
            # Si tu base de datos devuelve 'FechaPrestamo' como datetime.date,
            # asegúrate de que el formato coincida o ajústalo aquí.
            # Para el análisis, usaremos el formato de entrada esperado por datetime.strptime
            # que es el que se genera en data_manager para 'FechaPrestamo'.
            fecha_obj = datetime.strptime(reserva.get('FechaPrestamo'), "%d/%m/%Y") # Cambiado a FechaPrestamo

            match = True
            if anio is not None and fecha_obj.year != anio:
                match = False
            if mes is not None and fecha_obj.month != mes:
                match = False
            if dia is not None and fecha_obj.day != dia:
                match = False

            if match:
                reservas_filtradas.append(reserva)
        except (ValueError, TypeError):
            # Ignora reservas con formato de fecha inválido o si la clave no existe
            continue
    return reservas_filtradas

def alumno_mas_solicitudes(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    """
    Calcula los alumnos con más solicitudes de reserva, opcionalmente filtrado por fecha.
    Retorna una lista de tuplas (NombreAlumnoCompleto, conteo).
    """
    reservas_a_procesar = _filtrar_reservas_por_fecha(reservas, anio, mes, dia) #
    if not reservas_a_procesar:
        return []

    # Usa 'NombreAlumnoCompleto' del diccionario procesado en data_manager
    contador = collections.Counter(r.get('NombreAlumnoCompleto') for r in reservas_a_procesar if r.get('NombreAlumnoCompleto')) #
    return contador.most_common()

def sala_mas_ocupada(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    """
    Calcula las salas más ocupadas por número de reservas, opcionalmente filtrado por fecha.
    Retorna una lista de tuplas (NumeroSala, conteo).
    """
    reservas_a_procesar = _filtrar_reservas_por_fecha(reservas, anio, mes, dia) #
    if not reservas_a_procesar:
        return []

    # Usa 'NumeroSala' del diccionario procesado en data_manager
    contador = collections.Counter(r.get('NumeroSala') for r in reservas_a_procesar if r.get('NumeroSala')) #
    return contador.most_common()

def conteo_reservas_filtradas(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> int:
    """
    Retorna el número total de reservas después de aplicar los filtros de fecha.
    """
    return len(_filtrar_reservas_por_fecha(reservas, anio, mes, dia)) #

def horarios_mas_activos(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    """
    Identifica los rangos horarios con mayor actividad de reservas, opcionalmente filtrado por fecha.
    Retorna una lista de tuplas (rango_horario, conteo).
    """
    reservas_a_procesar = _filtrar_reservas_por_fecha(reservas, anio, mes, dia) #
    if not reservas_a_procesar:
        return []

    actividad_por_hora = collections.defaultdict(int)
    for reserva in reservas_a_procesar:
        try:
            # Asume 'HoraInicio' y 'HoraFin' están en formato "HH:MM:SS" (o "HH:MM")
            # Ajuste para usar strptime y luego acceder a .hour y .minute
            # Si el formato es "HH:MM", strptime('%H:%M') es suficiente.
            # Los datos de data_manager.py son "%H:%M:%S"
            hora_inicio_obj = datetime.strptime(reserva.get('HoraInicio'), "%H:%M:%S").time() #
            hora_fin_obj = datetime.strptime(reserva.get('HoraFin'), "%H:%M:%S").time() #

            current_h = hora_inicio_obj.hour
            # Considerar rangos de horas
            while current_h < hora_fin_obj.hour or (current_h == hora_fin_obj.hour and hora_fin_obj.minute > 0): #
                if current_h > 23: break # Evitar horas inválidas
                actividad_por_hora[current_h] += 1 #
                current_h += 1
        except (ValueError, IndexError, AttributeError, KeyError) as e: # Añadido KeyError
            print(f"Advertencia en horarios_mas_activos: No se pudo parsear la hora de la reserva o falta una clave: {e}. Datos: {reserva}") #
            continue
    
    # Formato de salida "HH:00 - HH+1:00" y ordenar
    resultado = [(f"{h:02d}:00 - {(h+1)%24:02d}:00", count) for h, count in actividad_por_hora.items()] # Ajustado para 24h
    resultado.sort(key=lambda x: (-x[1], x[0])) # Ordenar por conteo descendente, luego por hora ascendente
    return resultado