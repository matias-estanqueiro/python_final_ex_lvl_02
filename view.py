# pylint: disable=line-too-long

"""Modulos a utilizar"""
from tkinter import Label, Entry, Frame, Button, StringVar, END
from tkinter.ttk import Treeview
import tkcalendar as tk_calendar
from model import BaseDeDatos, ValidarDatos, MostrarAlertas


class VentanaAplicacion:
    """Clase ventana principal de la aplicación"""

    def __init__(self, window):
        """Configuracion inicial de la ventana principal"""

        # ----- Declaraciones ----- #
        self.base_datos = BaseDeDatos()
        self.validar_campos = ValidarDatos()
        self.alertas = MostrarAlertas()
        self.var_dni = StringVar()
        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_empresa = StringVar()
        self.var_telefono = StringVar()
        self.var_email = StringVar()
        self.var_direccion = StringVar()
        self.var_nacimiento = StringVar()
        # ----- (?) Pylint recomienda definir las variables en el constructor antes de utilizarlas
        self.item_seleccionado = None
        self.valores = None

        self.root = window
        self.root.title("TP FINAL - DIPLOMATURA INTERMEDIO (v2.0) - DATOS DE PERSONAL")

        self.root.resizable(False, False)

        # ----- Divido la ventana principal en 4 frames ----- #
        self.fra_encabezado = Frame(self.root)
        self.fra_encabezado.grid(row=0, column=0)
        self.fra_principal = Frame(self.root)
        self.fra_principal.grid(row=1, column=0)
        self.fra_botonera = Frame(self.root)
        self.fra_botonera.grid(row=2, column=0)
        self.fra_vista = Frame(self.root)
        self.fra_vista.grid(row=3, column=0)

        # ----- Frame -> Encabezado ----- #
        self.lbl_titulo = Label(
            self.fra_encabezado, text="---------- PERSONAL ----------"
        )
        self.lbl_titulo.grid(row=0, column=0, pady=10)

        # ----- Frame -> Principal ----- #
        self.lbl_dni = Label(self.fra_principal, text="DNI:")
        self.lbl_dni.grid(row=0, column=0, padx=5, pady=10)
        self.ent_dni = Entry(self.fra_principal, textvariable=self.var_dni, width=40)
        self.ent_dni.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_nombre = Label(self.fra_principal, text="Nombre:")
        self.lbl_nombre.grid(row=1, column=0, padx=5, pady=10)
        self.ent_nombre = Entry(
            self.fra_principal, textvariable=self.var_nombre, width=40
        )
        self.ent_nombre.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_apellido = Label(self.fra_principal, text="Apellido:")
        self.lbl_apellido.grid(row=2, column=0, padx=5, pady=10)
        self.ent_apellido = Entry(
            self.fra_principal, textvariable=self.var_apellido, width=40
        )
        self.ent_apellido.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_empresa = Label(self.fra_principal, text="Empresa:")
        self.lbl_empresa.grid(row=3, column=0, padx=5, pady=10)
        self.ent_empresa = Entry(
            self.fra_principal, textvariable=self.var_empresa, width=40
        )
        self.ent_empresa.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_telefono = Label(self.fra_principal, text="Telefono:")
        self.lbl_telefono.grid(row=4, column=0, padx=5, pady=10)
        self.ent_telefono = Entry(
            self.fra_principal, textvariable=self.var_telefono, width=40
        )
        self.ent_telefono.grid(row=4, column=1, padx=10, pady=10)

        self.lbl_email = Label(self.fra_principal, text="E-mail:")
        self.lbl_email.grid(row=5, column=0, padx=5, pady=10)
        self.ent_email = Entry(
            self.fra_principal, textvariable=self.var_email, width=40
        )
        self.ent_email.grid(row=5, column=1, padx=10, pady=10)

        self.lbl_direccion = Label(self.fra_principal, text="Direccion:")
        self.lbl_direccion.grid(row=6, column=0, padx=5, pady=10)
        self.ent_direccion = Entry(
            self.fra_principal, textvariable=self.var_direccion, width=40
        )
        self.ent_direccion.grid(row=6, column=1, padx=10, pady=10)

        self.lbl_nacimiento = Label(self.fra_principal, text="F. Nacimiento:")
        self.lbl_nacimiento.grid(row=7, column=0, padx=5, pady=10)
        self.ent_nacimiento = Entry(
            self.fra_principal, textvariable=self.var_nacimiento, width=40
        )
        self.ent_nacimiento.grid(row=7, column=1, padx=10, pady=10)

        self.calendario = tk_calendar.Calendar(
            self.fra_principal, selectmode="day", year=2022, month=2
        )
        self.calendario.grid(row=0, column=3, rowspan=4)

        self.lbl_info = Label(
            self.fra_principal,
            text="DNI / TELEFONO: solo numeros sin \nseparadores ni espacios\nEMAIL: formato email@email.com\nFECHA: formato dd/mm/aaaa",
        )
        self.lbl_info.grid(row=4, column=3, rowspan=4)

        # ----- Frame -> Botonera ----- #
        self.btn_agregar = Button(
            self.fra_botonera,
            text="Agregar",
            command=lambda: [
                self.base_datos.insertar_registro(
                    self.var_dni.get(),
                    self.var_nombre.get(),
                    self.var_apellido.get(),
                    self.var_empresa.get(),
                    self.var_telefono.get(),
                    self.var_email.get(),
                    self.var_direccion.get(),
                    self.var_nacimiento.get(),
                ),
                self.vaciar_entry(),
            ],
        )
        self.btn_agregar.grid(row=0, column=0, padx=20, pady=10)

        self.btn_borrar = Button(
            self.fra_botonera,
            text="Borrar",
            command=lambda: [
                self.base_datos.borrar_registro(self.var_dni.get()),
                self.vaciar_entry(),
            ],
        )
        self.btn_borrar.grid(row=0, column=1, padx=20, pady=10)

        self.btn_modificar = Button(
            self.fra_botonera,
            text="Modificar",
            command=lambda: [
                self.base_datos.actualizar_registro(
                    self.var_nombre.get(),
                    self.var_apellido.get(),
                    self.var_empresa.get(),
                    self.var_telefono.get(),
                    self.var_email.get(),
                    self.var_direccion.get(),
                    self.var_nacimiento.get(),
                    self.var_dni.get(),
                ),
                self.vaciar_entry(),
            ],
        )
        self.btn_modificar.grid(row=0, column=2, padx=20, pady=10)

        self.btn_buscar = Button(
            self.fra_botonera,
            text="Buscar",
            command=lambda: self.mostrar_busqueda(self.var_dni.get()),
        )
        self.btn_buscar.grid(row=0, column=3, padx=20, pady=10)

        self.btn_vaciar_campos = Button(
            self.fra_botonera,
            text="Vaciar Campos",
            command=lambda: [self.vaciar_entry()],
        )
        self.btn_vaciar_campos.grid(row=0, column=4, padx=20, pady=10)

        # ----- Frame -> Vista ----- #
        self.tv_tabla = Treeview(
            self.fra_vista,
            columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8"),
            height=5,
        )
        self.tv_tabla["show"] = "headings"
        self.tv_tabla.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
        self.tv_tabla.heading("#1", text="DNI")
        self.tv_tabla.column("#1", width=100)
        self.tv_tabla.heading("#2", text="Nombre")
        self.tv_tabla.column("#2", width=100)
        self.tv_tabla.heading("#3", text="Apellido")
        self.tv_tabla.column("#3", width=100)
        self.tv_tabla.heading("#4", text="Empresa")
        self.tv_tabla.column("#4", width=100)
        self.tv_tabla.heading("#5", text="Telefono")
        self.tv_tabla.column("#5", width=100)
        self.tv_tabla.heading("#6", text="E-mail")
        self.tv_tabla.column("#6", width=100)
        self.tv_tabla.heading("#7", text="Direccion")
        self.tv_tabla.column("#7", width=100)
        self.tv_tabla.heading("#8", text="Nacimiento")
        self.tv_tabla.column("#8", width=100)
        self.tv_tabla.bind("<ButtonRelease-1>", self.seleccionar_elemento)

    def mostrar_busqueda(self, dni):
        "Permite traer los resultados de la busqueda y mostrarlos en los entry, invocando a la funcion insertar_elementos()"
        self.resultado_busqueda = self.base_datos.buscar_registro(dni)
        self.vaciar_entry()
        try:
            for fila in self.resultado_busqueda:
                self.tv_tabla.insert(
                    "",
                    "end",
                    text="",
                    values=(
                        fila[0],
                        fila[1],
                        fila[2],
                        fila[3],
                        fila[4],
                        fila[5],
                        fila[6],
                        fila[7],
                    ),
                )
            self.var_dni.set(self.resultado_busqueda[0][0])
            self.var_nombre.set(self.resultado_busqueda[0][1])
            self.var_apellido.set(self.resultado_busqueda[0][2])
            self.var_empresa.set(self.resultado_busqueda[0][3])
            self.var_telefono.set(self.resultado_busqueda[0][4])
            self.var_email.set(self.resultado_busqueda[0][5])
            self.var_direccion.set(self.resultado_busqueda[0][6])
            self.var_nacimiento.set(self.resultado_busqueda[0][7])
        except IndexError:
            self.alertas.mensaje_error(
                "El DNI ingresado no se encuentra almacenado en la base de datos"
            )

    def vaciar_entry(self):
        """Deja todos los entry de la vista vacios para poder utilizarlos nuevamente"""
        self.ent_dni.delete(0, END)
        self.ent_nombre.delete(0, END)
        self.ent_apellido.delete(0, END)
        self.ent_empresa.delete(0, END)
        self.ent_telefono.delete(0, END)
        self.ent_email.delete(0, END)
        self.ent_direccion.delete(0, END)
        self.ent_nacimiento.delete(0, END)

    def seleccionar_elemento(self, evento):
        """Selecciona el elemento del TreeView y los coloca en los entry de la vista (previo a borrar los valores de los entry en caso de que no esten vacios)"""
        self.item_seleccionado = self.tv_tabla.focus()
        self.valores = self.tv_tabla.item(self.item_seleccionado, "values")
        self.vaciar_entry()
        self.var_dni.set(self.valores[0])
        self.var_nombre.set(self.valores[1])
        self.var_apellido.set(self.valores[2])
        self.var_empresa.set(self.valores[3])
        self.var_telefono.set(self.valores[4])
        self.var_email.set(self.valores[5])
        self.var_direccion.set(self.valores[6])
        self.var_nacimiento.set(self.valores[7])
