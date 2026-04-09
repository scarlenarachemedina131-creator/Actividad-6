import tkinter as tk
from tkinter import ttk, messagebox 
from ..service.task_service import TaskService



class AppWindow(tk.Tk):

    def __init__(self, task_service: TaskService) -> None:
        super().__init__()
        self._task_service = task_service

        self.title("Administrador de tareas")
        self.geometry("600x500")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self) -> None:
        #Para centrar el contenido
        self.grid_columnconfigure(0, weight=1)
        # Título principal
        tk.Label(self, text="Administrador de tareas", font=("Arial", 18, "bold")).pack(pady=10)

        # Formulario de creacion
        form_frame = tk.Frame(self)
        form_frame.grid(row=1, column=0,pady=5)

        tk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky="e", padx=5, pady=4)
        self.input_title = tk.Entry(form_frame, width=35)
        self.input_title.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky="e", padx=5, pady=4)
        self.input_description = tk.Entry(form_frame, width=35)
        self.input_description.grid(row=1, column=1, padx=5, pady=4)

        tk.Button(self, text="Agregar tarea", command=self.register_task, background="#28a745", foreground="black").grid(row=2, column=0, pady=8)

        # Treeview 
        columns = ("col_uuid", "col_title", "col_desc")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("col_uuid",  text="UUID")
        self.tree.heading("col_title", text="Título")
        self.tree.heading("col_desc",  text="Descripción")

        self.tree.column("col_uuid",  width=220, anchor="center")
        self.tree.column("col_title", width=200, anchor="center")
        self.tree.column("col_desc",  width=200, anchor="w")

        self.tree.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")    

        # Carga inicial de datos
        self.refresh_table()

    def register_task(self) -> None:
        title       = self.input_title.get().strip()
        description = self.input_description.get().strip()

        if not title or not description:
            messagebox.showwarning("Faltan datos, por favor ingresa el titulo y la descripcion.")
            return

        self._task_service.create_one_task(title, description)  # método correcto del service
        self.refresh_table()
        self.clear_inputs()

    def refresh_table(self) -> None:
        # Limpiar filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todas las tareas desde el servicio (acceso por atributo, no por clave)
        for task in self._task_service.get_all_tasks():
            self.tree.insert("", "end", values=(task.uuid, task.title, task.description))

    def clear_inputs(self) -> None:
        self.input_title.delete(0, "end")
        self.input_description.delete(0, "end")
