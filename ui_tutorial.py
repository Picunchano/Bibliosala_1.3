# --- Versión Anterior de: ui_tutorial.py ---

import customtkinter as ctk
from data_manager import play_sound_if_enabled
from config import ICON_PATH 

class TutorialWindow(ctk.CTkToplevel):
    """
    Una ventana que muestra un tutorial claro y preciso sobre cómo usar la aplicación,
    organizado en pestañas para cada funcionalidad principal.
    """
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
        """Maneja el cierre de la ventana con sonido."""
        play_sound_if_enabled()
        self.destroy()

    def _insert_text(self, textbox, text, heading=False):
        """
        Inserta texto en un CTkTextbox, opcionalmente con formato de encabezado.
        """
        font_size = 16 if heading else 14
        font = ctk.CTkFont(family="Arial", size=font_size, weight="bold" if heading else "normal")
        
        textbox.configure(state="normal")
        textbox.insert("end", text, font)
        textbox.configure(state="disabled")

    def _create_widgets(self):
        """Crea todos los widgets de la ventana del tutorial."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)

        title_label = ctk.CTkLabel(main_frame, text="¿Cómo Usar el Sistema?", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(0, 15))

        # Vista de Pestañas para organizar el contenido
        tab_view = ctk.CTkTabview(main_frame)
        tab_view.pack(expand=True, fill="both")

        # Se crean las pestañas
        tab_nueva_reserva = tab_view.add("1. Nueva Reserva")
        tab_ver_reservas = tab_view.add("2. Ver Reservas")
        tab_analisis = tab_view.add("3. Análisis y Registros")
        tab_settings = tab_view.add("4. Configuración")

        # Se añade el contenido a cada pestaña
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
        self._insert_text(textbox, "2.  Ingresa el RUT del alumno. Si el alumno ya está registrado en la base de datos, sus datos (nombre, apellido, etc.) se cargarán automáticamente. Si no, deberás completar los campos.\n\n")
        self._insert_text(textbox, "3.  Selecciona la sala deseada de la lista desplegable.\n\n")
        self._insert_text(textbox, "4.  Ajusta la fecha, hora de inicio y hora de fin de la reserva. Por defecto, se establece la fecha actual y un rango de una hora.\n\n")
        self._insert_text(textbox, "5.  Elige el tipo de préstamo: 'Individual' o 'Grupal'.\n\n")
        self._insert_text(textbox, "6.  Haz clic en 'Guardar Reserva' para confirmar. La reserva quedará registrada en el sistema.")

    def _populate_ver_reservas_tab(self, tab):
        textbox = ctk.CTkTextbox(tab, wrap="word", border_spacing=10, fg_color="transparent")
        textbox.pack(expand=True, fill="both", padx=5, pady=5)
        
        self._insert_text(textbox, "Visualizar y Gestionar Reservas\n\n", heading=True)
        self._insert_text(textbox, "Esta sección te permite ver todas las reservas activas y eliminarlas si es necesario.\n\n")
        self._insert_text(textbox, "1.  Desde el Menú Principal, haz clic en 'Ver Reservas'.\n\n")
        self._insert_text(textbox, "2.  En la tabla verás todas las reservas ordenadas por fecha y hora.\n\n")
        self._insert_text(textbox, "3.  Para eliminar una o más reservas, haz clic sobre sus filas en la tabla para seleccionarlas. Puedes seleccionar varias manteniendo la tecla 'Ctrl' presionada.\n\n")
        self._insert_text(textbox, "4.  Haz clic en el botón 'Eliminar Seleccionadas' y confirma la acción.\n\n")
        self._insert_text(textbox, "5.  Usa el botón 'Actualizar Lista' para recargar los datos desde la base de datos en cualquier momento.")

    def _populate_analisis_tab(self, tab):
        textbox = ctk.CTkTextbox(tab, wrap="word", border_spacing=10, fg_color="transparent")
        textbox.pack(expand=True, fill="both", padx=5, pady=5)

        self._insert_text(textbox, "Consultar Registros y Estadísticas\n\n", heading=True)
        self._insert_text(textbox, "El sistema ofrece dos ventanas para consultar datos históricos y de uso:\n\n")
        self._insert_text(textbox, "Análisis de Datos:\n", heading=True)
        self._insert_text(textbox, "   • Muestra estadísticas clave como los alumnos con más solicitudes, las salas más ocupadas y los horarios de mayor actividad.\n")
        self._insert_text(textbox, "   • Puedes filtrar los datos por año, mes y/o día para un análisis más específico.\n\n")
        self._insert_text(textbox, "Registro de Desocupación:\n", heading=True)
        self._insert_text(textbox, "   • Muestra un historial de las últimas 100 reservas que ya han finalizado, indicando qué alumno desocupó qué sala y cuándo.")
        
    def _populate_settings_tab(self, tab):
        textbox = ctk.CTkTextbox(tab, wrap="word", border_spacing=10, fg_color="transparent")
        textbox.pack(expand=True, fill="both", padx=5, pady=5)

        self._insert_text(textbox, "Configurar la Aplicación\n\n", heading=True)
        self._insert_text(textbox, "Personaliza tu experiencia con las siguientes opciones:\n\n")
        self._insert_text(textbox, "Habilitar Sonidos:\n", heading=True)
        self._insert_text(textbox, "   • Activa o desactiva los sonidos de notificación que se producen al hacer clic en botones o realizar acciones.\n\n")
        self._insert_text(textbox, "Tema de Color:\n", heading=True)
        self._insert_text(textbox, "   • Cambia la paleta de colores de la aplicación entre las opciones disponibles (blue, dark-blue, green).\n\n")
        self._insert_text(textbox, "Guardar y Aplicar:\n", heading=True)
        self._insert_text(textbox, "   • Haz clic en este botón para que tus cambios en la configuración se guarden y apliquen permanentemente.")