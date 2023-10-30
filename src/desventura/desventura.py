import os
#import rich
#import csv


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
        eleccion = input(f"\n¿Que te gustaria hacer?\n> ")
        match eleccion:
            case "1":
                aceptar = input(f"Desearia ver el tutorial? (Si/No)\n> ")
                aceptar = aceptar.strip().lower()
                match aceptar:
                    case "si":
                        tutorial()
                    case "no":
                        iniciar_nueva_partida()
                    case _:
                        print("Opcion invalida")
                        continue
            case "2":
                continuar_partida()
            case "3":
                creditos()
            case "0":
                print("¡Hasta pronto!")
                break
            case _:
                print("Opcion invalida")
                continue


def creditos():
    try:
        with open("creditos.txt", "rt", encoding="utf-8") as creditos:
            print(creditos.read())
    except FileExistsError or FileNotFoundError as err:
        print("ERROR: " + repr(err))


def tutorial():
#    oro = 1
#    pala = 1
#    cuerda = 1
#    puerta = 0
#    ventana = 0
#    norte = 0
#    sur = 0
    while True:
        try:
            with open("TUTORIAL.txt", "rt", encoding="utf-8") as arch:
                print(arch.read())
#                eleccion = int(input(f"\n¿Que te gustaria hacer?\n> "))
        except FileNotFoundError or FileExistsError as err:
            print("ERROR :" + repr(err))


#    ¡Intenta usar una de estas opciones y observa que ocurre!"""
#        )
#    while True:
#        eleccion_tutorial = input(f"\n¿Que te gustaria hacer?\n> ")
#        eleccion_tutorial = eleccion_tutorial.lower()
#        if eleccion_tutorial == "mirar oro" and oro == 1:
#            print(
#                r"""
#                El ORO brilla resplandecientemente. Tienes que esconderlo.
#                """
#            )
#        elif eleccion_tutorial == "mirar oro" and oro == 0:
#            print(
#                r"""
#                El ORO brillo incluso dentro de tus bolsillos. Tienes que esconderlo mejor.
#                """
#            )
#        elif eleccion_tutorial == "agarrar oro" and oro == 1:
#            oro = 0
#            print(
#                r"""
#                Agarrar el ORO y lo escondes en tu bolsillo.
#                """
#            )
#        elif eleccion_tutorial == "mirar pala" and pala == 1:
#            print(
#                r"""
#                Ves una gran PALA en el piso. Podrias usarla en tu mision.
#                """
#            )
#        elif eleccion_tutorial == "mirar pala" and pala == 0:
#            print(
#                r"""
#                La PALA pesa en tu espalda, pero te sera de ayuda.
#                """
#            )
#        else:
#            print(
#                r"""
#                No puedes hacer eso.
#                """
#            )
#
#


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def iniciar_nueva_partida():
    # Usando una partida (camino al .csv) como argumento, crea una copia, apendando X al final del nombre y
    # moviendola a la carpeta de "partidas". Empieza el juego con esa partida y cambia la variable "nivel" a 0
    pass


def continuar_partida():
    # Elige una de las partidas en "partidas", remueva todas las "X" de los otros archivos, y la pasa a el archivo
    # seleccionado, eligiendolo
    pass


mapa = {  # Obtener esto de un csv
    "Celda": {"Sur": "Ateneo", "Norte": "Secreto"},
    "Secreto": {"Sur": "Celda"},
    "Ateneo": {"Norte": "Celda", "Este": "Armeria", "Oeste": "Baño"},
    "Baño": {"Este": "Ateneo"},
    "Armeria": {"Oeste": "Ateneo", "Sur": "Barracas"},
    "Barracas": {"Norte": "Armeria"},
}

ubiacion = ""  # Para decirle al jugador donde estan

inventario = []  # list[str], ayuda a guardar el estado de la partida

nivel = 0  # Guarda el progreso de la historia

menu_principal()
