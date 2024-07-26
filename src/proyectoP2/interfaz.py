import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .bd import Registro, Item
from .Listado import Listado
from .Estadisticas import Estadisticas

class GestionGastosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Gastos Personales")
        
        self.rutaItems = './src/utils/databases/items.csv'
        self.registroItems = Registro(self.rutaItems)
        self.listadoItems = Listado(self.registroItems.leer_items())
        self.rutaEtiquetas = "./src/utils/databases/etiquetas.csv"
        self.registroEtiquetas = Registro(self.rutaEtiquetas)
        self.etiquetasDict = self.registroEtiquetas.leerEtiquetas()

        self.create_menu()
        self.create_frames()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.gastos_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Menú", menu=self.gastos_menu)
        self.gastos_menu.add_command(label="Añadir Gastos", command=self.show_add_gastos)
        self.gastos_menu.add_command(label="Añadir Etiquetas", command=self.showAddEtiquetas)
        self.gastos_menu.add_command(label="Ver Gastos", command=self.show_view_gastos)
        self.gastos_menu.add_command(label="Estadísticas", command=self.show_estadisticas)

    def create_frames(self):
        self.frame = tk.Canvas(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.add_gastos_frame = self.create_add_gastos_frame()
        self.addEtiquetasFrame = self.createAddEtiquetasFrame()
        self.view_gastos_frame = self.create_view_gastos_frame()
        self.estadisticas_frame = self.create_estadisticas_frame()

        self.show_view_gastos()

    def create_add_gastos_frame(self):
        frame = tk.Frame(self.frame)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text='Fecha (YYYY/MM/DD HH:MM:SS)').grid(row=0, column=0, padx=5, pady=5)
        self.fecha_entry = ttk.Entry(frame)
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=5)
        # Insertar la fecha actual en el campo de entrada de la fecha
        self.fecha_entry.insert(0, datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

        ttk.Label(frame, text='Monto').grid(row=1, column=0, padx=5, pady=5)
        self.monto_entry = ttk.Entry(frame)
        self.monto_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text='Etiquetas').grid(row=2, column=0, padx=5, pady=5)
        self.etiquetas_entry = ttk.Combobox(frame, state="readonly")
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
        self.fecha_fin_entry.insert(0, datetime.now().strftime('%Y/%m/%d'))  # Fecha actual

        ttk.Label(filter_frame, text='Etiquetas (separadas por comas)').grid(row=2, column=0, padx=5, pady=5)
        self.etiquetas_buscar_entry = ttk.Entry(filter_frame)
        self.etiquetas_buscar_entry.grid(row=2, column=1, padx=5, pady=5)

        self.filter_button = ttk.Button(filter_frame, text='Filtrar', command=self.update_treeview)
        self.filter_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.show_all_button = ttk.Button(filter_frame, text='Todos los Gastos', command=self.show_all_gastos)
        self.show_all_button.grid(row=3, column=1, columnspan=2, padx=5, pady=10)

        self.delete_item = ttk.Button(filter_frame, text='Borrar Item', command=self.delete_gasto)
        self.delete_item.grid(row=3, column=3, columnspan=2, padx=5, pady=10)

        # Treeview
        self.treeGastos = ttk.Treeview(frame, columns=('Fecha', 'Monto', 'Etiquetas', 'Descripción'), show='headings')
        self.treeGastos.heading('Fecha', text='Fecha')
        self.treeGastos.heading('Monto', text='Monto')
        self.treeGastos.heading('Etiquetas', text='Etiquetas')
        self.treeGastos.heading('Descripción', text='Descripción')
        self.treeGastos.pack(fill=tk.BOTH, expand=True)

        return frame

    def create_estadisticas_frame(self, statsYear = 0, statsMonth = 0):
        frame = tk.Canvas(self.frame)
        frame.pack(fill=tk.BOTH, expand=True)

        # ttk.Label(frame, text='Fecha (YYYY/MM/DD HH:MM:SS)').grid(row=0, column=0, padx=5, pady=5)
        titulo = ttk.Label(frame, text="Predicción de Gastos", font=("Arial", 15, "bold"))
        titulo.grid(row=0, column=1, columnspan=2, pady=20)

        if statsYear == 0:
            statsYear = Estadisticas.predictNextYear(self.listadoItems)
        if statsMonth == 0:
            statsMonth = Estadisticas.predictNextMonth(self.listadoItems)

        # Sección Predicción Mes Siguiente
        ttk.Label(frame, text=f"Predicción Mes {statsMonth.fecha.month}, Año {statsMonth.fecha.year}", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(frame, text=statsMonth.toSeparateString(etiquetas=False, desc=False)).grid(row = 2, column=0, padx=5, pady=5)

        # Línea divisoria
        linDiv = ttk.Separator(frame, orient="vertical")
        linDiv.grid(row=1, column=1, columnspan=5)

        # Sección Predicción Año Siguiente
        itemStatsYear = statsYear.getOldest().fecha
        ttk.Label(frame, text=f"Predicción Año {itemStatsYear.year - 1}/{itemStatsYear.month} - {itemStatsYear.year}/{itemStatsYear.month}", font=("Arial", 10, "bold")).grid(row= 1, column=1, padx=5, pady=5)

        self.showGraphEstadisticasButton = ttk.Button(frame, text="Gráfico de la Función", command=self.showGraphEstadisticas)
        self.showGraphEstadisticasButton.grid(row=1, column=3, padx=5, pady=5)

        rowCounter = 2
        for item in statsYear.items:
            s = item.toSeparateString(etiquetas=False, desc=False, lastCharF=" --- ")
            ttk.Label(frame, text=s).grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

        return frame
    
    def createAddEtiquetasFrame(self):
        frame = tk.Frame(self.frame)
        frame.pack(fill=tk.BOTH, expand=True)

        frameEtiquetaOptions = tk.Frame(frame)
        frameEtiquetaOptions.pack(fill=tk.X, pady=10)

        titulo = ttk.Label(frameEtiquetaOptions, text="Agregar Etiquetas", font=("Arial", 15, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(frameEtiquetaOptions, text="Nombre").grid(row=1, column=0, padx=5, pady=5)
        self.etiquetaNameEntry = ttk.Entry(frameEtiquetaOptions)
        self.etiquetaNameEntry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frameEtiquetaOptions, text="Peso").grid(row=2, column=0, padx=5, pady=5)
        self.etiquetaPesoEntry = ttk.Entry(frameEtiquetaOptions)
        self.etiquetaPesoEntry.grid(row=2, column=1, padx=5, pady=5)
        self.etiquetaPesoEntry.insert(0, "0")

        self.addEtiquetaButton = ttk.Button(frameEtiquetaOptions, text="Añadir Etiqueta", command=self.updateTreeEtiquetas)
        self.addEtiquetaButton.grid(row=2, column=2, padx=5, pady=5)

        self.deleteEtiquetaButton = ttk.Button(frameEtiquetaOptions, text="Eliminar Etiqueta", command=self.deleteEtiqueta)
        self.deleteEtiquetaButton.grid(row=2, column=3, padx=5, pady=5)

        self.treeEtiquetas = ttk.Treeview(frame, columns=("Etiqueta", "Peso"))
        self.treeEtiquetas.heading("Etiqueta", text="Etiqueta")
        self.treeEtiquetas.heading("Peso", text="Peso")
        self.treeEtiquetas.pack(fill=tk.BOTH, expand=True)

        return frame

    def showAddEtiquetas(self):
        self.clear_frames()
        self.addEtiquetasFrame.pack(fill=tk.BOTH, expand=True)
        self.display_items_in_treeview_Etiquetas()

    def show_estadisticas_data(self):
        self.clear_frames()
        self.estadisticas_frame.pack(fill=tk.BOTH, expand=True)

    def show_add_gastos(self):
        self.clear_frames()
        self.add_gastos_frame.pack(fill=tk.BOTH, expand=True)
        self.updateEtiquetasAddGasto()

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
        self.addEtiquetasFrame.pack_forget()

    def updateEtiquetasAddGasto(self):
        self.etiquetas_entry["values"] = list(self.etiquetasDict.keys())

    def update_treeview(self):
        try:
            fecha_inicio_str = self.fecha_inicio_entry.get()
            fecha_fin_str = self.fecha_fin_entry.get()
            etiquetas_buscar_str = self.etiquetas_buscar_entry.get()
            
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y/%m/%d') if fecha_inicio_str else self.listadoItems.getOldest().fecha
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y/%m/%d') if fecha_fin_str else datetime.now()
            etiquetas_buscar = [etq.strip() for etq in etiquetas_buscar_str.split(',')] if etiquetas_buscar_str else []

            listado_filtrado = self.listadoItems.dateFilter(fecha_inicio, fecha_fin)

            if etiquetas_buscar:
                listado_filtrado.items = [item for item in listado_filtrado.items if any(etq in etiquetas_buscar for etq in item.etiquetas)]

            listado_filtrado.items = sorted(listado_filtrado.items, key=lambda x: (self.etiquetasDict[x.etiquetas[0]], ord(x.etiquetas[0][0])))
            self.display_items_in_treeview(listado_filtrado.items)

        except Exception as e:
            messagebox.showerror('Error', f'Error al filtrar los datos: {e}')

    def updateTreeEtiquetas(self):
        try:
            nombreEtiqueta = self.etiquetaNameEntry.get()
            pesoEtiqueta = self.etiquetaPesoEntry.get()

            self.etiquetasDict[nombreEtiqueta] = int(pesoEtiqueta)
            self.registroEtiquetas.sobreescribirEtiquetas(self.etiquetasDict)
            self.clearEtiquetasFields()

            self.display_items_in_treeview_Etiquetas()
            messagebox.showinfo("Éxito", "La etiqueta y su peso se han añadido correctamente")
        except Exception:
            messagebox.showerror("Error", "Error con los valores ingresados, intente nuevamente")

    def delete_gasto(self):
        try:
            selected_item = self.treeGastos.focus()

            itemArray = self.treeGastos.item(selected_item)['values']
            itemGasto = Item(datetime.strptime(itemArray[0], '%Y-%m-%d %H:%M:%S'), float(itemArray[1]), [i for i in itemArray[2].split(", ")], itemArray[3])

            self.listadoItems.removeItems(itemGasto)
            self.registroItems.sobrescribir_items(self.listadoItems.items)

            self.display_items_in_treeview(self.listadoItems.items)
        except Exception:
            messagebox.showerror("Error", "No se ha seleccionado ningún gasto")

    def deleteEtiqueta(self):
        try:
            selectedEtiqueta = self.treeEtiquetas.focus()

            etiqueta = self.treeEtiquetas.item(selectedEtiqueta)['values']
            
            self.etiquetasDict.pop(etiqueta[0])
            self.registroEtiquetas.sobreescribirEtiquetas(self.etiquetasDict)

            self.display_items_in_treeview_Etiquetas()
        except Exception as e:
            messagebox.showerror("Error", f"No se ha seleccionado ninguna etiqueta: {e}")

    def show_all_gastos(self):
        try:
            self.display_items_in_treeview(self.listadoItems.items)
        except Exception as e:
            messagebox.showerror('Error', f'Error al mostrar todos los gastos: {e}')

    def display_items_in_treeview(self, items):
        for item in self.treeGastos.get_children():
            self.treeGastos.delete(item)

        for item in items:
            self.treeGastos.insert('', tk.END, values=(item.fecha, item.monto, ', '.join(item.etiquetas), item.descripcion))

    def display_items_in_treeview_Etiquetas(self):
        for item in self.treeEtiquetas.get_children():
            self.treeEtiquetas.delete(item)

        self.etiquetasDict = {item: value for item, value in sorted(self.etiquetasDict.items(), key=lambda item: item[1])}

        for item in self.etiquetasDict.items():
            self.treeEtiquetas.insert('', tk.END, values=(item[0], item[1]))

    def showGraphEstadisticas(self):
        f = Estadisticas.getFunction(self.listadoItems)
        if f != 0:
            plot = Estadisticas.functionGraph(f)

        plot.show()

    def add_item(self):
        try:
            fecha = datetime.strptime(self.fecha_entry.get(), '%Y/%m/%d %H:%M:%S')
            monto = float(self.monto_entry.get())
            etiquetas = [etq.strip() for etq in self.etiquetas_entry.get().split(',')]
            descripcion = self.descripcion_entry.get()

            item = Item(fecha, monto, etiquetas, descripcion)
            self.listadoItems.addItems(item)
            self.registroItems.agregar_item(item)
            self.clear_add_item_fields()
            messagebox.showinfo('Éxito', 'El gasto se ha añadido correctamente')

        except Exception as e:
            messagebox.showerror('Error', f'Error al añadir el gasto: {e}')

    def clear_add_item_fields(self):
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        self.monto_entry.delete(0, tk.END)
        self.etiquetas_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)

    def clearEtiquetasFields(self):
        self.etiquetaNameEntry.delete(0, tk.END)
        self.etiquetaPesoEntry.delete(0, tk.END)
        self.etiquetaPesoEntry.insert(0, "0")
