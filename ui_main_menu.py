# ui_main_menu.py
import tkinter as tk
from tkinter import ttk
from ui_nueva_reserva import NuevaReservaWindow # Importar
from ui_ver_reservas import VerReservasWindow   # Importar
from ui_analisis_datos import AnalisisWindow     # Importar
from data_manager import play_sound # Para el sonido

class MainMenuWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Menú Principal")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (self.winfo_width() / 2)
        y = (screen_height / 2) - (self.winfo_height() / 2)
        self.geometry(f"+{int(x)}+{int(y)}")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Gestión de Salas", font=("Helvetica", 18, "bold")).pack(pady=20)

        # Botones para diferentes funciones
        btn_nueva_reserva = ttk.Button(main_frame, text="Nueva Reserva", command=self._open_nueva_reserva)
        btn_nueva_reserva.pack(fill=tk.X, pady=10)

        btn_ver_reservas = ttk.Button(main_frame, text="Ver Reservas", command=self._open_ver_reservas)
        btn_ver_reservas.pack(fill=tk.X, pady=10)

        btn_analisis = ttk.Button(main_frame, text="Análisis de Datos", command=self._open_analisis_datos)
        btn_analisis.pack(fill=tk.X, pady=10)

    def _open_nueva_reserva(self):
        play_sound()
        NuevaReservaWindow(self)

    def _open_ver_reservas(self):
        play_sound()
        VerReservasWindow(self)

    def _open_analisis_datos(self):
        play_sound()
        AnalisisWindow(self)

    def _on_close(self):
        play_sound()
        self.parent.destroy() # Cierra la aplicación principal al cerrar el menú