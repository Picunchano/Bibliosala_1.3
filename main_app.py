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