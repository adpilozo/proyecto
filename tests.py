from bd import *
from Estadisticas import *
from datetime import datetime

registro1 = Registro('items.csv')

# registro1.agregar_item(Item(datetime.now(), -30.54, ['Agua', 'Servicio Básico'], 'Pago del servicio de agua de dos meses.'))
# registro1.agregar_item(Item(datetime.now(), 450, ['Salario'], 'Pago del salario mínimo.'))

it1 = Item(datetime(2024, 5, 18, 5, 32, 10), 60, ["Luz", "Servicio Básico"], "Pago de la luz")
it2 = Item(datetime(2024, 6, 19), 58, ["Agua", "Servicio Básico"], "Pago de la luz")
it3 = Item(datetime(2024, 7, 18), 50, ["Agua", "Servicio Básico"], "Pago de la luz")
# it4 = Item(datetime(2021, 7, 7), 40, ["Agua", "Servicio Básico"], "Pago de la luz")

p1 = Listado([it1, it2, it3])
p1.printItems()
print(Estadisticas.predictNextYear(p1).printItems())

p1.saveItems()
