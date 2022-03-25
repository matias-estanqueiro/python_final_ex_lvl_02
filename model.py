# pylint: disable=line-too-long

"""Modulos a utilizar"""
import sqlite3 as bd_sqlite
from sqlite3 import Error
from tkinter.messagebox import showerror, showinfo
import re


class MostrarAlertas:
    """Clase para mostrar los errores o la informacion al usuario mediante cuadros de dialogo durante la ejecucion de la aplicacion"""

    def mensaje_error(self, desc_error):
        """Muestra mensaje de error"""
        showerror("Error", desc_error)

    def mensaje_ok(self, desc_mensaje):
        """Muestra mensaje de informacion"""
        showinfo("Mensaje", desc_mensaje)


class ValidarDatos:
    """Metodos para realizar la validacion de los datos, en caso de que alguno no cumpla con el formato especificado, no se realizara la consulta"""

    def __init__(self):
        """Instancia la clase MostrarAlertas, la cual utiliza para enviar al usuario mensajes mediante cuadros de dialogo"""
        self.alertas = MostrarAlertas()

    def validar_dni(self, dni):
        """Validacion mediante expresiones regulares del campo DNI"""
        patron_dni = "^[0-9]{7,8}$"
        if not re.match(patron_dni, dni):
            self.alertas.mensaje_error("Por favor introduzca un formato de DNI valido")
            return False

    def validar_telefono(self, telefono):
        """Validacion mediante expresiones regulares del campo telefono"""
        patron_telefono = "^[0-9]{10,20}$"
        if not re.match(patron_telefono, telefono):
            self.alertas.mensaje_error(
                "Por favor introduzca un formato de telefono valido"
            )
            return False

    def validar_email(self, email):
        """Validacion mediante expresiones regulares del campo email"""
        patron_mail = "^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        if not re.match(patron_mail, email):
            self.alertas.mensaje_error(
                "Por favor introduzca un formato de email valido"
            )
            return False

    def validar_nacimiento(self, nacimiento):
        """Validacion mediante expresiones regulares del campo nacimiento (fecha)"""
        patron_nacimiento = "^^(((0[1-9]|[12][0-9]|30)[-/]?(0[13-9]|1[012])|31[-/]?(0[13578]|1[02])|(0[1-9]|1[0-9]|2[0-8])[-/]?02)[-/]?[0-9]{4}|29[-/]?02[-/]?([0-9]{2}(([2468][048]|[02468][48])|[13579][26])|([13579][26]|[02468][048]|0[0-9]|1[0-6])00))$"
        if not re.match(patron_nacimiento, nacimiento):
            self.alertas.mensaje_error(
                "Por favor introduzca un formato de fecha valido"
            )
            return False


