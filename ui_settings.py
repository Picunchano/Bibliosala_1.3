# --- Archivo Actualizado: ui_settings.py ---
import customtkinter as ctk
from tkinter import messagebox
from config_manager import load_settings, save_settings, DEFAULT_SETTINGS
from data_manager import play_sound_if_enabled
from config import ICON_PATH # <-- Se importa la ruta del ícono

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.iconbitmap(ICON_PATH) # <-- Se establece el ícono para esta ventana
        self.title("Configuración")
        self.geometry("400x300")
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.settings = load_settings()
        self._crear_widgets()

    def _crear_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="Opciones de Configuración", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        self.sound_var = ctk.BooleanVar(value=self.settings.get("sound_enabled", DEFAULT_SETTINGS["sound_enabled"]))
        sound_checkbox = ctk.CTkCheckBox(main_frame, text="Habilitar Sonidos", variable=self.sound_var)
        sound_checkbox.pack(anchor="w", pady=10)
        color_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        color_frame.pack(anchor="w", pady=10)
        ctk.CTkLabel(color_frame, text="Tema de Color:").pack(side="left", padx=(0,10))
        self.color_theme_var = ctk.StringVar(value=self.settings.get("color_theme", DEFAULT_SETTINGS["color_theme"]))
        color_options = ["blue", "dark-blue", "green"]
        color_option_menu = ctk.CTkOptionMenu(color_frame, variable=self.color_theme_var, values=color_options, command=self._apply_color_theme)
        color_option_menu.pack(side="left")
        btn_guardar = ctk.CTkButton(main_frame, text="Guardar y Aplicar", command=self._save_current_settings)
        btn_guardar.pack(pady=20)
        btn_reset = ctk.CTkButton(main_frame, text="Restablecer por Defecto", command=self._reset_to_default)
        btn_reset.pack(pady=5)

    def _save_current_settings(self):
        self.settings["sound_enabled"] = self.sound_var.get()
        self.settings["color_theme"] = self.color_theme_var.get()
        save_settings(self.settings)
        ctk.set_default_color_theme(self.settings["color_theme"])
        play_sound_if_enabled()
        messagebox.showinfo("Configuración", "Configuración guardada exitosamente.", parent=self)

    def _apply_color_theme(self, choice):
        ctk.set_default_color_theme(choice)
        play_sound_if_enabled()

    def _reset_to_default(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.sound_var.set(self.settings["sound_enabled"])
        self.color_theme_var.set(self.settings["color_theme"])
        ctk.set_default_color_theme(self.settings["color_theme"])
        save_settings(self.settings)
        play_sound_if_enabled()
        messagebox.showinfo("Configuración", "Configuración restablecida a valores por defecto.", parent=self)

    def _on_close(self):
        play_sound_if_enabled()
        self.destroy()