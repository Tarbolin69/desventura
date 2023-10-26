import os


# def tutorial():
#    oro = 1
#    pala = 1
#    cuerda = 1
#    puerta = 0
#    ventana = 0
#    norte = 0
#    sur = 0
#    if (oro == 1 and pala == 1 and cuerda == 1) and (ventana == 0 and puerta == 0):
#        print(
#            r"""
#    Este el tutorial oficial de Desventura. Aqui veras las bases sobre como avanzar en el
#    juego y como usar las herramientas que tienes a tu disposicion. Si has jugado juegos
#    de texto en el pasado, entonces esto te resultara familar.
#
#    Imaginemos lo siguiente:
#
#                                   /`\            (        /`\
#                            /`\   // \\           ))      // \\
#                           // \\  // \\  /`\______||      // \\
#                           // \\  // \\ // /       \  /`\ // \\
#                           // \\  // \\ ///_________\// \\// \\
#                           // \\  // \\ // |-[+]---| // \\// \\
#                           // \\  // \\ // |-------| // \\// \\
#              _____,....-----'------'-----''-------'---'----'--
#   `~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~`~
#    Te encuentras solo en una cabaña, en un bosque, en el medio de la noche. Al
#    NORTE hay una PUERTA y una VENTANA. En la esquina de la cabaña puedes ver una
#    PALA, una CUERDA y ORO. Tienes que esconder el ORO antes de que algo malo ocurra.
#
#    Las opciones a tu disposicion en Desventura son las siguientes:
#        * Mirar {objeto/dirección}: Te da la descripción de un objeto o lo que hay en una dirección
#        * Agarrar {objeto}: Te permite poner un objeto que puedas agarrar en tu inventario
#        * Usar {objeto}: Usas uno de tus objetos
#        * Ir {objeto/direccion}: Vas hacia un objeto o dirección
#
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
# print(  # Tipografia: stampatello
#    r"""
# .-,--.                       .
#' |   \ ,-. ,-. .  , ,-. ,-. |- . . ,-. ,-.
# , |   / |-' `-. | /  |-' | | |  | | |   ,-|
# `-^--'  `-' `-' `'   `-' ' ' `' `-^ '   `-^
# - El mejor juego de texto escrito en Python
#
# [1] Nuevo Juego [2] Cargar [3] Creditos [0] Salir
#
#                                           """
# )
# eleccion = int(input(f"\n¿Que te gustaria hacer?\n> "))
#
#
# if eleccion == 1:
#    print("Desearia ver el tutorial? (Si/No)")
#    aceptar = input(f"\n¿Que te gustaria hacer?\n> ")
#    aceptar = aceptar.lower()
#    if aceptar == "si":
#        tutorial()
#    else:
#        print(
#            r"""
#        Te encuentras solo en una gran y poderosa oscuridad. La unica luz viene de atras de
#        las rejas de tu celda. A tu lado tienes un CERILLO y una LAMPARA. Frente a ti, hay
#        una PUERTA DE ACERO cerrado con llave la cual lleva hacia la libertad.
#
#        ¿Que vas a hacer?
#        """
#        )


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
