# --- Archivo Actualizado: ui_splash_screen.py ---
import customtkinter as ctk
import tkinter as tk
import threading
import time
import queue
from PIL import Image, ImageTk  # <-- 1. Se importa la librería Pillow

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent, setup_task=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_task = setup_task

        self.title("Cargando Bibliosala...") #
        self.geometry("400x250") #
        self.overrideredirect(True) #
        self.attributes("-topmost", True) #
        self.resizable(False, False) #

        # Centrar la splash screen
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2) #
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2) #
        self.geometry(f"+{x}+{y}") #

        self.queue = queue.Queue()
        self._create_widgets()
        
        threading.Thread(target=self._run_setup_task, daemon=True).start()
        self.process_queue()

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent") #
        main_frame.pack(expand=True, fill='both', padx=20, pady=20) #

        try:
            from config import LOGO_PATH
            
            # --- INICIO DE LA MODIFICACIÓN ---
            # 2. Abrir la imagen original usando Pillow
            pil_image = Image.open(LOGO_PATH)

            # 3. Definir un tamaño máximo para la imagen para que no tape los otros elementos
            max_width = 380
            max_height = 150  # Se reduce la altura para dejar espacio abajo

            # 4. Redimensionar la imagen manteniendo su proporción (thumbnail es ideal para esto)
            pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # 5. Convertir la imagen de Pillow (redimensionada) a un formato que CustomTkinter pueda usar
            self.logo_image = ImageTk.PhotoImage(pil_image)
            # --- FIN DE LA MODIFICACIÓN ---
            
            logo_label = ctk.CTkLabel(main_frame, image=self.logo_image, text="") #
            logo_label.pack(pady=(0, 10)) #

        except Exception as e:
            print(f"Error al cargar o redimensionar la imagen: {e}")
            # Si falla, se muestra el texto "Bibliosala" como antes
            ctk.CTkLabel(main_frame, text="Bibliosala", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(0, 10)) #

        # El resto de los widgets se mantienen igual
        self.status_label = ctk.CTkLabel(main_frame, text="Inicializando...", font=ctk.CTkFont(size=14)) #
        self.status_label.pack(pady=(10, 5)) #

        self.progressbar = ctk.CTkProgressBar(main_frame, mode="indeterminate") #
        self.progressbar.pack(fill='x', pady=(5, 10)) #
        self.progressbar.start()
    
    # El resto de las funciones de la clase no cambian...
    def process_queue(self):
        try:
            message = self.queue.get_nowait()
            if callable(message):
                message()
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

    def _run_setup_task(self):
        time.sleep(1) #
        self.queue.put(lambda: self.status_label.configure(text="Configurando base de datos...")) #
        success = True #
        if self.setup_task: #
            success = self.setup_task() #
        if not success:
            def update_ui_on_failure():
                self.progressbar.stop()
                self.status_label.configure(text="Error de inicialización. Verifique la consola.", text_color="red") #
                self.after(3000, self.parent.destroy) #
            self.queue.put(update_ui_on_failure)
            return
        def update_ui_on_success():
            self.progressbar.set(1.0) #
            self.progressbar.stop()
            self.status_label.configure(text="Completado. Iniciando aplicación...") #
            self.after(500, self.destroy) #
        self.queue.put(update_ui_on_success)