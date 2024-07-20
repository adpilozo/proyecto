import copy
from Listado import *
from bd import Item
from datetime import datetime
from sympy import Symbol # Librería a instalar (pip install sympy)

class Estadisticas:
    def statsMonth(list1: Listado, mes:int = datetime.now().month, año:int = datetime.now().year) -> Listado:
        mesAux = mes + 1
        añoAux = año
        if mes == 12:
            mesAux = 1
            añoAux += 1

        return list1.dateFilter(datetime(año, mes, 1), datetime(añoAux, mesAux, 1))

    def statsYear(list1: Listado, año:int = datetime.now().year) -> Listado:
        return list1.dateFilter(datetime(año, 1, 1), datetime(año + 1, 1, 1))
    
    def pointsToFunction(listX: list[int], listF: list[int]):
        n = len(listX)
        x = Symbol("x")
        f = 0

        for i in range(0, n):
            aux = 1
            for j in range(0, n):
                if i != j:
                    aux *= (x - listX[j]) / (listX[i] - listX[j])

            f += aux * listF[i]

        return f

    def getFunction(list1: Listado):
        nList = len(list1.items)
        if nList < 1:
            return 0
        
        fechaToEval = list1.getOldest().fecha
        toSec = lambda fecha1: fecha1.days * 86400 + fecha1.seconds
        lambF = lambda item: round(toSec(item.fecha - fechaToEval) / 86400, 5)
        listX = [lambF(it) for it in list1.items]
        listF = list1.getGastos()

        return Estadisticas.pointsToFunction(listX, listF) # Función estimada para los datos ingresados

    def predictNextMonth(list1: Listado) -> Item:
        maxTimeItem = list1.getLatest().fecha
        if maxTimeItem.month == 12:
            dateAux = datetime(maxTimeItem.year + 1, 1, 1)
        else:
            dateAux = datetime(maxTimeItem.year, maxTimeItem.month + 1, 1)

        f = Estadisticas.getFunction(list1)
        x = Symbol("x")

        monto = f.evalf(subs={x: (list1.getOldest().fecha - dateAux).seconds / 3600})

        return Item(dateAux, monto, list(list1.getEtiquetas().keys()), f"Predicción Mes: {dateAux.month}, Año: {dateAux.year}")

    def predictNextYear(list1: Listado) -> Listado:
        listReturn = Listado()
        listAux = copy.deepcopy(list1)

        for i in range(0, 12):
            itemAux = Estadisticas.predictNextMonth(listAux)

            listAux.addItems(itemAux)
            listReturn.addItems(itemAux)

        return listReturn
