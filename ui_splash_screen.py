# ui_splash_screen.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk # Asegúrate de tener Pillow instalado: pip install Pillow
import threading
import time
from config import LOGO_PATH # Asegúrate de que LOGO_PATH está en config.py

class SplashScreen(tk.Toplevel):
    def __init__(self, parent, setup_task):
        super().__init__(parent)
        self.parent = parent
        self.setup_task = setup_task
        self.overrideredirect(True)  # Elimina bordes de la ventana
        self.geometry(self._center_window(400, 300))
        self.config(bg="white")

        self.logo_image = None
        try:
            original_image = Image.open(LOGO_PATH)
            # Redimensionar la imagen para que quepa en la ventana
            resized_image = original_image.resize((200, 200), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo del logo en '{LOGO_PATH}'.")
        except Exception as e:
            print(f"Error al cargar la imagen del logo: {e}")

        self._create_widgets()
        # self.parent.withdraw() # Esta línea ya no va aquí, se hace en MainApplication

        self.task_complete = False # Flag para señalizar la finalización de la tarea

        # Iniciar la tarea de setup en un hilo separado
        self.thread = threading.Thread(target=self._run_setup_task)
        self.thread.start()

        # Iniciar la verificación de la finalización de la tarea en el hilo principal de Tkinter
        # Este after es el que está en el hilo principal de la splash screen
        self.after(100, self._check_task_completion) # Verifica cada 100ms

    def _center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return f"{width}x{height}+{int(x)}+{int(y)}"

    def _create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        if self.logo_image:
            logo_label = tk.Label(main_frame, image=self.logo_image, bg="white")
            logo_label.pack(pady=10)
        else:
            no_logo_label = ttk.Label(main_frame, text="Sistema de Reservas", font=("Helvetica", 20, "bold"), background="white")
            no_logo_label.pack(pady=10)


        ttk.Label(main_frame, text="Cargando aplicación...", font=("Helvetica", 12), background="white").pack(pady=5)

        self.progress_bar = ttk.Progressbar(main_frame, mode="indeterminate", length=250)
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10) # Velocidad del movimiento

    def _run_setup_task(self):
        try:
            self.setup_task() # Ejecuta la función de setup de la DB
        finally:
            # Espera un poco para que el usuario vea la pantalla de carga
            time.sleep(1.5)
            self.task_complete = True # Señaliza que la tarea ha terminado

    def _check_task_completion(self):
        # Este método se ejecuta en el hilo principal de Tkinter de la splash screen
        if self.task_complete:
            self.destroy() # Cierra la splash screen
        else:
            self.after(100, self._check_task_completion) # Vuelve a programar la verificación