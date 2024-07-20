import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import csv
from ver_gastos import VerGastosPage

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Gastos Personales")
        self.root.geometry("800x600")

        # Crear el menú
        self.create_menu()

        # Crear frames para la navegación
        self.frames = {}
        for F in (HomePage, VerGastosPage):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        menu_options = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menú", menu=menu_options)
        menu_options.add_command(label="Ver Gastos", command=lambda: self.show_frame("VerGastosPage"))
        menu_options.add_command(label="Añadir Gastos", command=lambda: self.show_frame("HomePage"))
        menu_options.add_command(label="Estadísticas", command=self.estadisticas)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def estadisticas(self):
        tk.messagebox.showinfo("Estadísticas", "Función de estadísticas aún no implementada.")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Campo de monto
        self.monto_label = ttk.Label(self, text="Monto:")
        self.monto_label.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.monto_entry = ttk.Entry(self)
        self.monto_entry.grid(column=1, row=0, padx=10, pady=10)
        self.monto_entry.bind("<KeyRelease>", self.validate_number)

        # Campo de fecha
        self.fecha_label = ttk.Label(self, text="Fecha:")
        self.fecha_label.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        self.fecha_entry = DateEntry(self, date_pattern='dd/mm/yyyy')
        self.fecha_entry.grid(column=1, row=1, padx=10, pady=10)

        # Campo de etiquetas
        self.etiquetas_label = ttk.Label(self, text="Etiquetas:")
        self.etiquetas_label.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
        self.etiquetas_button = ttk.Button(self, text="Seleccionar Etiquetas", command=self.open_tag_window)
        self.etiquetas_button.grid(column=1, row=2, padx=10, pady=10)

        # Etiquetas seleccionadas
        self.selected_tags_label = ttk.Label(self, text="")
        self.selected_tags_label.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)

        # Campo de descripción
        self.descripcion_label = ttk.Label(self, text="Descripción:")
        self.descripcion_label.grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
        self.descripcion_text = tk.Text(self, height=6, width=40)
        self.descripcion_text.grid(column=1, row=4, padx=10, pady=10)

        # Botón para añadir gasto
        self.add_button = ttk.Button(self, text="Añadir Gasto", command=self.add_expense)
        self.add_button.grid(column=1, row=5, padx=10, pady=10)

    def validate_number(self, event):
        value = self.monto_entry.get()
        if not value.isdigit():
            tk.messagebox.showwarning("Advertencia", "Ingrese solo números")
            self.monto_entry.delete(0, tk.END)

    def open_tag_window(self):
        tag_window = tk.Toplevel(self)
        tag_window.title("Seleccionar Etiquetas")

        # Obtener el tamaño de la ventana principal para centrar la ventana emergente
        win_width = 400
        win_height = 300
        root_width = self.winfo_width()
        root_height = self.winfo_height()
        root_x = self.winfo_rootx()
        root_y = self.winfo_rooty()
        x = root_x + (root_width // 2) - (win_width // 2)
        y = root_y + (root_height // 2) - (win_height // 2)
        tag_window.geometry(f"{win_width}x{win_height}+{x}+{y}")

        # Crear lista de etiquetas
        self.tag_listbox = tk.Listbox(tag_window, selectmode=tk.MULTIPLE)
        self.tag_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        etiquetas = ["Alimentación", "Transporte", "Entretenimiento", "Educación", "Salud"]
        for etiqueta in etiquetas:
            self.tag_listbox.insert(tk.END, etiqueta)

        select_button = ttk.Button(tag_window, text="Seleccionar", command=lambda: self.select_tags(tag_window))
        select_button.pack(padx=10, pady=10)

    def select_tags(self, tag_window):
        selected_tags = [self.tag_listbox.get(i) for i in self.tag_listbox.curselection()]
        self.selected_tags_label.config(text=f"Etiquetas seleccionadas: {', '.join(selected_tags)}")
        tag_window.destroy()

    def add_expense(self):
        monto = self.monto_entry.get()
        fecha = self.fecha_entry.get()
        descripcion = self.descripcion_text.get("1.0", tk.END).strip()
        etiquetas = self.selected_tags_label.cget("text").replace("Etiquetas seleccionadas: ", "")
        
        if monto and fecha and descripcion and etiquetas:
            with open('gastos.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([monto, fecha, descripcion, etiquetas])
            tk.messagebox.showinfo("Éxito", "Gasto añadido correctamente.")
        else:
            tk.messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
