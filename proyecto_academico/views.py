from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


class EstudianteController:

    def __init__(self):
        self.gestor = GestorJSON("data/estudiantes.json")
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for estudiante in self.lista:
            datos.append(estudiante.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "carnet"):
                if datos[campo].strip() == "":
                    return "El campo " + campo + " es obligatorio"

        if "email" in datos:
            email = datos["email"].strip().lower()
            if not es_email_valido(email):
                return "Email inválido"
            emails_usados = set()
            for estudiante in self.lista:
                if estudiante.id != id_actual:
                    emails_usados.add(estudiante.email)
            if email in emails_usados:
                return "Ese email ya está registrado"

        if "carnet" in datos:
            carnet = datos["carnet"].strip().upper()
            # CONJUNTO: no guarda repetidos y preguntar "in" es muy rápido
            carnets_usados = set()
            for estudiante in self.lista:
                if estudiante.id != id_actual:
                    carnets_usados.add(estudiante.carnet)
            if carnet in carnets_usados:
                return "Ese carnet ya está registrado"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_estudiante):
        for estudiante in self.lista:
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for estudiante in self.lista:
            # TUPLA: los campos donde se busca son fijos, no cambian
            campos = (estudiante.nombre, estudiante.apellido, estudiante.email,
                      estudiante.carnet, estudiante.carrera)
            for campo in campos:
                if texto in campo.lower():
                    encontrados.append(estudiante)
                    break
        return encontrados

    def siguiente(self):
        mayor = 0
        for estudiante in self.lista:
            if estudiante.id > mayor:
                mayor = estudiante.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        estudiante = Estudiante(self.siguiente(),
                                datos["nombre"].strip().title(),
                                datos["apellido"].strip().title(),
                                datos["email"].strip().lower(),
                                datos["carnet"].strip().upper(),
                                datos["carrera"].strip().title())
        self.lista.append(estudiante)
        self.guardar()
        return True, "Estudiante creado: " + estudiante.etiqueta()

    def actualizar(self, id_estudiante, datos):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, "No existe un estudiante con ese id"
        if len(datos) == 0:
            return False, "No se indicó ningún cambio"

        error = self.validar(datos, id_estudiante)
        if error:
            return False, error

        if "nombre" in datos:
            estudiante.nombre = datos["nombre"].strip().title()
        if "apellido" in datos:
            estudiante.apellido = datos["apellido"].strip().title()
        if "email" in datos:
            estudiante.email = datos["email"].strip().lower()
        if "carnet" in datos:
            estudiante.carnet = datos["carnet"].strip().upper()
        if "carrera" in datos:
            estudiante.carrera = datos["carrera"].strip().title()

        self.guardar()
        return True, "Estudiante actualizado"

    def eliminar(self, id_estudiante):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, "No existe un estudiante con ese id"

        self.lista.remove(estudiante)
        self.guardar()
        return True, "Estudiante eliminado"

    def carreras(self):
        distintas = set()
        for estudiante in self.lista:
            if estudiante.carrera != "":
                distintas.add(estudiante.carrera)
        return sorted(distintas)


class MateriaController:

    def __init__(self):
        self.gestor = GestorJSON("data/materias.json")
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for materia in self.lista:
            datos.append(materia.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo", "creditos", "cupos"):
                if datos[campo].strip() == "":
                    return "El campo " + campo + " es obligatorio"

        if "codigo" in datos:
            codigo = datos["codigo"].strip().upper()
            # CONJUNTO: el código no se puede repetir y "in" responde al instante
            codigos_usados = set()
            for materia in self.lista:
                if materia.id != id_actual:
                    codigos_usados.add(materia.codigo)
            if codigo in codigos_usados:
                return "Ese código ya existe"

        if "creditos" in datos:
            creditos = datos["creditos"].strip()
            if not creditos.isdigit():
                return "Los créditos deben ser un número entero"
            if int(creditos) < 1 or int(creditos) > 10:
                return "Los créditos deben estar entre 1 y 10"

        if "cupos" in datos:
            cupos = datos["cupos"].strip()
            if not cupos.isdigit():
                return "Los cupos deben ser un número entero"
            if int(cupos) > Materia.CUPOS_MAXIMOS:
                return "Los cupos no pueden ser más de " + str(Materia.CUPOS_MAXIMOS)
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_materia):
        for materia in self.lista:
            if materia.id == id_materia:
                return materia
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontradas = []
        if texto == "":
            return encontradas

        for materia in self.lista:
            if texto in materia.nombre.lower() or texto in materia.codigo.lower():
                encontradas.append(materia)
        return encontradas

    def siguiente(self):
        mayor = 0
        for materia in self.lista:
            if materia.id > mayor:
                mayor = materia.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        materia = Materia(self.siguiente(),
                          datos["nombre"].strip().title(),
                          datos["codigo"].strip().upper(),
                          int(datos["creditos"]),
                          int(datos["cupos"]))
        self.lista.append(materia)
        self.guardar()
        return True, "Materia creada: " + materia.etiqueta()

    def actualizar(self, id_materia, datos):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, "No existe una materia con ese id"
        if len(datos) == 0:
            return False, "No se indicó ningún cambio"

        error = self.validar(datos, id_materia)
        if error:
            return False, error

        if "nombre" in datos:
            materia.nombre = datos["nombre"].strip().title()
        if "codigo" in datos:
            materia.codigo = datos["codigo"].strip().upper()
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])

        self.guardar()
        return True, "Materia actualizada"

    def eliminar(self, id_materia):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, "No existe una materia con ese id"

        self.lista.remove(materia)
        self.guardar()
        return True, "Materia eliminada"

    def materias_sin_cupo(self):
        sin_cupo = []
        for materia in self.lista:
            if not materia.hay_cupo():
                sin_cupo.append(materia)
        return sin_cupo


