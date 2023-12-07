import csv
import time
import os


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
        elif eleccion == "4":
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
    for letra in texto:
        print(letra, end="")
        # sys.stdout.write(letra)
        time.sleep(0.0001)


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


def juego(mapa, objetos):
    inventario = []
    while True:
        pass


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

def describir_locacion(mapa)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def cambiar_ubicacion():
    pass


def hablar_con_personaje():
    pass


def iniciar_nueva_partida():
    # Usando una partida (camino al .csv) como argumento, crea una copia, apendando X al final del nombre y
    # moviendola a la carpeta de "partidas". Empieza el juego con esa partida y cambia la variable "nivel" a 0
    pass


def continuar_partida():
    # Elige una de las partidas en "partidas", remueva todas las "X" de los otros archivos, y la pasa a el archivo
    # seleccionado, eligiendolo
    pass


menu_principal()
