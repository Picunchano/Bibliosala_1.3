# ui_ver_reservas.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from data_manager import cargar_reservas, eliminar_reservas_por_timestamps, play_sound

class VerReservasWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Ver Reservas")
        self.geometry("1100x600") # Ampliado para nuevas columnas
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.reservas = []
        self._crear_widgets()
        self._cargar_reservas_en_tabla(modo_activo=True)

    def _crear_widgets(self):
        modo_frame = ttk.Frame(self, padding="10")
        modo_frame.pack(fill=tk.X)

        self.modo_var = tk.StringVar(value="activas")
        rb_activas = ttk.Radiobutton(modo_frame, text="Reservas Activas", variable=self.modo_var, value="activas", command=self._cambiar_modo_vista)
        rb_activas.pack(side=tk.LEFT, padx=10)
        rb_historial = ttk.Radiobutton(modo_frame, text="Historial de Reservas", variable=self.modo_var, value="historial", command=self._cambiar_modo_vista)
        rb_historial.pack(side=tk.LEFT, padx=10)

        btn_frame = ttk.Frame(self, padding="10")
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Actualizar Lista", command=self._actualizar_lista).pack(side=tk.LEFT, padx=5)
        self.delete_button = ttk.Button(btn_frame, text="Eliminar Seleccionadas", command=self._eliminar_reservas, state=tk.DISABLED)
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        # Columnas actualizadas
        columns = ("RUT", "Nombre Completo", "Carrera", "Email", "Sala", "Fecha Préstamo", "Hora Inicio", "Hora Fin", "Tipo Préstamo")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("RUT", text="RUT")
        self.tree.heading("Nombre Completo", text="Nombre Completo")
        self.tree.heading("Carrera", text="Carrera")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Sala", text="Sala")
        self.tree.heading("Fecha Préstamo", text="Fecha Préstamo")
        self.tree.heading("Hora Inicio", text="Hora Inicio")
        self.tree.heading("Hora Fin", text="Hora Fin")
        self.tree.heading("Tipo Préstamo", text="Tipo Préstamo")

        self.tree.column("RUT", width=90, anchor=tk.CENTER)
        self.tree.column("Nombre Completo", width=160, anchor=tk.W)
        self.tree.column("Carrera", width=100, anchor=tk.W)
        self.tree.column("Email", width=150, anchor=tk.W)
        self.tree.column("Sala", width=70, anchor=tk.CENTER)
        self.tree.column("Fecha Préstamo", width=90, anchor=tk.CENTER)
        self.tree.column("Hora Inicio", width=70, anchor=tk.CENTER)
        self.tree.column("Hora Fin", width=70, anchor=tk.CENTER)
        self.tree.column("Tipo Préstamo", width=90, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_treeview_select)

    def _cambiar_modo_vista(self):
        play_sound()
        modo_activo = (self.modo_var.get() == "activas")
        self._cargar_reservas_en_tabla(modo_activo)
        self.delete_button.config(state=tk.DISABLED)

    def _actualizar_lista(self):
        play_sound()
        modo_activo = (self.modo_var.get() == "activas")
        self._cargar_reservas_en_tabla(modo_activo)
        messagebox.showinfo("Actualizado", "La lista de reservas ha sido actualizada.", parent=self)

    def _cargar_reservas_en_tabla(self, modo_activo=True):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.reservas = cargar_reservas()

        now = datetime.datetime.now()

        for reserva in self.reservas:
            try:
                iid = reserva.get('id_prestamo')

                fecha_str = reserva.get('FechaPrestamo', 'N/A')
                hora_inicio_str = reserva.get('HoraInicio', 'N/A')
                hora_fin_str = reserva.get('HoraFin', 'N/A')

                reserva_datetime_inicio = None
                reserva_datetime_fin = None
                try:
                    fecha_obj = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
                    hora_inicio_obj = datetime.datetime.strptime(hora_inicio_str, "%H:%M").time()
                    hora_fin_obj = datetime.datetime.strptime(hora_fin_str, "%H:%M").time()

                    reserva_datetime_inicio = datetime.datetime.combine(fecha_obj, hora_inicio_obj)
                    reserva_datetime_fin = datetime.datetime.combine(fecha_obj, hora_fin_obj)
                except ValueError:
                    pass

                is_active = False
                if reserva_datetime_inicio and reserva_datetime_fin:
                    is_active = (reserva_datetime_inicio <= now <= reserva_datetime_fin)

                if modo_activo and not is_active:
                    continue

                values = (
                    reserva.get('RUTAlumno', 'N/A'),
                    reserva.get('NombreAlumnoCompleto', 'N/A'),
                    reserva.get('CarreraAlumno', 'N/A'),
                    reserva.get('EmailAlumno', 'N/A'),
                    reserva.get('NumeroSala', 'N/A'),
                    fecha_str,
                    hora_inicio_str,
                    hora_fin_str,
                    reserva.get('IndividualOGrupal', 'N/A')
                )
                self.tree.insert("", tk.END, iid=iid, values=values)
            except KeyError as e:
                print(f"Advertencia: Datos de reserva incompletos o mal formados. Falta clave: {e}. Datos: {reserva}")

    def _on_treeview_select(self, event):
        selected_items = self.tree.selection()
        if selected_items and self.modo_var.get() == "historial":
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)

    def _eliminar_reservas(self):
        play_sound()
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Ninguna Selección", "Por favor, seleccione las reservas a eliminar.", parent=self)
            return

        confirm = messagebox.askyesno("Confirmar Eliminación",
                                      f"¿Está seguro de que desea eliminar {len(selected_items)} reserva(s) seleccionada(s)? Esta acción es irreversible.",
                                      parent=self)
        if confirm:
            ids_to_delete = [self.tree.item(item)['iid'] for item in selected_items]

            if eliminar_reservas_por_timestamps(ids_to_delete):
                messagebox.showinfo("Éxito", f"{len(ids_to_delete)} reserva(s) eliminada(s) correctamente.", parent=self)
                self._cargar_reservas_en_tabla(modo_activo=False) # Recargar historial
            else:
                messagebox.showerror("Error", "No se pudo eliminar la(s) reserva(s).", parent=self)
        self.delete_button.config(state=tk.DISABLED)

    def _on_close(self):
        play_sound()
        self.destroy()