class MatriculaController:

    def __init__(self, estudiantes, materias):
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON("data/matriculas.json")
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for matricula in self.lista:
            datos.append(matricula.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos):
        if not datos["estudiante_id"].strip().isdigit():
            return "El id del estudiante debe ser un número"
        if not datos["materia_id"].strip().isdigit():
            return "El id de la materia debe ser un número"
        if datos["periodo"].strip() == "":
            return "El periodo es obligatorio"

        estudiante_id = int(datos["estudiante_id"])
        materia_id = int(datos["materia_id"])
        periodo = datos["periodo"].strip()

        # CONJUNTO: guarda los ids que existen y "in" responde al instante
        ids_estudiantes = set()
        for estudiante in self.estudiantes.leer():
            ids_estudiantes.add(estudiante.id)
        if estudiante_id not in ids_estudiantes:
            return "No existe un estudiante con ese id"

        ids_materias = set()
        for materia in self.materias.leer():
            ids_materias.add(materia.id)
        if materia_id not in ids_materias:
            return "No existe una materia con ese id"

        materia = self.materias.obtener(materia_id)
        if not materia.hay_cupo():
            return "No hay cupos disponibles en " + materia.nombre

        for matricula in self.lista:
            if (matricula.estudiante_id == estudiante_id
                    and matricula.materia_id == materia_id
                    and matricula.periodo == periodo):
                return "Ese estudiante ya está matriculado en esa materia en ese periodo"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_matricula):
        for matricula in self.lista:
            if matricula.id == id_matricula:
                return matricula
        return None

    def siguiente(self):
        mayor = 0
        for matricula in self.lista:
            if matricula.id > mayor:
                mayor = matricula.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        materia = self.materias.obtener(int(datos["materia_id"]))
        matricula = Matricula(self.siguiente(),
                              int(datos["estudiante_id"]),
                              materia.id,
                              datos["periodo"].strip())

        materia.ocupar_cupo()
        self.materias.guardar()
        self.lista.append(matricula)
        self.guardar()
        return True, "Matrícula registrada en " + materia.nombre

    def registrar_nota(self, id_matricula, nota):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, "No existe esa matrícula"
        if not Materia.es_nota_valida(nota):
            return False, "La nota debe ser un número entre 0 y 20"

        matricula.nota = float(nota)
        self.guardar()
        return True, "Nota registrada: " + str(matricula.nota) + " (" + matricula.estado() + ")"

    def retirar_matricula(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, "No existe esa matrícula"

        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, "Matrícula retirada y cupo liberado"

    def certificado(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return None

        # DICCIONARIO ÍNDICE {id: objeto}: busca por id sin recorrer toda la lista
        estudiantes_por_id = {}
        for estudiante in self.estudiantes.leer():
            estudiantes_por_id[estudiante.id] = estudiante

        materias_por_id = {}
        for materia in self.materias.leer():
            materias_por_id[materia.id] = materia

        estudiante = estudiantes_por_id.get(matricula.estudiante_id)
        materia = materias_por_id.get(matricula.materia_id)

        texto = "CERTIFICADO #" + str(matricula.id) + "   periodo: " + matricula.periodo + "\n"
        if estudiante is None:
            texto = texto + "Estudiante: eliminado\n"
        else:
            texto = texto + ("Estudiante: " + estudiante.nombre_completo()
                             + "   (" + estudiante.carnet + ")\n")
        if materia is None:
            texto = texto + "Materia   : eliminada\n"
        else:
            texto = texto + ("Materia   : " + materia.nombre + "   (" + materia.codigo
                             + ") · " + str(materia.creditos) + " créditos\n")
        texto = texto + "-" * 42 + "\n"
        texto = texto + "Nota      : " + str(matricula.nota) + "\n"
        texto = texto + "Estado    : " + matricula.estado()
        return texto

    def matriculas_por_estudiante(self):
        # DICCIONARIO DE LISTAS: {estudiante_id: [sus matrículas]}
        agrupadas = {}
        for matricula in self.lista:
            agrupadas.setdefault(matricula.estudiante_id, []).append(matricula)
        return agrupadas

    def promedio_de_estudiante(self, id_estudiante):
        suma = 0
        cantidad = 0
        for matricula in self.lista:
            if matricula.estudiante_id == id_estudiante:
                suma = suma + matricula.nota
                cantidad = cantidad + 1
        if cantidad == 0:
            return 0
        return round(suma / cantidad, 2)

    def total_aprobadas(self):
        total = 0
        for matricula in self.lista:
            if matricula.esta_aprobada():
                total = total + 1
        return total
