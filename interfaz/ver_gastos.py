import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import csv

class VerGastosPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Tabla de gastos
        self.tree = ttk.Treeview(self, columns=("monto", "fecha", "descripcion", "etiquetas"), show="headings")
        self.tree.heading("monto", text="Monto")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("etiquetas", text="Etiquetas")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Campos de filtrado
        self.filter_frame = ttk.Frame(self)
        self.filter_frame.pack(fill=tk.X, pady=10)

        self.filter_label = ttk.Label(self.filter_frame, text="Filtrar por Fecha:")
        self.filter_label.grid(column=0, row=0, padx=10, pady=5)
        self.filter_date = DateEntry(self.filter_frame, date_pattern='dd/mm/yyyy')
        self.filter_date.grid(column=1, row=0, padx=10, pady=5)
        self.filter_date_button = ttk.Button(self.filter_frame, text="Filtrar", command=self.filter_by_date)
        self.filter_date_button.grid(column=2, row=0, padx=10, pady=5)

        self.filter_label2 = ttk.Label(self.filter_frame, text="Filtrar por Etiquetas:")
        self.filter_label2.grid(column=0, row=1, padx=10, pady=5)
        self.filter_tags_entry = ttk.Entry(self.filter_frame)
        self.filter_tags_entry.grid(column=1, row=1, padx=10, pady=5)
        self.filter_tags_button = ttk.Button(self.filter_frame, text="Filtrar", command=self.filter_by_tags)
        self.filter_tags_button.grid(column=2, row=1, padx=10, pady=5)

        # Cargar datos
        self.load_data()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        try:
            with open('gastos.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            tk.messagebox.showwarning("Advertencia", "No se encontró el archivo 'gastos.csv'.")

    def filter_by_date(self):
        filter_date = self.filter_date.get()
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            with open('gastos.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == filter_date:
                        self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            tk.messagebox.showwarning("Advertencia", "No se encontró el archivo 'gastos.csv'.")

    def filter_by_tags(self):
        filter_tags = self.filter_tags_entry.get().lower()
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            with open('gastos.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    tags = row[3].lower()
                    if filter_tags in tags:
                        self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            tk.messagebox.showwarning("Advertencia", "No se encontró el archivo 'gastos.csv'.")
