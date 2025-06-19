# --- Archivo Modificado: ui_main_menu.py ---
import customtkinter as ctk
from ui_nueva_reserva import NuevaReservaWindow
from ui_ver_reservas import VerReservasWindow
from ui_analisis_datos import AnalisisWindow
from ui_log_desocupacion import LogDesocupacionWindow
from ui_settings import SettingsWindow
from ui_tutorial import TutorialWindow  # <-- 1. IMPORTAR la nueva ventana de tutorial
from data_manager import play_sound_if_enabled

class MainMenuWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self._create_widgets()

    def _create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Gestión de Salas - Menú Principal", font=ctk.CTkFont(size=24, weight="bold")) #
        title_label.pack(pady=40) #

        button_frame = ctk.CTkFrame(self, fg_color="transparent") #
        button_frame.pack(expand=True) #

        button_font = ctk.CTkFont(size=14)
        button_width = 250 #
        button_height = 50 #

        btn_nueva_reserva = ctk.CTkButton(button_frame, text="Nueva Reserva", command=self._open_nueva_reserva, font=button_font, width=button_width, height=button_height) #
        btn_nueva_reserva.pack(pady=10) #

        btn_ver_reservas = ctk.CTkButton(button_frame, text="Ver Reservas", command=self._open_ver_reservas, font=button_font, width=button_width, height=button_height) #
        btn_ver_reservas.pack(pady=10) #

        btn_log_desocupacion = ctk.CTkButton(button_frame, text="Registro de Desocupación", command=self._open_log_desocupacion, font=button_font, width=button_width, height=button_height) #
        btn_log_desocupacion.pack(pady=10) #

        btn_analisis = ctk.CTkButton(button_frame, text="Análisis de Datos", command=self._open_analisis_datos, font=button_font, width=button_width, height=button_height) #
        btn_analisis.pack(pady=10) #

        btn_settings = ctk.CTkButton(button_frame, text="Configuración", command=self._open_settings, font=button_font, width=button_width, height=button_height) #
        btn_settings.pack(pady=10) #

        # --- 2. AÑADIR EL NUEVO BOTÓN DE TUTORIAL ---
        btn_tutorial = ctk.CTkButton(button_frame, text="Tutorial", command=self._open_tutorial, font=button_font, width=button_width, height=button_height)
        btn_tutorial.pack(pady=10)

    def _open_nueva_reserva(self):
        play_sound_if_enabled()
        NuevaReservaWindow(self.parent)

    def _open_ver_reservas(self):
        play_sound_if_enabled()
        VerReservasWindow(self.parent)

    def _open_log_desocupacion(self):
        play_sound_if_enabled() #
        LogDesocupacionWindow(self.parent) #

    def _open_analisis_datos(self):
        play_sound_if_enabled()
        AnalisisWindow(self.parent)

    def _open_settings(self):
        play_sound_if_enabled()
        SettingsWindow(self.parent)
        
    # --- 3. AÑADIR EL NUEVO MÉTODO PARA ABRIR EL TUTORIAL ---
    def _open_tutorial(self):
        """Abre la ventana del tutorial."""
        play_sound_if_enabled()
        TutorialWindow(self.parent)