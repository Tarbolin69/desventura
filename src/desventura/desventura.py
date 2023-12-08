import csv
import ast
import time
import os
import textwrap


def menu_principal():
    print(
        r"""
  .-,--.                       .
  ' |   \ ,-. ,-. .  , ,-. ,-. |- . . ,-. ,-.
  , |   / |-' `-. | /  |-' | | |  | | |   ,-|
  `-^--'  `-' `-' `'   `-' ' ' `' `-^ '   `-^
  - El mejor juego de texto escrito en Python

[1] Nuevo Juego [2] Cargar [3] Creditos [0] Salir
"""
    )
    while True:
        eleccion = input("\n¿Que te gustaria hacer?\n> ").strip().lower()
        if eleccion == "1":
            nuevo_juego()
        elif eleccion == "2":
            continuar_partida()
        elif eleccion == "3":
            creditos()
        elif eleccion == "0":
            print("¡Hasta pronto!")
            break
        else:
            print("Opcion invalida")


def nuevo_juego():
    while True:
        aceptar = input("Desearia ver el tutorial? (Si/No)\n> ").strip().lower()
        if aceptar == "si":
            tutorial()
            break
        elif aceptar == "no":
            iniciar_nueva_partida()
        else:
            print("Opcion invalida")


def creditos():
    try:
        with open("creditos.txt", "rt", encoding="utf-8") as creditos:
            print(creditos.read())
    except FileExistsError or FileNotFoundError as err:
        print("ERROR: " + repr(err))


def print_lento(texto):
    print()
    for letra in texto:
        print(letra, end="")
        # time.sleep(0.0001)
    print()


def archivo_a_dict(camino):
    try:
        with open(camino, "rt", encoding="utf-8-sig") as archivo:
            csv_dict = csv.DictReader(archivo, delimiter=";")
            return list(csv_dict)
    except Exception:
        print("El archivo no pudo ser leido")
        return


def archivo_a_txt(camino):
    try:
        with open(camino, "rt", encoding="utf-8-sig") as archivo:
            archivo_leido = archivo.read()
    except Exception:
        print("El archivo no pudo ser leido")
        return
    else:
        return archivo_leido


def mirar(objetivo: str):
    print(f"Miras {objetivo}")


def agarrar(objetivo: str):
    print(f"Agarras {objetivo}")


def usar(objetivo: str):
    print(f"Usas {objetivo}")


def ir(objetivo: str):
    print(f"Vas a {objetivo}")


def acciones(accion, mapa, inventario, objetos):
    if not accion:
        print()
        print("Ingrese una opcion valida")
        return
    print()
    objetivo = accion.strip().lower().split()[-1]
    accion = accion.strip().lower().split()[0]
    match accion:
        case "mirar":
            mirar(objetivo)
        case "agarrar":
            agarrar(objetivo)
        case "usar":
            usar(objetivo)
        case "ir":
            ir(objetivo)
        case _:
            print("Esa no es una opcion valida")


def juego(mapa, objetos):
    inventario = []
    while True:
        describir_locacion(mapa)
        accion = input("\n¿Que te gustaria hacer?\n> ").strip().lower()
        acciones(accion, mapa, inventario, objetos)


def tutorial():
    camino = os.path.join("historias", "venturas_en_holand")
    intro_archivo = os.path.join(camino, "INICIO.txt")
    intro_mapa = os.path.join(camino, "mapa.csv")
    intro_objetos = os.path.join(camino, "objetos.csv")
    dict_objetos = archivo_a_dict(intro_objetos)
    dict_mapa = archivo_a_dict(intro_mapa)
    print_lento(archivo_a_txt(intro_archivo))
    juego(dict_mapa, dict_objetos)


def inicializar_partida_locacion():
    pass


def describir_locacion(mapa):
    print()
    for locacion in mapa:
        if locacion["estado"] == "1":
            print(textwrap.fill(locacion["texto"], 80))
    print()
    print("Las habitaciones adyacentes son:")
    for locacion in mapa:
        if locacion["estado"] == "1":
            for adyacente in ast.literal_eval(locacion["adyacentes"]):
                print(f"- {adyacente}")
    print()


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def cambiar_ubicacion():
    pass


def hablar_con_personaje(camino):
    ruta = os.path.join(camino, "personajes", "agujero.csv")
    with open(ruta, "rt", encoding="utf-8-sig") as renglones:
        dialogos = [x.rstrip().split(";") for x in renglones]
        print(dialogos[1][2])
        time.sleep(1)
        print(dialogos[1][3])
        cant = [str(x + 1) for x, _ in enumerate(dialogos[2:])]
        print(cant)
        while True:
            for x, y in enumerate(dialogos[2:-1]):
                print(x + 1, "-", y[2])
            print(len(cant), "- Irte")
            opcion = input("Q: ")
            if opcion == cant[-1]:
                break
            elif opcion in cant:
                print(dialogos[int(opcion) + 1][3])
        print(dialogos[int(opcion) + 1][2])
        time.sleep(1)
        print(dialogos[int(opcion) + 1][3])
    return


def iniciar_nueva_partida():
    # Usando una partida (camino al .csv) como argumento, crea una copia, apendando X al final del nombre y
    # moviendola a la carpeta de "partidas". Empieza el juego con esa partida y cambia la variable "nivel" a 0
    pass


def continuar_partida():
    # Elige una de las partidas en "partidas", remueva todas las "X" de los otros archivos, y la pasa a el archivo
    # seleccionado, eligiendolo
    pass


menu_principal()
