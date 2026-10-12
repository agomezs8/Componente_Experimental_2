from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from models import Materia
from views import EstudianteController, MateriaController, MatriculaController

estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(texto):
    try:
        return int(input(texto))
    except ValueError:
        return None


def mostrar_resultado(resultado):
    exito = resultado[0]
    mensaje = resultado[1]
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio):
    if len(objetos) == 0:
        imprimir_info(vacio)
    else:
        for objeto in objetos:
            print("  " + str(objeto))
        imprimir_info("Total: " + str(len(objetos)))


def mostrar_detalle(objeto):
    datos = objeto.a_diccionario()
    for clave in datos:
        print("  " + clave + ": " + str(datos[clave]))


def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {}
    datos["nombre"] = input("Nombre: ")
    datos["apellido"] = input("Apellido: ")
    datos["email"] = input("Email: ")
    datos["carnet"] = input("Carnet: ")
    datos["carrera"] = input("Carrera: ")
    mostrar_resultado(estudiantes.crear(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavía no hay estudiantes.")
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    texto = input("Nombre, email, carnet o carrera: ")
    mostrar_lista(estudiantes.buscar(texto), "No se encontró ningún estudiante.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(estudiante)
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        imprimir_info("Editando: " + estudiante.etiqueta())
        print("Deje en blanco lo que no quiera cambiar.\n")
        datos = {}
        nombre = input("Nombre [" + estudiante.nombre + "]: ")
        if nombre != "":
            datos["nombre"] = nombre
        apellido = input("Apellido [" + estudiante.apellido + "]: ")
        if apellido != "":
            datos["apellido"] = apellido
        email = input("Email [" + estudiante.email + "]: ")
        if email != "":
            datos["email"] = email
        carnet = input("Carnet [" + estudiante.carnet + "]: ")
        if carnet != "":
            datos["carnet"] = carnet
        carrera = input("Carrera [" + estudiante.carrera + "]: ")
        if carrera != "":
            datos["carrera"] = carrera
        mostrar_resultado(estudiantes.actualizar(id_estudiante, datos))
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        imprimir_info("Se eliminará: " + estudiante.etiqueta())
        if confirmar("¿Confirma?"):
            mostrar_resultado(estudiantes.eliminar(id_estudiante))
        else:
            imprimir_info("Operación cancelada")
    pausa()


def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {}
    datos["nombre"] = input("Nombre: ")
    datos["codigo"] = input("Código (ej. MAT101): ")
    datos["creditos"] = input("Créditos (1 a 10): ")
    datos["cupos"] = input("Cupos (0 a " + str(Materia.CUPOS_MAXIMOS) + "): ")
    mostrar_resultado(materias.crear(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavía no hay materias.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    texto = input("Nombre o código: ")
    mostrar_lista(materias.buscar(texto), "No se encontró ninguna materia.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrada")
    else:
        mostrar_detalle(materia)
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrada")
    else:
        imprimir_info("Editando: " + materia.etiqueta())
        print("Deje en blanco lo que no quiera cambiar.\n")
        datos = {}
        nombre = input("Nombre [" + materia.nombre + "]: ")
        if nombre != "":
            datos["nombre"] = nombre
        codigo = input("Código [" + materia.codigo + "]: ")
        if codigo != "":
            datos["codigo"] = codigo
        creditos = input("Créditos [" + str(materia.creditos) + "]: ")
        if creditos != "":
            datos["creditos"] = creditos
        cupos = input("Cupos [" + str(materia.cupos) + "]: ")
        if cupos != "":
            datos["cupos"] = cupos
        mostrar_resultado(materias.actualizar(id_materia, datos))
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrada")
    else:
        imprimir_info("Se eliminará: " + materia.etiqueta())
        if confirmar("¿Confirma?"):
            mostrar_resultado(materias.eliminar(id_materia))
        else:
            imprimir_info("Operación cancelada")
    pausa()


def matricular():
    imprimir_titulo("MATRICULAR")
    datos = {}
    datos["estudiante_id"] = input("Id del estudiante: ")
    datos["materia_id"] = input("Id de la materia: ")
    datos["periodo"] = input("Periodo (ej. 2026-1): ")
    mostrar_resultado(matriculas.crear(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "Todavía no hay matrículas.")
    pausa()


def registrar_nota():
    imprimir_titulo("REGISTRAR NOTA")
    id_matricula = pedir_entero("Id de la matrícula: ")
    if matriculas.obtener(id_matricula) is None:
        imprimir_error("No existe esa matrícula")
    else:
        nota = input("Nota (0 a 20): ")
        mostrar_resultado(matriculas.registrar_nota(id_matricula, nota))
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO")
    texto = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if texto is None:
        imprimir_error("No existe esa matrícula")
    else:
        print(texto)
    pausa()


def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")
    id_matricula = pedir_entero("Id de la matrícula: ")
    if confirmar("Se liberará el cupo. ¿Confirma?"):
        mostrar_resultado(matriculas.retirar_matricula(id_matricula))
    else:
        imprimir_info("Operación cancelada")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN")
    print("  Estudiantes       : " + str(len(estudiantes.leer())))
    print("  Carreras          : " + ", ".join(estudiantes.carreras()))
    print("  Materias          : " + str(len(materias.leer())))
    nombres = []
    for materia in materias.materias_sin_cupo():
        nombres.append(materia.nombre)
    print("  Materias sin cupo : " + ", ".join(nombres))
    print("  Matrículas        : " + str(len(matriculas.leer())))
    print("  Aprobadas         : " + str(matriculas.total_aprobadas()))
    pausa()


def menu_estudiantes():
    opcion = ""
    while opcion != "0":
        imprimir_titulo("ESTUDIANTES")
        print("  1. Crear estudiante")
        print("  2. Ver todos")
        print("  3. Buscar")
        print("  4. Ver por id")
        print("  5. Actualizar")
        print("  6. Eliminar")
        print("  0. Volver\n")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_estudiante()
        elif opcion == "2":
            listar_estudiantes()
        elif opcion == "3":
            buscar_estudiante()
        elif opcion == "4":
            ver_estudiante()
        elif opcion == "5":
            actualizar_estudiante()
        elif opcion == "6":
            eliminar_estudiante()
        elif opcion != "0":
            imprimir_error("Opción no válida")
            pausa()


def menu_materias():
    opcion = ""
    while opcion != "0":
        imprimir_titulo("MATERIAS")
        print("  1. Crear materia")
        print("  2. Ver todas")
        print("  3. Buscar")
        print("  4. Ver por id")
        print("  5. Actualizar")
        print("  6. Eliminar")
        print("  0. Volver\n")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_materia()
        elif opcion == "2":
            listar_materias()
        elif opcion == "3":
            buscar_materia()
        elif opcion == "4":
            ver_materia()
        elif opcion == "5":
            actualizar_materia()
        elif opcion == "6":
            eliminar_materia()
        elif opcion != "0":
            imprimir_error("Opción no válida")
            pausa()


def menu_matriculas():
    opcion = ""
    while opcion != "0":
        imprimir_titulo("MATRÍCULAS")
        print("  1. Matricular")
        print("  2. Ver todas")
        print("  3. Registrar nota")
        print("  4. Ver certificado")
        print("  5. Retirar matrícula")
        print("  0. Volver\n")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            matricular()
        elif opcion == "2":
            listar_matriculas()
        elif opcion == "3":
            registrar_nota()
        elif opcion == "4":
            ver_certificado()
        elif opcion == "5":
            retirar_matricula()
        elif opcion != "0":
            imprimir_error("Opción no válida")
            pausa()


def main():
    opcion = ""
    while opcion != "0":
        imprimir_titulo("SISTEMA ACADÉMICO")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            menu_estudiantes()
        elif opcion == "2":
            menu_materias()
        elif opcion == "3":
            menu_matriculas()
        elif opcion == "4":
            resumen()
        elif opcion != "0":
            imprimir_error("Opción no válida")
            pausa()
    imprimir_info("¡Hasta luego!")


main()
