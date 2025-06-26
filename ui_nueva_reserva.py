# --- Archivo Actualizado: ui_nueva_reserva.py ---
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from data_manager import guardar_reserva, cargar_salas_disponibles, play_sound_if_enabled
from db_connection import execute_query
from config import ICON_PATH

class NuevaReservaWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.withdraw() # 1. Ocultar la ventana al nacer

        self.iconbitmap(ICON_PATH)
        self.title("Nueva Reserva")
        self.geometry("500x650") #
        self.resizable(False, False)
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.salas_disponibles = cargar_salas_disponibles()
        self._crear_widgets()
        self._establecer_fecha_hora_actual()
        
        self.after(10, self._center_and_show) # 2. Llamar a la función para centrar y mostrar

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
            self.deiconify() # 3. Mostrar la ventana ya centrada

    # ... (el resto del archivo no cambia)
    def _crear_widgets(self):
        form_frame = ttk.Frame(self, padding="15")
        form_frame.pack(expand=True, fill=tk.BOTH)
        self.entries = {}
        ttk.Label(form_frame, text="RUT Alumno:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entries['RUTAlumno'] = ttk.Entry(form_frame, width=35)
        self.entries['RUTAlumno'].grid(row=0, column=1, padx=5, pady=5)
        self.entries['RUTAlumno'].bind("<FocusOut>", self._verificar_alumno)
        self.entries['RUTAlumno'].bind("<Return>", self._verificar_alumno)
        ttk.Label(form_frame, text="Nombre Alumno:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entries['Nombre'] = ttk.Entry(form_frame, width=35)
        self.entries['Nombre'].grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Apellido Alumno:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entries['Apellido'] = ttk.Entry(form_frame, width=35)
        self.entries['Apellido'].grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Carrera Alumno:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entries['Carrera'] = ttk.Entry(form_frame, width=35)
        self.entries['Carrera'].grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Email Alumno:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entries['Email'] = ttk.Entry(form_frame, width=35)
        self.entries['Email'].grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Número Sala:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entries['NumeroSala'] = tk.StringVar(form_frame)
        if self.salas_disponibles:
            self.entries['NumeroSala'].set(self.salas_disponibles[0])
            sala_option_menu = ttk.OptionMenu(form_frame, self.entries['NumeroSala'], self.salas_disponibles[0], *self.salas_disponibles)
            sala_option_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        else:
            ttk.Label(form_frame, text="No hay salas disponibles.").grid(row=5, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(form_frame, text="Fecha Préstamo (DD/MM/YYYY):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entries['FechaPrestamo'] = ttk.Entry(form_frame, width=35)
        self.entries['FechaPrestamo'].grid(row=6, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Hora Inicio (HH:MM:SS):").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entries['HoraInicio'] = ttk.Entry(form_frame, width=35)
        self.entries['HoraInicio'].grid(row=7, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Hora Fin (HH:MM:SS):").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entries['HoraFin'] = ttk.Entry(form_frame, width=35)
        self.entries['HoraFin'].grid(row=8, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Tipo de Préstamo:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.entries['IndividualOGrupal'] = tk.StringVar(form_frame)
        self.entries['IndividualOGrupal'].set("Individual")
        tipo_prestamo_option_menu = ttk.OptionMenu(form_frame, self.entries['IndividualOGrupal'], "Individual", "Individual", "Grupal")
        tipo_prestamo_option_menu.grid(row=9, column=1, padx=5, pady=5, sticky="ew")
        btn_guardar = ttk.Button(form_frame, text="Guardar Reserva", command=self._guardar_reserva)
        btn_guardar.grid(row=10, column=0, columnspan=2, pady=20, sticky="ew")

    def _establecer_fecha_hora_actual(self):
        now = datetime.datetime.now()
        self.entries['FechaPrestamo'].delete(0, tk.END)
        self.entries['FechaPrestamo'].insert(0, now.strftime("%d/%m/%Y"))
        self.entries['HoraInicio'].delete(0, tk.END)
        self.entries['HoraInicio'].insert(0, now.strftime("%H:%M:%S"))
        self.entries['HoraFin'].delete(0, tk.END)
        hora_fin_demo = now + datetime.timedelta(seconds=10)
        self.entries['HoraFin'].insert(0, hora_fin_demo.strftime("%H:%M:%S"))

    def _verificar_alumno(self, event=None):
        rut = self.entries['RUTAlumno'].get().strip()
        if not rut:
            return
        query = "SELECT nombre, apellido, carrera, email FROM Alumno WHERE rut_alumno = %s"
        alumno_data = execute_query(query, (rut,), fetch_one=True)
        if alumno_data:
            self.entries['Nombre'].delete(0, tk.END)
            self.entries['Nombre'].insert(0, alumno_data['nombre'])
            self.entries['Apellido'].delete(0, tk.END)
            self.entries['Apellido'].insert(0, alumno_data['apellido'])
            self.entries['Carrera'].delete(0, tk.END)
            self.entries['Carrera'].insert(0, alumno_data['carrera'])
            self.entries['Email'].delete(0, tk.END)
            self.entries['Email'].insert(0, alumno_data['email'])
        else:
            self.entries['Nombre'].delete(0, tk.END)
            self.entries['Apellido'].delete(0, tk.END)
            self.entries['Carrera'].delete(0, tk.END)
            self.entries['Email'].delete(0, tk.END)

    def _guardar_reserva(self):
        play_sound_if_enabled()
        datos = {key: entry.get() if not isinstance(entry, tk.StringVar) else entry.get()
                 for key, entry in self.entries.items()}
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=self)
            return
        try:
            datetime.datetime.strptime(datos['FechaPrestamo'], "%d/%m/%Y")
            hora_inicio_dt = datetime.datetime.strptime(datos['HoraInicio'], "%H:%M:%S").time()
            hora_fin_dt = datetime.datetime.strptime(datos['HoraFin'], "%H:%M:%S").time()
            if hora_inicio_dt >= hora_fin_dt:
                 messagebox.showerror("Error de Horario", "La hora de fin debe ser posterior a la hora de inicio.", parent=self)
                 return
        except ValueError:
            messagebox.showerror("Error de Formato", "Asegúrese de que la fecha sea DD/MM/YYYY y las horas HH:MM:SS.", parent=self)
            return
        if guardar_reserva(datos):
            messagebox.showinfo("Éxito", "Reserva guardada correctamente.", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la reserva.", parent=self)

    def _on_close(self):
        play_sound_if_enabled()
        self.destroy()