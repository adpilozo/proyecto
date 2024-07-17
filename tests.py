from bd import Registro, Item
from datetime import datetime

registro1 = Registro('items.csv')

registro1.agregar_item(Item(datetime.now(), -30.54, ['Agua', 'Servicio Básico'], 'Pago del servicio de agua de dos meses.'))
registro1.agregar_item(Item(datetime.now(), 450, ['Salario'], 'Pago del salario mínimo.'))