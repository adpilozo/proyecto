import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from bd import Item, Registro
from Listado import Listado
from Estadisticas import Estadisticas

class GestionGastosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Gastos Personales")
        
        self.registro = Registro('items.csv')
        self.listado = Listado(self.registro.leer_items())

        self.create_menu()
        self.create_frames()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.gastos_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Menú", menu=self.gastos_menu)
        self.gastos_menu.add_command(label="Añadir Gastos", command=self.show_add_gastos)
        self.gastos_menu.add_command(label="Ver Gastos", command=self.show_view_gastos)
        self.gastos_menu.add_command(label="Estadísticas", command=self.show_estadisticas)

    def create_frames(self):
        self.frame = tk.Canvas(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.add_gastos_frame = self.create_add_gastos_frame()
        self.view_gastos_frame = self.create_view_gastos_frame()
        self.estadisticas_frame = self.create_estadisticas_frame()

        # Ventana Inicial
        self.show_view_gastos()

    def create_add_gastos_frame(self):
        frame = tk.Frame(self.frame)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text='Fecha (YYYY/MM/DD HH:MM:SS)').grid(row=0, column=0, padx=5, pady=5)
        self.fecha_entry = ttk.Entry(frame)
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text='Monto').grid(row=1, column=0, padx=5, pady=5)
        self.monto_entry = ttk.Entry(frame)
        self.monto_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text='Etiquetas').grid(row=2, column=0, padx=5, pady=5)
        self.etiquetas_entry = ttk.Entry(frame)
        self.etiquetas_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text='Descripción').grid(row=3, column=0, padx=5, pady=5)
        self.descripcion_entry = ttk.Entry(frame)
        self.descripcion_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(frame, text='Añadir Item', command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        return frame

    def create_view_gastos_frame(self):
        frame = tk.Frame(self.frame)
        frame.pack(fill=tk.BOTH, expand=True)

        # Filtros
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text='Fecha Inicio (YYYY/MM/DD)').grid(row=0, column=0, padx=5, pady=5)
        self.fecha_inicio_entry = ttk.Entry(filter_frame)
        self.fecha_inicio_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text='Fecha Fin (YYYY/MM/DD)').grid(row=1, column=0, padx=5, pady=5)
        self.fecha_fin_entry = ttk.Entry(filter_frame)
        self.fecha_fin_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text='Etiquetas (separadas por comas)').grid(row=2, column=0, padx=5, pady=5)
        self.etiquetas_buscar_entry = ttk.Entry(filter_frame)
        self.etiquetas_buscar_entry.grid(row=2, column=1, padx=5, pady=5)

        self.filter_button = ttk.Button(filter_frame, text='Filtrar', command=self.update_treeview)
        self.filter_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Treeview
        self.tree = ttk.Treeview(frame, columns=('Fecha', 'Monto', 'Etiquetas', 'Descripción'), show='headings')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Monto', text='Monto')
        self.tree.heading('Etiquetas', text='Etiquetas')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.pack(fill=tk.BOTH, expand=True)

        return frame

    def create_estadisticas_frame(self):
        frame = tk.Canvas(self.frame)
        frame.pack(fill=tk.BOTH, expand=True)

        # ttk.Label(frame, text='Fecha (YYYY/MM/DD HH:MM:SS)').grid(row=0, column=0, padx=5, pady=5)
        titulo = ttk.Label(frame, text="Predicción de Gastos", font=("Arial", 15, "bold"))
        titulo.pack(pady=20)

        statsYear = Estadisticas.predictNextYear(self.listado)
        statsMonth = Estadisticas.predictNextMonth(self.listado)

        # Sección Predicción Mes Siguiente
        ttk.Label(frame, text=f"Predicción Mes {statsMonth.fecha.month}, Año {statsMonth.fecha.year}", font=("Arial", 10, "bold")).pack(padx=5, pady=5)

        ttk.Label(frame, text=statsMonth.toSeparateString(etiquetas=False, desc=False)).pack(padx=5, pady=5)

        # Línea divisoria
        linDiv = ttk.Separator(frame, orient="horizontal")
        linDiv.pack(fill="x")

        # ScrollBar
        self.scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame.configure(yscrollcommand=self.scrollbar.set)

        # Sección Predicción Año Siguiente
        itemStatsYear = statsYear.getOldest().fecha
        ttk.Label(frame, text=f"Predicción Año {itemStatsYear.year - 1}/{itemStatsYear.month} - {itemStatsYear.year}/{itemStatsYear.month}", font=("Arial", 10, "bold")).pack(padx=5, pady=5)

        for item in statsYear.items:
            s = item.toSeparateString(etiquetas=False, desc=False, lastCharF=" --- ")
            ttk.Label(frame, text=s).pack(padx=5, pady=5)

        return frame

    def show_estadisticas_data(self):
        self.clear_frames()
        self.estadisticas_frame.pack(fill=tk.BOTH, expand=True)

    def show_add_gastos(self):
        self.clear_frames()
        self.add_gastos_frame.pack(fill=tk.BOTH, expand=True)

    def show_view_gastos(self):
        self.clear_frames()
        self.view_gastos_frame.pack(fill=tk.BOTH, expand=True)
        self.update_treeview()

    def show_estadisticas(self):
        self.clear_frames()
        self.estadisticas_frame.pack(fill=tk.BOTH, expand=True)
        self.show_estadisticas_data()

    def clear_frames(self):
        self.add_gastos_frame.pack_forget()
        self.view_gastos_frame.pack_forget()
        self.estadisticas_frame.pack_forget()

    def update_treeview(self):
        try:
            fecha_inicio_str = self.fecha_inicio_entry.get()
            fecha_fin_str = self.fecha_fin_entry.get()
            etiquetas_buscar_str = self.etiquetas_buscar_entry.get()
            
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y/%m/%d') if fecha_inicio_str else self.listado.getOldest().fecha
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y/%m/%d') if fecha_fin_str else datetime.now()
            etiquetas_buscar = [etq.strip() for etq in etiquetas_buscar_str.split(',')] if etiquetas_buscar_str else []

            listado_filtrado = self.listado.dateFilter(fecha_inicio, fecha_fin)
            
            if etiquetas_buscar:
                listado_filtrado.items = [item for item in listado_filtrado.items if any(etq in etiquetas_buscar for etq in item.etiquetas)]

            if listado_filtrado.items:
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for item in listado_filtrado.items:
                    self.tree.insert('', tk.END, values=(item.fecha, item.monto, ', '.join(item.etiquetas), item.descripcion))

        except Exception as e:
            messagebox.showerror('Error', f'Error al filtrar los datos: {e}')

    def add_item(self):
        try:
            fecha = datetime.strptime(self.fecha_entry.get(), '%Y/%m/%d %H:%M:%S')
            monto = float(self.monto_entry.get())
            etiquetas = [etq.strip() for etq in self.etiquetas_entry.get().split(',')]
            descripcion = self.descripcion_entry.get()

            nuevo_item = Item(fecha, monto, etiquetas, descripcion)
            self.listado.addItems(nuevo_item)
            self.listado.saveItems('items.csv')

            self.update_treeview()
            self.clear_entries()
            messagebox.showinfo('Éxito', 'Item añadido correctamente')
        except Exception as e:
            messagebox.showerror('Error', f'Error al añadir el item: {e}')

    def clear_entries(self):
        self.fecha_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)
        self.etiquetas_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.fecha_inicio_entry.delete(0, tk.END)
        self.fecha_fin_entry.delete(0, tk.END)
        self.etiquetas_buscar_entry.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = GestionGastosApp(root)
    root.mainloop()
