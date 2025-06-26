# --- Archivo Actualizado: ui_ver_reservas.py ---
import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import get_all_reservations, eliminar_reservas_por_timestamps, play_sound_if_enabled
from config import ICON_PATH

class VerReservasWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.withdraw() # Ocultar la ventana

        self.iconbitmap(ICON_PATH)
        self.title("Ver Reservas")
        self.geometry("900x600")
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.reservas_cargadas = []
        self.selected_reservation_ids = set()

        self._crear_widgets()
        self._cargar_reservas()
        
        self.after(10, self._center_and_show) # Centrar y mostrar

    def _center_and_show(self):
        """Centra la ventana en la pantalla y la hace visible."""
        try:
            self.update_idletasks()
            width = self.winfo_width()
            height = self.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
            self.geometry(f'{width}x{height}+{x}+{y}')
        finally:
            self.deiconify()

    def _crear_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        columns = ("ID", "RUT Alumno", "Nombre Completo", "Carrera", "Email", "Sala", "Fecha", "Hora Inicio", "Hora Fin", "Tipo")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.column("ID", width=50)
        self.tree.column("RUT Alumno", width=90)
        self.tree.column("Nombre Completo", width=150)
        self.tree.column("Carrera", width=100)
        self.tree.column("Email", width=120)
        self.tree.column("Sala", width=60)
        self.tree.column("Fecha", width=90)
        self.tree.column("Hora Inicio", width=80)
        self.tree.column("Hora Fin", width=80)
        self.tree.column("Tipo", width=70)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        btn_actualizar = ttk.Button(button_frame, text="Actualizar Lista", command=self._cargar_reservas)
        btn_actualizar.pack(side="left", padx=5)
        btn_eliminar_seleccionadas = ttk.Button(button_frame, text="Eliminar Seleccionadas", command=self._eliminar_reservas_seleccionadas)
        btn_eliminar_seleccionadas.pack(side="left", padx=5)

    def _cargar_reservas(self):
        play_sound_if_enabled()
        self.reservas_cargadas = get_all_reservations()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.selected_reservation_ids.clear()
        if not self.reservas_cargadas:
            self.tree.insert("", "end", values=("No hay reservas para mostrar.", "", "", "", "", "", "", "", "", ""), tags=('no_data',))
            self.tree.tag_configure('no_data', foreground='gray')
        else:
            for reserva in self.reservas_cargadas:
                self.tree.insert("", "end", iid=reserva['id_prestamo'],
                                 values=(
                                     reserva.get('id_prestamo', 'N/A'),
                                     reserva.get('RUTAlumno', 'N/A'),
                                     reserva.get('NombreAlumnoCompleto', 'N/A'),
                                     reserva.get('CarreraAlumno', 'N/A'),
                                     reserva.get('EmailAlumno', 'N/A'),
                                     reserva.get('NumeroSala', 'N/A'),
                                     reserva.get('FechaPrestamo', 'N/A'),
                                     reserva.get('HoraInicio', 'N/A'),
                                     reserva.get('HoraFin', 'N/A'),
                                     reserva.get('IndividualOGrupal', 'N/A')
                                 ))

    def _on_tree_select(self, event):
        current_selection = self.tree.selection()
        self.selected_reservation_ids.clear()
        for item_id in current_selection:
            self.selected_reservation_ids.add(int(item_id))

    def _eliminar_reservas_seleccionadas(self):
        play_sound_if_enabled()
        if not self.selected_reservation_ids:
            messagebox.showwarning("Advertencia", "No hay reservas seleccionadas para eliminar.", parent=self)
            return
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar {len(self.selected_reservation_ids)} reserva(s) seleccionada(s)?",
            parent=self
        )
        if confirm:
            if eliminar_reservas_por_timestamps(list(self.selected_reservation_ids)):
                messagebox.showinfo("Éxito", "Reserva(s) eliminada(s) correctamente.", parent=self)
                self._cargar_reservas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la(s) reserva(s).", parent=self)
        
    def _on_close(self):
        play_sound_if_enabled()
        self.destroy()