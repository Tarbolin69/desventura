# Intentemos usar la libreria CSV para hacer mas simple el leer archivos como diccionarios
import csv

# OS es para que funcione bien en Mac, Windows y Linux
import os

# RICH talvez vamos a usar para que sea mejor la experiencia al escribir
import rich


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
        eleccion = input(f"\n¿Que te gustaria hacer?\n> ").strip().lower()
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
    aceptar = input("Desearia ver el tutorial? (Si/No)\n> ").strip().lower()
    while True:
        if aceptar == "si":
            tutorial()
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


def tutorial():
    # Esto tendria que leer y usar la carpeta TUTORIAL
    pass


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
