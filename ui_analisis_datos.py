# --- Archivo Actualizado: ui_analisis_datos.py ---
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
from collections import Counter
from data_manager import get_all_reservations, play_sound_if_enabled
from config import ICON_PATH

class AnalisisWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.withdraw() # Ocultar

        self.iconbitmap(ICON_PATH)
        self.title("Análisis de Datos de Reservas")
        self.geometry("700x600")
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.reservas = []
        self._crear_widgets()
        
        self.after(10, self._center_and_show) # Centrar y mostrar

    def _center_and_show(self):
        """Centra la ventana en la pantalla y la hace visible."""
        try:
            self.update_idletasks()
            width = self.winfo_width()
            height = self.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
            self.geometry(f'{width}x{height}+{x}+{y}')
        finally:
            self.deiconify()

    # ... (el resto del archivo no cambia) ...
    def _crear_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(expand=True, fill=tk.BOTH)
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros por Fecha", padding="10")
        filter_frame.pack(fill=tk.X, pady=10)
        ttk.Label(filter_frame, text="Año (YYYY):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.year_entry = ttk.Entry(filter_frame, width=10)
        self.year_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(filter_frame, text="Mes (MM):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.month_entry = ttk.Entry(filter_frame, width=10)
        self.month_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        ttk.Label(filter_frame, text="Día (DD):").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.day_entry = ttk.Entry(filter_frame, width=10)
        self.day_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        btn_apply_filter = ttk.Button(filter_frame, text="Aplicar Filtro", command=self._aplicar_filtro)
        btn_apply_filter.grid(row=0, column=6, padx=10, pady=5)
        btn_clear_filter = ttk.Button(filter_frame, text="Limpiar Filtro", command=self._limpiar_filtro)
        btn_clear_filter.grid(row=0, column=7, padx=5, pady=5)
        analysis_frame = ttk.LabelFrame(main_frame, text="Resultados del Análisis", padding="10")
        analysis_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, wrap=tk.WORD, state='disabled', font=("Courier New", 10))
        self.analysis_text.pack(expand=True, fill=tk.BOTH)
        self._realizar_analisis()

    def _aplicar_filtro(self):
        play_sound_if_enabled()
        self._realizar_analisis()

    def _limpiar_filtro(self):
        play_sound_if_enabled()
        self.year_entry.delete(0, tk.END)
        self.month_entry.delete(0, tk.END)
        self.day_entry.delete(0, tk.END)
        self._realizar_analisis()

    def _realizar_analisis(self):
        self.reservas = get_all_reservations()
        filtered_reservas = self._filtrar_reservas()
        self.analysis_text.config(state='normal')
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "--- Resumen General ---\n")
        self.analysis_text.insert(tk.END, f"Total de Reservas Cargadas: {len(self.reservas)}\n")
        self.analysis_text.insert(tk.END, f"Total de Reservas Filtradas: {len(filtered_reservas)}\n\n")
        self._analizar_alumnos_activos(filtered_reservas)
        self._analizar_salas_ocupadas(filtered_reservas)
        self._analizar_horarios_actividad(filtered_reservas)
        self._analizar_tipo_prestamo(filtered_reservas)
        self.analysis_text.config(state='disabled')

    def _filtrar_reservas(self):
        year_str = self.year_entry.get().strip()
        month_str = self.month_entry.get().strip()
        day_str = self.day_entry.get().strip()
        filtered = []
        for reserva in self.reservas:
            try:
                fecha_reserva = datetime.datetime.strptime(reserva['FechaPrestamo'], "%d/%m/%Y").date()
                match = True
                if year_str and str(fecha_reserva.year) != year_str:
                    match = False
                if month_str and str(fecha_reserva.month).zfill(2) != month_str.zfill(2):
                    match = False
                if day_str and str(fecha_reserva.day).zfill(2) != day_str.zfill(2):
                    match = False
                if match:
                    filtered.append(reserva)
            except (ValueError, KeyError) as e:
                print(f"Advertencia: No se pudo parsear la fecha de la reserva: {e}. Datos: {reserva}")
                continue
        return filtered

    def _analizar_alumnos_activos(self, filtered_reservas):
        alumnos = [reserva['NombreAlumnoCompleto'] for reserva in filtered_reservas if 'NombreAlumnoCompleto' in reserva]
        alumno_counts = Counter(alumnos)
        self.analysis_text.insert(tk.END, "--- Alumnos con Más Solicitudes ---\n")
        if alumno_counts:
            for alumno, count in alumno_counts.most_common(5):
                self.analysis_text.insert(tk.END, f"- {alumno}: {count} reservas\n")
        else:
            self.analysis_text.insert(tk.END, "No hay datos de alumnos para analizar.\n")
        self.analysis_text.insert(tk.END, "\n")

    def _analizar_salas_ocupadas(self, filtered_reservas):
        salas = [reserva['NumeroSala'] for reserva in filtered_reservas if 'NumeroSala' in reserva]
        sala_counts = Counter(salas)
        self.analysis_text.insert(tk.END, "--- Salas Más Ocupadas ---\n")
        if sala_counts:
            for sala, count in sala_counts.most_common(5):
                self.analysis_text.insert(tk.END, f"- Sala {sala}: {count} reservas\n")
        else:
            self.analysis_text.insert(tk.END, "No hay datos de salas para analizar.\n")
        self.analysis_text.insert(tk.END, "\n")

    def _analizar_horarios_actividad(self, filtered_reservas):
        horas_actividad = Counter()
        for reserva in filtered_reservas:
            try:
                hora_inicio = datetime.datetime.strptime(reserva['HoraInicio'], "%H:%M:%S").time()
                hora_fin = datetime.datetime.strptime(reserva['HoraFin'], "%H:%M:%S").time()
                current_hour = hora_inicio.hour
                while current_hour < hora_fin.hour or (current_hour == hora_fin.hour and hora_fin.minute > 0):
                    horas_actividad[f"{current_hour:02d}:00"] += 1
                    current_hour += 1
                    if current_hour > 23: break
            except (ValueError, KeyError) as e:
                print(f"Advertencia: No se pudo parsear la hora: {e}. Datos: {reserva}")
                continue
        self.analysis_text.insert(tk.END, "--- Horarios de Mayor Actividad ---\n")
        if horas_actividad:
            sorted_horas = sorted(horas_actividad.items(), key=lambda item: (int(item[0].split(':')[0]), -item[1]))
            for hora, count in sorted_horas:
                self.analysis_text.insert(tk.END, f"- {hora}: {count} ocurrencias\n")
        else:
            self.analysis_text.insert(tk.END, "No hay datos de horarios para analizar.\n")
        self.analysis_text.insert(tk.END, "\n")

    def _analizar_tipo_prestamo(self, filtered_reservas):
        tipos_prestamo = [reserva['IndividualOGrupal'] for reserva in filtered_reservas if 'IndividualOGrupal' in reserva]
        tipo_counts = Counter(tipos_prestamo)
        self.analysis_text.insert(tk.END, "--- Tipos de Préstamo Más Comunes ---\n")
        if tipo_counts:
            for tipo, count in tipo_counts.most_common():
                self.analysis_text.insert(tk.END, f"- {tipo}: {count} reservas\n")
        else:
            self.analysis_text.insert(tk.END, "No hay datos de tipos de préstamo para analizar.\n")
        self.analysis_text.insert(tk.END, "\n")

    def _on_close(self):
        play_sound_if_enabled()
        self.destroy()