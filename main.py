import tkinter as tk
from tkinter import Tk

from src.proyectoP2.interfaz import GestionGastosApp

if __name__ == '__main__':
    root = tk.Tk()
    app = GestionGastosApp(root)
    root.mainloop()