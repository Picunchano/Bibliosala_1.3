# --- Versión Final y Completa: main_app.py ---
import customtkinter as ctk
import datetime
from ui_splash_screen import SplashScreen
from ui_login import LoginWindow
from ui_main_menu import MainMenuWindow
from ui_notification_popup import NotificationPopup
from db_connection import setup_database
from data_manager import get_all_reservations
from config_manager import load_settings
from config import ICON_PATH

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.iconbitmap(ICON_PATH)
        self.settings = load_settings()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(self.settings.get("color_theme", "dark-blue"))
        self.title("Sistema de Gestión de Salas - Bibliosala")
        self.state('zoomed')
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Ocultar la ventana hasta que el login sea exitoso
        self.withdraw()
        
        # Variables de estado de la aplicación
        self.main_menu = None
        self.notificaciones_mostradas = set()
        self.primer_chequeo_completado = False
        
        # Agendar el proceso de arranque para después de que inicie el mainloop
        self.after(100, self.run_startup_process)

    def run_startup_process(self):
        """Muestra el splash, ejecuta el setup de la DB y luego muestra la ventana de login."""
        splash = SplashScreen(self, setup_task=setup_database)
        self.wait_window(splash)
        
        login_window = LoginWindow(self)
        self.wait_window(login_window)

    def after_login_success(self):
        """Se ejecuta después de un inicio de sesión exitoso."""
        # Muestra el menú principal
        self.main_menu = MainMenuWindow(self)
        self.main_menu.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Hace visible la ventana principal
        self.deiconify()
        self.focus_force()
        
        # Inicia el ciclo de revisión de notificaciones
        self.iniciar_chequeo_reservas()

    def _on_closing(self):
        """Maneja el cierre de la aplicación."""
        self.destroy()

    def iniciar_chequeo_reservas(self):
        """Comprueba periódicamente si alguna reserva ha finalizado y muestra una notificación."""
        reservas = get_all_reservations()
        ahora = datetime.datetime.now()

        for reserva in reservas:
            try:
                fecha_fin_str = f"{reserva['FechaPrestamo']} {reserva['HoraFin']}"
                fecha_fin_obj = datetime.datetime.strptime(fecha_fin_str, "%d/%m/%Y %H:%M:%S")
                reserva_id = reserva['id_prestamo']

                # Si la reserva ha terminado...
                if fecha_fin_obj < ahora:
                    # Y si no es la primera revisión y la notificación no se ha mostrado...
                    if self.primer_chequeo_completado and reserva_id not in self.notificaciones_mostradas:
                        # ...muestra la notificación.
                        NotificationPopup(self, reserva['NombreAlumnoCompleto'], reserva['NumeroSala'])
                        self.notificaciones_mostradas.add(reserva_id)
                    else:
                        # Para la primera revisión, solo registra las reservas ya terminadas sin notificar.
                        self.notificaciones_mostradas.add(reserva_id)
            except (ValueError, KeyError):
                continue
        
        # Marca la primera revisión como completada para activar las notificaciones futuras.
        if not self.primer_chequeo_completado:
            self.primer_chequeo_completado = True
            print("INFO: Carga inicial de reservas finalizadas completada. Las notificaciones están activas.")

        # Agenda la próxima revisión en 15 segundos
        self.after(15000, self.iniciar_chequeo_reservas)

# Este bloque es el que inicia toda la aplicación. Si falta, el programa no hace nada.
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()