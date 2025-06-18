# main_app.py
import tkinter as tk
from ui_splash_screen import SplashScreen
from ui_login import LoginWindow
from ui_main_menu import MainMenuWindow
from db_connection import setup_database # Importa la función de configuración de la base de datos

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Salas")
        self.geometry("800x600") # Tamaño inicial de la ventana principal
        self.withdraw() # Oculta la ventana principal al inicio

        # Muestra la Splash Screen y pasa la tarea de setup de la DB
        self.splash_screen = SplashScreen(self, setup_task=setup_database)
        self.splash_screen.wait_window() # Espera a que la splash screen se cierre

        # Después de que la splash screen se cierra, muestra la ventana principal
        # y luego la ventana de login.
        self.deiconify() # Muestra la ventana principal (self.parent) después de que la splash se haya ido
        self.login_window = LoginWindow(self)
        self.login_window.wait_window() # Espera a que la ventana de login se cierre

    def after_login_success(self):
        # Este método es llamado por LoginWindow cuando el login es exitoso
        self.main_menu_window = MainMenuWindow(self)
        # No usamos wait_window() aquí porque el menú principal debe permanecer abierto
        # y permite interactuar con otras ventanas hijas.

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()