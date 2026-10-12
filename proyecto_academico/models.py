from datetime import date


class ModeloBase:

    def __init__(self, id_registro):
        self.id = int(id_registro)

    @classmethod
    def desde_diccionario(cls, datos):
        datos = dict(datos)
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        return "registro " + str(self.id)

    def __str__(self):
        return "[" + str(self.id) + "] " + self.etiqueta()


class Persona(ModeloBase):

    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return self.nombre + " " + self.apellido

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Estudiante(Persona):

    def __init__(self, id_registro, nombre, apellido, email, carnet="", carrera=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        return super().etiqueta() + " · " + self.carnet + " · " + self.carrera


class Materia(ModeloBase):

    CUPOS_MAXIMOS = 30
    NOTA_APROBACION = 14

    def __init__(self, id_registro, nombre, codigo, creditos=0, cupos=0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    @staticmethod
    def es_nota_valida(valor):
        try:
            nota = float(valor)
        except ValueError:
            return False
        return nota >= 0 and nota <= 20

    def hay_cupo(self):
        return self.cupos > 0

    def ocupar_cupo(self):
        self.cupos = self.cupos - 1

    def liberar_cupo(self):
        self.cupos = self.cupos + 1

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.codigo
        datos["creditos"] = self.creditos
        datos["cupos"] = self.cupos
        return datos

    def etiqueta(self):
        return (self.codigo + " · " + self.nombre + " · " + str(self.creditos)
                + " créditos · cupos " + str(self.cupos))


class Matricula(ModeloBase):

    def __init__(self, id_registro, estudiante_id, materia_id, periodo, nota=0, fecha=""):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo
        self.nota = float(nota)
        if fecha == "":
            fecha = date.today().isoformat()
        self.fecha = fecha

    def esta_aprobada(self):
        return self.nota >= Materia.NOTA_APROBACION

    def estado(self):
        if self.esta_aprobada():
            return "Aprobado"
        return "Reprobado"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["nota"] = self.nota
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (self.fecha + " · estudiante " + str(self.estudiante_id)
                + " · materia " + str(self.materia_id) + " · " + self.periodo
                + " · nota " + str(self.nota) + " · " + self.estado())
