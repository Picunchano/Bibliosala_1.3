<<<<<<< HEAD
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
=======
# --- Archivo Completo y Reestructurado: main_app.py ---
import customtkinter as ctk
from ui_splash_screen import SplashScreen
from ui_login import LoginWindow
from ui_main_menu import MainMenuWindow
from db_connection import setup_database
from config_manager import load_settings

class MainApplication(ctk.CTk):
    def __init__(self):
        print("DEBUG: 1. MainApplication: __init__ ha comenzado.")
        super().__init__()

        # 1. Configuración básica de la ventana principal
        self.settings = load_settings()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(self.settings.get("color_theme", "dark-blue"))
        self.title("Sistema de Gestión de Salas - Bibliosala")
        self.state('zoomed')
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # La ventana principal se esconde. Se mostrará solo después de un login exitoso.
        self.withdraw()

        self.main_menu = None # El menú se creará después

        print("DEBUG: 2. MainApplication: __init__ finalizado. Se agenda el proceso de arranque.")
        # 2. Agendamos el proceso de arranque para que se ejecute DESPUÉS de que inicie el mainloop
        self.after(100, self.run_startup_process)

    def run_startup_process(self):
        """Muestra el splash, ejecuta el setup de la DB y luego muestra la ventana de login."""
        print("DEBUG: 3. MainApplication: run_startup_process() ha comenzado.")
        
        # --- Muestra el Splash Screen ---
        splash = SplashScreen(self, setup_task=setup_database)
        self.wait_window(splash) # Esto es seguro aquí porque el mainloop ya está corriendo

        # --- Inicia el Proceso de Login ---
        print("DEBUG: 4. MainApplication: Se va a crear y mostrar la ventana de Login.")
        login_window = LoginWindow(self)
        self.wait_window(login_window)

        # Este punto solo se alcanza si la ventana de login se cierra.
        # Si el login fue exitoso, la ventana principal ya estará visible.
        # Si el usuario cerró la ventana de login con la 'X', la app ya se habrá cerrado.
        print("DEBUG: 8. MainApplication: El proceso de login ha terminado.")


    def after_login_success(self):
        """Esta función es llamada por LoginWindow cuando el login es exitoso."""
        print("DEBUG: 6. MainApplication: after_login_success() ha sido LLAMADO.")
        try:
            # Crea y empaqueta el menú principal en la ventana
            self.main_menu = MainMenuWindow(self)
            self.main_menu.pack(expand=True, fill='both', padx=20, pady=20)

            # 3. AHORA, con la ventana ya poblada con el menú, la hacemos visible.
            self.deiconify()
            self.focus_force() # La traemos al frente
            print("DEBUG: 7. MainApplication: after_login_success() COMPLETADO. Ventana principal visible.")
        except Exception as e:
            print(f"ERROR: Ha ocurrido un error dentro de after_login_success(): {e}")

    def _on_closing(self):
        print("DEBUG: La ventana principal se está cerrando...")
        self.destroy()


if __name__ == "__main__":
    print("DEBUG: El programa ha comenzado a ejecutarse.")
    app = MainApplication()
    print("DEBUG: Objeto MainApplication creado. Llamando a mainloop().")
    app.mainloop()
    # Este último print solo aparecerá en la consola cuando cierres la aplicación de forma normal.
    print("DEBUG: mainloop() ha terminado. La aplicación se está cerrando definitivamente.")
>>>>>>> 60afa05422fad075c9a22e8d54eae8e369eb6486