class BaseDeDatos:
    """Operaciones de CRUD para el manejo de la base de datos SQLite3"""

    def __init__(self):
        """Constructor de la clase. La aplicación utiliza como motor de base de datos SQLite3"""
        # ----- Objetos. Instancias de las clases creadas
        self.alertas = MostrarAlertas()
        self.validar = ValidarDatos()
        # ----- (?) Pylint recomienda definir las variables en el constructor antes de utilizarlas
        self.resultado_consulta = None
        self.con = None
        self.instruccion = None
        self.sql = None
        self.datos = None
        self.comprueba_dni = None
        self.comprueba_telefono = None
        self.comprueba_email = None
        self.comprueba_nacimiento = None
        self.registro = None

        try:
            self.conexion = bd_sqlite.connect("personal_v2.db")
            self.cursor = self.conexion.cursor()
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS personal(dni text PRIMARY KEY, nombre text NOT NULL, apellido text NOT NULL, empresa text NOT NULL, telefono text NOT NULL, email text NOT NULL, direccion text NOT NULL, nacimiento text NOT NULL)"
            )
            self.conexion.commit()
            print("DB = personal_v2.db \nTABLA = personal")
        except Error:
            print(Error)

    def conexion_base_datos(self):
        """Conexión con la base de datos. Metodo reutilizable para realizar la conexion"""
        self.con = bd_sqlite.connect("personal_v2.db")
        return self.con

    def insertar_registro(
        self, dni, nombre, apellido, empresa, telefono, email, direccion, nacimiento
    ):
        """Inserta nuevos registros en la tabla personal en la base de datos personal_v2. Para que se puedan realizar el alta de datos, todos los campos deben estar completos (se realiza esta validacion) y correctos (se valida mediante regex)"""
        if (
            dni == ""
            or nombre == ""
            or apellido == ""
            or empresa == ""
            or telefono == ""
            or email == ""
            or direccion == ""
            or nacimiento == ""
        ):
            self.alertas.mensaje_ok(
                "Para poder ingresar la información en la base de datos, todos los campos deben estar completos"
            )
        else:
            self.comprueba_dni = self.validar.validar_dni(dni)
            self.comprueba_telefono = self.validar.validar_telefono(telefono)
            self.comprueba_email = self.validar.validar_email(email)
            self.comprueba_nacimiento = self.validar.validar_nacimiento(nacimiento)
            if (
                self.comprueba_dni is not False
                and self.comprueba_telefono is not False
                and self.comprueba_email is not False
                and self.comprueba_nacimiento is not False
            ):
                try:
                    self.datos = (
                        dni,
                        nombre,
                        apellido,
                        empresa,
                        telefono,
                        email,
                        direccion,
                        nacimiento,
                    )
                    self.conexion = self.conexion_base_datos()
                    self.instruccion = "INSERT INTO personal(dni, nombre, apellido, empresa, telefono, email, direccion, nacimiento) VALUES(?,?,?,?,?,?,?,?)"
                    self.cursor = self.conexion.cursor()
                    self.cursor.execute(self.instruccion, self.datos)
                    self.conexion.commit()
                    self.alertas.mensaje_ok("La información fue agregada con exito")
                except Error:
                    self.alertas.mensaje_error(
                        "ERROR: La operacion no pudo realizarse correctamente. POSIBLE MOTIVO: El dni Ingresado ya se encuentra registrado"
                    )

    def borrar_registro(self, dni):
        """Elimina registros de la tabla 'personal' en la base de datos 'personal_v2'. Previamente realiza una validacion para comprobar que el DNI ingresado se encuentre en la base de datos"""
        self.conexion = self.conexion_base_datos()
        self.registro = self.buscar_registro(dni)
        if self.registro == []:
            self.alertas.mensaje_error(
                "El DNI ingresado no se encuentra en la base de datos"
            )
        else:
            try:
                self.instruccion = "DELETE FROM personal WHERE dni=?"
                self.cursor = self.conexion.cursor()
                self.cursor.execute(self.instruccion, (dni,))
                self.conexion.commit()
                self.alertas.mensaje_ok("Los datos se borraron correctamente")
            except Error:
                self.alertas.mensaje_error(
                    "Error: La operacion no pudo realizarse correctamente"
                )

    def actualizar_registro(
        self, nombre, apellido, empresa, telefono, email, direccion, nacimiento, dni
    ):
        """Actualiza registros de la tabla 'personal' en la base de datos 'personal_v2'. Previamente valida que el campo DNI realmente se encuentre almacenado en la base de datos (en caso de no encontrarlo avisa al usuario mediante ua alerta)"""
        self.conexion = self.conexion_base_datos()
        self.registro = self.buscar_registro(dni)
        if self.registro == []:
            self.alertas.mensaje_error(
                "No se puede actualizar. El DNI ingresado no se encuentra en la base de datos"
            )
        else:
            try:
                self.datos = (
                    nombre,
                    apellido,
                    empresa,
                    telefono,
                    email,
                    direccion,
                    nacimiento,
                    dni,
                )
                self.instruccion = "UPDATE personal SET (nombre, apellido, empresa, telefono, email, direccion, nacimiento)=(?,?,?,?,?,?,?) WHERE dni=?"
                self.cursor = self.conexion.cursor()
                self.cursor.execute(self.instruccion, self.datos)
                self.conexion.commit()
                self.alertas.mensaje_ok("Los datos se actualizaron correctamente")
            except Error:
                self.alertas.mensaje_error(
                    "Error: La operacion no pudo realizarse correctamente"
                )

    def buscar_registro(self, dni):
        """Busca registros de la tabla 'personal' de la base de datos 'personal_v2'. Este metodo tambien es utilizado en las operaciones de borrar y actualizar para traer los daots de la base de datos a la aplicacion"""
        self.conexion = self.conexion_base_datos()
        self.instruccion = "SELECT * FROM personal WHERE dni=?"
        self.cursor = self.conexion.cursor()
        self.cursor.execute(self.instruccion, (dni,))
        self.resultado_consulta = self.cursor.fetchall()
        self.conexion.commit()
        return self.resultado_consulta
