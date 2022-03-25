# pylint: disable=line-too-long

"""Modulos a utilizar"""
from tkinter import Tk
import view


class Aplicacion:
    """Controlador de la aplicacion, trabaja sobre la interfaz de la misma"""

    def __init__(self, root):
        """Constructor de la clase. Definiciones para utilizar la vista de la aplicacion (view.py)"""
        self.root_controler = root
        self.obj_vista = view.VentanaAplicacion(self.root_controler)


if __name__ == "__main__":
    root_tk = Tk()
    app = Aplicacion(root_tk)
    root_tk.mainloop()
