# --- Versión Final y Corregida de: ui_tutorial.py ---

import customtkinter as ctk
from data_manager import play_sound_if_enabled
from config import ICON_PATH

class TutorialWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.iconbitmap(ICON_PATH)
        self.title("Tutorial del Sistema Bibliosala")
        self.geometry("800x600")
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._create_widgets()

    def _on_close(self):
        play_sound_if_enabled()
        self.destroy()

    def _insert_text(self, textbox, text, heading=False):
        font_size = 16 if heading else 14
        font = ctk.CTkFont(family="Arial", size=font_size, weight="bold" if heading else "normal")
        
        textbox.configure(state="normal")
        textbox.insert("end", text, font)
        textbox.configure(state="disabled")

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)

        title_label = ctk.CTkLabel(main_frame, text="¿Cómo Usar el Sistema?", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(0, 15))

        tab_view = ctk.CTkTabview(main_frame)
        tab_view.pack(expand=True, fill="both")

        tab_nueva_reserva = tab_view.add("1. Nueva Reserva")
        tab_ver_reservas = tab_view.add("2. Ver Reservas")
        tab_analisis = tab_view.add("3. Análisis y Registros")
        tab_settings = tab_view.add("4. Configuración")

        self._populate_nueva_reserva_tab(tab_nueva_reserva)
        self._populate_ver_reservas_tab(tab_ver_reservas)
        self._populate_analisis_tab(tab_analisis)
        self._populate_settings_tab(tab_settings)

    def _populate_nueva_reserva_tab(self, tab):
        textbox = ctk.CTkTextbox(tab, wrap="word", border_spacing=10, fg_color="transparent")
        textbox.pack(expand=True, fill="both", padx=5, pady=5)
        
        self._insert_text(textbox, "Crear una Nueva Reserva de Sala\n\n", heading=True)
        self._insert_text(textbox, "Sigue estos pasos para agendar el préstamo de una sala:\n\n")
        self._insert_text(textbox, "1.  Desde el Menú Principal, haz clic en 'Nueva Reserva'.\n\n")
        self._insert_text(textbox, "2.  Ingresa el RUT del alumno. Si ya está registrado, sus datos se cargarán. Si no, completa los campos.\n\n")
        self._insert_text(textbox, "3.  Selecciona la sala, la fecha y las horas de inicio y fin.\n\n\n")
        self._insert_text(textbox, "Nota para Demostración:\n", heading=True)
        self._insert_text(textbox, "Actualmente, la duración por defecto de la reserva está configurada en 10 segundos para facilitar las pruebas.")

    def _populate_ver_reservas_tab(self, tab):
        textbox = ctk.CTkTextbox(tab, wrap="word", border_spacing=10, fg_color="transparent")
        textbox.pack(expand=True, fill="both", padx=5, pady=5)
        
        self._insert_text(textbox, "Visualizar y Gestionar Reservas\n\n", heading=True)
        self._insert_text(textbox, "1.  Desde el Menú Principal, haz clic en 'Ver Reservas'.\n\n")
        self._insert_text(textbox, "2.  Para eliminar una o más reservas, haz clic en sus filas para seleccionarlas.\n\n")
        self._insert_text(textbox, "3.  Haz clic en 'Eliminar Seleccionadas' y confirma la acción.")

    def _populate_analisis_tab(self, tab):
        textbox = ctk.CTkTextbox(tab, wrap="word", border_spacing=10, fg_color="transparent")
        textbox.pack(expand=True, fill="both", padx=5, pady=5)

        self._insert_text(textbox, "Consultar Registros y Estadísticas\n\n", heading=True)
        self._insert_text(textbox, "El sistema ofrece varias herramientas para monitorizar la actividad:\n\n")
        self._insert_text(textbox, "Notificaciones en Tiempo Real:\n", heading=True)
        self._insert_text(textbox, "   • Cuando una reserva termina, aparecerá una ventana emergente para notificar que la sala ha quedado libre.\n\n")
        self._insert_text(textbox, "Análisis de Datos:\n", heading=True)
        self._insert_text(textbox, "   • Muestra estadísticas clave como los alumnos más activos y las salas más usadas.\n\n")
        self._insert_text(textbox, "Registro de Desocupación:\n", heading=True)
        self._insert_text(textbox, "   • Muestra un historial de las últimas reservas que ya han finalizado.")
        
    def _populate_settings_tab(self, tab):
        textbox = ctk.CTkTextbox(tab, wrap="word", border_spacing=10, fg_color="transparent")
        textbox.pack(expand=True, fill="both", padx=5, pady=5)

        self._insert_text(textbox, "Configurar la Aplicación\n\n", heading=True)
        self._insert_text(textbox, "La personalización se gestiona desde el archivo `config.py`.\n\n")
        self._insert_text(textbox, "Sonido de Notificación:\n", heading=True)
        self._insert_text(textbox, "   • La ruta al archivo de sonido .wav se define en la variable `SOUND_EFFECT_PATH`.\n\n")
        self._insert_text(textbox, "Tema de Color:\n", heading=True)
        self._insert_text(textbox, "   • El tema se puede cambiar en la ventana de Configuración y se guarda en `settings.json`.\n\n")
        self._insert_text(textbox, "Ícono y Logo:\n", heading=True)
        self._insert_text(textbox, "   • El ícono de la aplicación (.ico) se define en `ICON_PATH`.\n")
        self._insert_text(textbox, "   • La imagen de la pantalla de carga se define en `LOGO_PATH`.")