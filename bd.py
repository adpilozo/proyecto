import csv
from datetime import datetime

formato_fecha = '%Y/%m/%d %H:%M:%S'
delimitadores_csv = [',', '_']

class Item:
    def __init__ (self, fecha, monto, etiquetas, descripción):
        self.fecha = fecha
        self.monto = monto
        self.etiquetas = etiquetas
        self.descripción = descripción
    
    def to_string(self):
        return 'Item:' + '\n  Fecha: ' + datetime.strftime(self.fecha, formato_fecha) + '\n  Monto: ' + str(self.monto) + '\n  Etiquetas: ' + str(self.etiquetas) +  '\n  Descripción: ' + self.descripción # Amo a mi novia hermosa
    
    def mostrar(self):
        print(self.to_string())

class Registro:
    def __init__(self, ruta):
        self.ruta = ruta

    def csv_item(self, csv):
        fecha = datetime.strptime(csv[0], formato_fecha)
        monto = float(csv[1])
        etiquetas = csv[2].split(delimitadores_csv[1])
        descripción = csv[3]

        return Item(fecha, monto, etiquetas, descripción)

    def item_csv(self, item):
        fecha_string = item.fecha.strftime(formato_fecha)
        monto_string = str(item.monto)
        etiquetas_string = delimitadores_csv[1].join(item.etiquetas)

        return [fecha_string, monto_string, etiquetas_string, item.descripción]

    def leer_items(self):
        with open(self.ruta, encoding='utf-8') as archivo:
            items = []
            lector = csv.reader(archivo, delimiter = delimitadores_csv[0])

            for linea in lector:
                items.append(self.csv_item(linea))
            
            return items

    def sobrescribir_items(self, items):
        items_csv = []
        if len(items) > 0:
            for item in items:
                items_csv.append(self.item_csv(item))
        
        with open(self.ruta, 'w', newline = '', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo, delimiter = delimitadores_csv[0])
            escritor.writerows(items_csv)
    
    def agregar_item(self, item):
        items = self.leer_items()
        items.append(item)
        self.sobrescribir_items(items)

    def eliminar_item(self, indice):
        items = self.leer_items()
        if indice < len(items):
            del items[indice]
        self.sobrescribir_items(items)
    
    def obtener_item(self, indice):
        return self.leer_items()[indice]
    
    def filtrar_fecha(self, fecha):
        items_filtrado = []

        for item in self.leer_items():
            if item.fecha.date == fecha.date:
                items_filtrado.append(item)
        
        return items_filtrado
    
    def filtrar_mes(self, mes, año):
        items_filtrado = []

        for item in self.leer_items():
            if item.fecha.month == mes and item.fecha.year == año:
                items_filtrado.append(item)
        
        return items_filtrado

    def monto_total(self):
        total = 0

        for item in self.leer_items():
            total += item.monto
        
        return round(total, 2)
