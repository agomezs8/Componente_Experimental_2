import os

RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def imprimir_titulo(texto):
    limpiar_pantalla()
    print("=" * 60)
    print(texto.center(60))
    print("=" * 60)
    print()


def imprimir_exito(mensaje):
    print("✓ " + mensaje)


def imprimir_error(mensaje):
    print("✗ " + mensaje)


def imprimir_info(mensaje):
    print("ℹ " + mensaje)


def confirmar(pregunta):
    respuesta = input(pregunta + " (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    partes = texto.split("@")
    usuario = partes[0]
    dominio = partes[1]
    if usuario == "":
        return False
    if "." not in dominio:
        return False
    if dominio.endswith("."):
        return False
    return True
