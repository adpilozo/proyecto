from src.proyectoP2.bd import Registro

r = Registro("./src/utils/databases/etiquetas.csv")
r1 = Registro("./src/utils/databases/items.csv")

etiquetas = r.leerEtiquetas()
gastos = r1.leer_items()

A = sorted(gastos, key=lambda x: (etiquetas[x.etiquetas[0]], ord(x.etiquetas[0][0])))

print(A)