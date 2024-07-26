import csv
from datetime import datetime

formato_fecha = '%Y/%m/%d %H:%M:%S'
delimitadores_csv = [',', '_']

class Item:
    def __init__ (self, fecha = datetime(1, 1, 1), monto = 0.0, etiquetas = [], descripcion = ""):
        self.fecha = fecha
        self.monto = monto
        self.etiquetas = etiquetas
        self.descripcion = descripcion

    def to_string(self):
        return 'Item:' + '\n  Fecha: ' + datetime.strftime(self.fecha, formato_fecha) + '\n  Monto: ' + str(self.monto) + '\n  Etiquetas: ' + str(self.etiquetas) +  '\n  descripcion: ' + self.descripcion

    def mostrar(self):
        print(self.to_string())

    def __eq__(self, item) -> bool:
        if isinstance(item, Item):
            return self.descripcion == item.descripcion and self.fecha == item.fecha and self.etiquetas == item.etiquetas and self.monto == item.monto
        return False

    def __str__(self) -> str:
        return f"Fecha: {self.fecha}, Monto: {self.monto}, Etiquetas: {self.etiquetas}, Descripción: {self.descripcion}"

    def toSeparateString(self, fecha:bool = True, monto:bool = True, etiquetas:bool = True, desc:bool = True, lastSpace:bool = False, lastCharF:str = "\n", lastCharM:str = "\n", lastCharE:str = "\n", lastCharD:str = "\n") -> str:
        s = ""
        if fecha:
            s += f"Fecha: {self.fecha}" + lastCharF
        if monto:
            s += f"Monto: {self.monto}" + lastCharM
        if etiquetas:
            s += f"Etiquetas: {self.etiquetas}" + lastCharE
        if desc:
            s += f"Descripción: {self.descripcion}" + lastCharD
        if lastSpace:
            s += "\n"

        return s

class Registro:
    def __init__(self, ruta:str):
        self.ruta = ruta

    def csv_item(self, csv):
        fecha = datetime.strptime(csv[0], formato_fecha)
        monto = float(csv[1])
        etiquetas = csv[2].split(delimitadores_csv[1])
        descripcion = csv[3]

        return Item(fecha, monto, etiquetas, descripcion)

    def item_csv(self, item):
        fecha_string = item.fecha.strftime(formato_fecha)
        monto_string = str(item.monto)
        etiquetas_string = delimitadores_csv[1].join(item.etiquetas)

        return [fecha_string, monto_string, etiquetas_string, item.descripcion]

    def leer_items(self) -> list[Item]:
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

    def leerEtiquetas(self):
        with open(self.ruta, encoding='utf-8') as archivo:
            etiquetas = {}
            lector = csv.reader(archivo, delimiter = delimitadores_csv[0])

            for linea in lector:
                etiquetas[linea[0]] = int(linea[1])

        return etiquetas

    def sobreescribirEtiquetas(self, etiquetas: dict):
        etq_csv = [(clave, valor) for clave, valor in etiquetas.items()]
        
        with open(self.ruta, 'w', newline = '', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo, delimiter = delimitadores_csv[0])
            escritor.writerows(etq_csv)
