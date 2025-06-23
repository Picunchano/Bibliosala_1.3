# --- Archivo Actualizado: ui_login.py ---
import customtkinter as ctk
from tkinter import messagebox
from data_manager import validate_user, play_sound_if_enabled
from config import ICON_PATH  # <-- Se importa la ruta del ícono

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.iconbitmap(ICON_PATH)  # <-- Se establece el ícono para esta ventana
        self.title("Iniciar Sesión")
        self.geometry("350x280")
        self.resizable(False, False)
        self.grab_set()
        self.transient(parent)

        self.after(20, self._center_window)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._create_widgets()

    def _center_window(self):
        try:
            self.update_idletasks()
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.winfo_width() // 2)
            y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.winfo_height() // 2)
            self.geometry(f"+{x}+{y}")
        except Exception as e:
            print(f"DEBUG: No se pudo centrar la ventana de login: {e}")

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill='both', padx=25, pady=20)
        ctk.CTkLabel(main_frame, text="Bienvenido", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)
        ctk.CTkLabel(main_frame, text="Usuario:").pack(anchor="w", pady=(10, 2))
        self.username_entry = ctk.CTkEntry(main_frame, width=250)
        self.username_entry.pack(fill='x', pady=(0, 10))
        self.username_entry.focus_set()
        ctk.CTkLabel(main_frame, text="Contraseña:").pack(anchor="w", pady=(10, 2))
        self.password_entry = ctk.CTkEntry(main_frame, show="*", width=250)
        self.password_entry.pack(fill='x', pady=(0, 20))
        self.password_entry.bind("<Return>", lambda event: self._attempt_login())
        login_button = ctk.CTkButton(main_frame, text="Entrar", command=self._attempt_login, height=40)
        login_button.pack(fill='x')

    def _attempt_login(self):
        play_sound_if_enabled()
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = validate_user(username, password)
        if user:
            self.parent.after_login_success()
            self.destroy()
        else:
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.", parent=self)
            self.password_entry.delete(0, 'end')
            self.username_entry.focus_set()

    def _on_closing(self):
        self.parent.destroy()