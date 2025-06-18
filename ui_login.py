# ui_login.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import ADMIN_USERNAME, ADMIN_PASSWORD # Importar credenciales fijas
from data_manager import play_sound # Para el sonido

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Iniciar Sesión")
        self.geometry("350x250")
        self.resizable(False, False)
        self.grab_set()  # Hace la ventana modal
        self.transient(parent) # La ventana de login es hija de la principal

        # Centrar la ventana de login
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Título
        ttk.Label(main_frame, text="Bienvenido", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Campo de Usuario
        ttk.Label(main_frame, text="Usuario:").pack(anchor="w", pady=(10, 2))
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))
        self.username_entry.focus_set() # Poner el foco al inicio

        # Campo de Contraseña
        ttk.Label(main_frame, text="Contraseña:").pack(anchor="w", pady=(10, 2))
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        self.password_entry.bind("<Return>", lambda event: self._attempt_login())

        # Botón de Iniciar Sesión
        login_button = ttk.Button(main_frame, text="Entrar", command=self._attempt_login)
        login_button.pack(pady=10)

    def _attempt_login(self):
        play_sound()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validación simple contra credenciales fijas
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.parent.after_login_success() # Llama al método en la ventana principal
            self.destroy() # Cierra la ventana de login
        else:
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.", parent=self)
            self.password_entry.delete(0, tk.END) # Limpiar campo de contraseña
            self.username_entry.focus_set() # Volver a poner el foco en el usuario

    def _on_closing(self):
        # Si la ventana de login se cierra sin éxito, cierra la aplicación principal
        self.parent.destroy()