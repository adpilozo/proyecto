import os
from datetime import datetime
from .bd import Item, Registro

class Listado:
    def __init__(self, items:list[Item] = []):
        self.items = items

    def setItems(self, csvFile: str) -> None:
        if os.path.isfile(csvFile):
            reg1 = Registro(csvFile)
            self.items = reg1.leer_items()
        else:
            with open(csvFile, "w"):
                pass

    def addItems(self, item: Item) -> None:
        self.items.append(item)

    def removeItems(self, item: Item) -> None:
        for i in self.items:
            if i == item:
                self.items.remove(i)

    def printItems(self) -> None:
        for item in self.items:
            print(item)

        print("\n")

    def dateFilter(self, fechaInicio: datetime, fechaFin: datetime = datetime.now()):
        listaFiltrada = Listado([])

        for i in self.items:
            if i.fecha.date() >= fechaInicio.date() and i.fecha.date() <= fechaFin.date():
                listaFiltrada.addItems(i)

        return listaFiltrada

    def getLatest(self) -> Item:
        itAux = Item()

        for item in self.items:
            if item.fecha > itAux.fecha:
                itAux = item

        return itAux

    def getOldest(self) -> Item:
        itAux = self.items[0]

        for item in self.items:
            if item.fecha < itAux.fecha:
                itAux = item

        return itAux

    def getDescripciones(self) -> list[str]:
        return [item.descripcion for item in self.items]

    def getGastos(self) -> list[int]:
        return [item.monto for item in self.items]

    def getFechas(self) -> list[datetime]:
        return [item.fecha for item in self.items]

    def getEtiquetas(self) -> dict:
        etqAll = {}

        for item in self.items:
            for etqStr in item.etiquetas:
                if etqStr in etqAll.keys():
                    etqAll[etqStr] += 1
                else:
                    etqAll[etqStr] = 1

        return etqAll

    def __str__(self) -> str:
        return "\n".join(str(item) for item in self.items)

    def saveItems(self, ruta:str = "items.csv") -> None:
        r1 = Registro(ruta)
        r1.sobrescribir_items(self.items)
