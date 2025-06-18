# ui_nueva_reserva.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from data_manager import guardar_reserva, cargar_salas_disponibles, play_sound

class NuevaReservaWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Nueva Reserva")
        self.geometry("500x580") # Ajustado para nuevos campos
        self.resizable(False, False)
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.salas_disponibles = cargar_salas_disponibles()
        self._crear_widgets()
        self._establecer_fecha_hora_actual()

    def _crear_widgets(self):
        form_frame = ttk.Frame(self, padding="15")
        form_frame.pack(expand=True, fill=tk.BOTH)

        self.entries = {}

        # Campos de Alumno
        ttk.Label(form_frame, text="RUT Alumno:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entries['RUTAlumno'] = ttk.Entry(form_frame, width=35)
        self.entries['RUTAlumno'].grid(row=0, column=1, padx=5, pady=5)

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

        # Campos de Sala
        ttk.Label(form_frame, text="Número Sala:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entries['NumeroSala'] = tk.StringVar(form_frame)
        if self.salas_disponibles:
            self.entries['NumeroSala'].set(self.salas_disponibles[0])
            sala_option_menu = ttk.OptionMenu(form_frame, self.entries['NumeroSala'], self.salas_disponibles[0], *self.salas_disponibles)
            sala_option_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        else:
            ttk.Label(form_frame, text="No hay salas disponibles.").grid(row=5, column=1, padx=5, pady=5, sticky="w")
            self.entries['NumeroSala'].set("N/A")

        # Campos de Préstamo
        ttk.Label(form_frame, text="Fecha Préstamo (DD/MM/YYYY):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entries['FechaPrestamo'] = ttk.Entry(form_frame, width=35)
        self.entries['FechaPrestamo'].grid(row=6, column=1, padx=5, pady=5)

        # Etiqueta de Hora Inicio
        ttk.Label(form_frame, text="Hora Inicio (HH:MM:SS):").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entries['HoraInicio'] = ttk.Entry(form_frame, width=35)
        self.entries['HoraInicio'].grid(row=7, column=1, padx=5, pady=5)

        # Etiqueta de Hora Fin
        ttk.Label(form_frame, text="Hora Fin (HH:MM:SS):").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entries['HoraFin'] = ttk.Entry(form_frame, width=35)
        self.entries['HoraFin'].grid(row=8, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Tipo de Préstamo:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.entries['IndividualOGrupal'] = tk.StringVar(form_frame)
        self.entries['IndividualOGrupal'].set("Individual")
        tipo_prestamo_options = ["Individual", "Grupal"]
        tipo_prestamo_menu = ttk.OptionMenu(form_frame, self.entries['IndividualOGrupal'], "Individual", *tipo_prestamo_options)
        tipo_prestamo_menu.grid(row=9, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        confirmar_button = ttk.Button(button_frame, text="Confirmar Reserva", command=self._confirmar_reserva_action)
        confirmar_button.pack(side=tk.LEFT, padx=5)

        cancelar_button = ttk.Button(button_frame, text="Cancelar", command=self._on_close)
        cancelar_button.pack(side=tk.RIGHT, padx=5)

    def _establecer_fecha_hora_actual(self):
        now = datetime.datetime.now()
        fecha_str = now.strftime("%d/%m/%Y")
        hora_inicio_str = now.strftime("%H:%M:%S")

        # --- CAMBIO CLAVE AQUÍ: Duración de 10 segundos ---
        hora_fin_obj = now + datetime.timedelta(seconds=10) # <-- ¡Aquí está el cambio!
        # --- FIN DEL CAMBIO ---

        hora_fin_str = hora_fin_obj.strftime("%H:%M:%S")

        self.entries['FechaPrestamo'].delete(0, tk.END)
        self.entries['FechaPrestamo'].insert(0, fecha_str)
        self.entries['HoraInicio'].delete(0, tk.END)
        self.entries['HoraInicio'].insert(0, hora_inicio_str)
        self.entries['HoraFin'].delete(0, tk.END)
        self.entries['HoraFin'].insert(0, hora_fin_str)

    def _confirmar_reserva_action(self):
        play_sound()
        reserva_data = {
            'RUTAlumno': self.entries['RUTAlumno'].get(),
            'Nombre': self.entries['Nombre'].get(),
            'Apellido': self.entries['Apellido'].get(),
            'Carrera': self.entries['Carrera'].get(),
            'Email': self.entries['Email'].get(),
            'NumeroSala': self.entries['NumeroSala'].get(),
            'FechaPrestamo': self.entries['FechaPrestamo'].get(),
            'HoraInicio': self.entries['HoraInicio'].get(),
            'HoraFin': self.entries['HoraFin'].get(),
            'IndividualOGrupal': self.entries['IndividualOGrupal'].get()
        }

        # Validaciones de campos obligatorios
        required_fields = ['RUTAlumno', 'Nombre', 'Apellido', 'NumeroSala', 'FechaPrestamo', 'HoraInicio', 'HoraFin']
        if not all(reserva_data[field] for field in required_fields):
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos obligatorios.", parent=self)
            return

        rut = reserva_data['RUTAlumno']
        # Validacion RUT: 8 a 12 caracteres, solo dígitos, puntos, guiones y 'k'/'K'
        if not all(c.isdigit() or c in '.-kK' for c in rut) or not (8 <= len(rut) <= 12):
            messagebox.showwarning("Formato Inválido", "El RUT no tiene un formato válido (ej. 12.345.678-9).", parent=self)
            return

        email = reserva_data['Email']
        if email and ('@' not in email or '.' not in email.split('@')[-1]):
            messagebox.showwarning("Formato Inválido", "El correo electrónico no tiene un formato válido.", parent=self)
            return

        if guardar_reserva(reserva_data):
            messagebox.showinfo("Éxito", "Reserva guardada correctamente.", parent=self)
            self._limpiar_campos()
            self._establecer_fecha_hora_actual()
        else:
            messagebox.showerror("Error", "No se pudo guardar la reserva. Posiblemente la sala ya está ocupada o hubo un error.", parent=self)

    def _limpiar_campos(self):
        # Limpia los campos de entrada
        self.entries['RUTAlumno'].delete(0, tk.END)
        self.entries['Nombre'].delete(0, tk.END)
        self.entries['Apellido'].delete(0, tk.END)
        self.entries['Carrera'].delete(0, tk.END)
        self.entries['Email'].delete(0, tk.END)

        # Restablece los valores predeterminados para OptionMenu
        if self.salas_disponibles:
            self.entries['NumeroSala'].set(self.salas_disponibles[0])
        else:
            self.entries['NumeroSala'].set("N/A") # O algún valor predeterminado si no hay salas

        self.entries['IndividualOGrupal'].set("Individual")

        # Limpia los campos de fecha y hora, que se restablecerán a la hora actual
        self.entries['FechaPrestamo'].delete(0, tk.END)
        self.entries['HoraInicio'].delete(0, tk.END)
        self.entries['HoraFin'].delete(0, tk.END)


    def _on_close(self):
        play_sound()
        self.destroy()