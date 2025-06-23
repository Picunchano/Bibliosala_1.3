# --- Archivo Actualizado: ui_notification_popup.py ---
import customtkinter as ctk
from data_manager import play_sound_if_enabled
from config import ICON_PATH # <-- Se importa la ruta del ícono

class NotificationPopup(ctk.CTkToplevel):
    def __init__(self, parent, student_name, room_number):
        super().__init__(parent)

        self.iconbitmap(ICON_PATH) # <-- Se establece el ícono para esta ventana
        self.title("Reserva Finalizada")
        self.geometry("400x150")
        self.resizable(False, False)

        self.grab_set()
        self.transient(parent)
        self.attributes("-topmost", True)

        play_sound_if_enabled()
        self.after(10, self.center_on_screen)

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        message = f"El estudiante {student_name}\nha finalizado su tiempo en la Sala {room_number}."
        label = ctk.CTkLabel(main_frame, text=message, font=ctk.CTkFont(size=16))
        label.pack(expand=True)
        ok_button = ctk.CTkButton(main_frame, text="Aceptar", command=self.destroy, width=120)
        ok_button.pack(pady=(10, 0))
        ok_button.focus()

    def center_on_screen(self):
        try:
            self.update_idletasks()
            window_width = self.winfo_width()
            window_height = self.winfo_height()
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = int((screen_width / 2) - (window_width / 2))
            y = int((screen_height / 2) - (window_height / 2))
            self.geometry(f"+{x}+{y}")
        except Exception as e:
            print(f"No se pudo centrar la ventana de notificación: {e}")