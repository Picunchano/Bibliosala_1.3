# --- Archivo Actualizado: main_app.py ---
import customtkinter as ctk
from ui_splash_screen import SplashScreen
from ui_login import LoginWindow
from ui_main_menu import MainMenuWindow
from db_connection import setup_database
from config_manager import load_settings
from config import ICON_PATH  # <-- 1. Se importa la nueva ruta del ícono

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- INICIO DE LA MODIFICACIÓN ---
        # 2. Se usa la variable ICON_PATH para establecer el ícono
        self.iconbitmap(ICON_PATH)
        # --- FIN DE LA MODIFICACIÓN ---

        self.settings = load_settings()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(self.settings.get("color_theme", "dark-blue"))

        self.title("Sistema de Gestión de Salas - Bibliosala")
        self.state('zoomed')
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.withdraw()
        self.main_menu = None
        self.notificaciones_mostradas = set()
        self.primer_chequeo_completado = False
        
        self.after(100, self.run_startup_process)

    # (El resto del archivo main_app.py no necesita cambios)
    def run_startup_process(self):
        splash = SplashScreen(self, setup_task=setup_database)
        self.wait_window(splash)
        login_window = LoginWindow(self)
        self.wait_window(login_window)

    def after_login_success(self):
        self.main_menu = MainMenuWindow(self)
        self.main_menu.pack(expand=True, fill='both', padx=20, pady=20)
        self.deiconify()
        self.focus_force()
        self.iniciar_chequeo_reservas()

    def _on_closing(self):
        self.destroy()

    def iniciar_chequeo_reservas(self):
        import datetime
        from data_manager import get_all_reservations
        reservas = get_all_reservations()
        ahora = datetime.datetime.now()
        for reserva in reservas:
            try:
                fecha_fin_str = f"{reserva['FechaPrestamo']} {reserva['HoraFin']}"
                fecha_fin_obj = datetime.datetime.strptime(fecha_fin_str, "%d/%m/%Y %H:%M:%S")
                reserva_id = reserva['id_prestamo']
                if fecha_fin_obj < ahora:
                    if self.primer_chequeo_completado and reserva_id not in self.notificaciones_mostradas:
                        from ui_notification_popup import NotificationPopup
                        NotificationPopup(self, reserva['NombreAlumnoCompleto'], reserva['NumeroSala'])
                        self.notificaciones_mostradas.add(reserva_id)
                    else:
                        self.notificaciones_mostradas.add(reserva_id)
            except (ValueError, KeyError):
                continue
        if not self.primer_chequeo_completado:
            self.primer_chequeo_completado = True
            print("INFO: Carga inicial de reservas finalizadas completada. Las notificaciones están activas.")
        self.after(15000, self.iniciar_chequeo_reservas)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()