from bd import *
from datetime import datetime

registro1 = Registro('items.csv')

# registro1.agregar_item(Item(datetime.now(), -30.54, ['Agua', 'Servicio Básico'], 'Pago del servicio de agua de dos meses.'))
# registro1.agregar_item(Item(datetime.now(), 450, ['Salario'], 'Pago del salario mínimo.'))

it1 = Item(datetime(2024, 6, 18), 60, ["Luz", "Servicio Básico"], "Pago de la luz")
it2 = Item(datetime(2023, 11, 29), 40, ["Agua", "Servicio Básico"], "Pago de la luz")
it3 = Item(datetime.now(), 40, ["Agua", "Servicio Básico"], "Pago de la luz")

p1 = Listado([it1, it2, it3])
p1.printItems()

print("\n\n")

p2 = Estadisticas.statsYear(p1)
p2.printItems()
