# --- analysis.py ---
import collections
from datetime import datetime

def _filtrar_reservas_por_fecha(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    if anio is None and mes is None and dia is None:
        return list(reservas)
    reservas_filtradas = []
    for reserva in reservas:
        try:
            fecha_obj = datetime.strptime(reserva.get('FechaSolicitud'), "%d/%m/%Y")
            match = True
            if anio is not None and fecha_obj.year != anio: match = False
            if mes is not None and fecha_obj.month != mes: match = False
            if dia is not None and fecha_obj.day != dia: match = False
            if match: reservas_filtradas.append(reserva)
        except (ValueError, TypeError):
            continue
    return reservas_filtradas

def alumno_mas_solicitudes(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    reservas_a_procesar = _filtrar_reservas_por_fecha(reservas, anio, mes, dia)
    if not reservas_a_procesar: return []
    contador = collections.Counter(r.get('NombreAlumno') for r in reservas_a_procesar if r.get('NombreAlumno'))
    return contador.most_common()

def sala_mas_ocupada(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    reservas_a_procesar = _filtrar_reservas_por_fecha(reservas, anio, mes, dia)
    if not reservas_a_procesar: return []
    contador = collections.Counter(r.get('IDSala') for r in reservas_a_procesar if r.get('IDSala'))
    return contador.most_common()

def conteo_reservas_filtradas(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> int:
    return len(_filtrar_reservas_por_fecha(reservas, anio, mes, dia))

def horarios_mas_activos(reservas: list, anio: int = None, mes: int = None, dia: int = None) -> list:
    reservas_a_procesar = _filtrar_reservas_por_fecha(reservas, anio, mes, dia)
    if not reservas_a_procesar: return []
    actividad_por_hora = collections.defaultdict(int)
    for reserva in reservas_a_procesar:
        try:
            h_inicio = int(reserva.get('HoraInicio').split(':')[0])
            h_fin = int(reserva.get('HoraFin').split(':')[0])
            m_fin = int(reserva.get('HoraFin').split(':')[1])
            current_h = h_inicio
            while current_h < h_fin or (current_h == h_fin and m_fin > 0):
                if current_h > 23: break
                actividad_por_hora[current_h] += 1
                current_h += 1
        except (ValueError, IndexError, AttributeError):
            continue
    
    resultado = [(f"{h:02d}:00 - {h+1:02d}:00", count) for h, count in actividad_por_hora.items()]
    resultado.sort(key=lambda x: (-x[1], x[0]))
    return resultado