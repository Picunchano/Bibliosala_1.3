# --- Archivo Actualizado: ui_log_desocupacion.py ---
import customtkinter as ctk
from data_manager import cargar_reservas_finalizadas, play_sound_if_enabled
from config import ICON_PATH

class LogDesocupacionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.withdraw() # Ocultar

        self.iconbitmap(ICON_PATH)
        self.title("Registro de Desocupación de Salas")
        self.geometry("800x500")
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._crear_widgets()
        self._cargar_logs()

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
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)
        title_label = ctk.CTkLabel(main_frame, text="Salas Desocupadas Recientemente", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 10))
        self.log_textbox = ctk.CTkTextbox(main_frame, state="disabled", font=("Courier New", 12))
        self.log_textbox.pack(expand=True, fill='both')
        btn_actualizar = ctk.CTkButton(main_frame, text="Actualizar", command=self._cargar_logs)
        btn_actualizar.pack(pady=10)

    def _cargar_logs(self):
        play_sound_if_enabled()
        logs = cargar_reservas_finalizadas()
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        if not logs:
            self.log_textbox.insert("end", "No hay registros de desocupación recientes.")
        else:
            header = f"{'Fecha Fin':<12}{'Hora Fin':<12}{'Sala':<10}{'Alumno'}\n"
            separator = "-" * 60 + "\n"
            self.log_textbox.insert("end", header)
            self.log_textbox.insert("end", separator)
            for log in logs:
                linea = (f"{log['FechaPrestamo']:<12}"
                         f"{log['HoraFin']:<12}"
                         f"{log['NumeroSala']:<10}"
                         f"{log['NombreAlumnoCompleto']}\n")
                self.log_textbox.insert("end", linea)
        self.log_textbox.configure(state="disabled")

    def _on_close(self):
        play_sound_if_enabled()
        self.destroy()