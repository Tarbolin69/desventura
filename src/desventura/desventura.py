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
        match eleccion:
            case "1":
                nuevo_juego()
            case "2":
                continuar_partida()
            case "3":
                creditos()
            case "0":
                print("¡Hasta pronto!")
            case _:
                print("Opcion invalida")


def nuevo_juego():
    while True:
        aceptar = input("Desearia ver el tutorial? (Si/No)\n> ").strip().lower()
        if aceptar == "si":
            iniciar_nueva_partida("venturas_en_holand")
            break
        elif aceptar == "no":
            campaña = elegir_campaña("historias")
            iniciar_nueva_partida(campaña)
            break
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


def mirar(objetivo: str, mapa, objetos):
    objetivo_titulo = objetivo.title()
    for locacion in mapa:
        if (
            locacion["estado"] == "1"
            and objetivo_titulo in locacion["items"]
            and len(objetivo_titulo)
        ):
            for items in objetos:
                if objetivo_titulo == items["nombre"]:
                    print_acomodado(items["descripción"])
                    return
    print(f"No puedes mirar {objetivo}")


def agarrar(objetivo: str, mapa: list[dict], objetos: list[dict]):
    objetivo = objetivo.title()
    for locacion in mapa:
        items_posibles = ast.literal_eval(locacion["items"])
        if (
            locacion["estado"] == "1"
            and items_posibles != ""
            and objetivo in items_posibles[0]
        ):
            for i, objeto in enumerate(objetos):
                if objeto["nombre"] == objetivo:
                    item = objetos.pop(i)
                    locacion["items"] = locacion["items"].replace(objetivo, " ")
                    print(f"Obtuviste {objetivo}")
                    return item
    print(f"No puedes agarrar {objetivo}")
    print()


def usar(objetivo: str, inventario, mapa):
    pass


def hablar(objetivo: str, mapa, camino):
    personaje = objetivo.strip().lower() + ".csv"
    for locacion in mapa:
        if locacion["estado"] == "1" and locacion["personajes"] == personaje:
            hablar_con_personaje(camino, personaje)
            return
    print(f"No puedes hablar con {objetivo}")


def hablar_con_personaje(camino: str, personaje: str):
    personaje_nombre = personaje[:-4].title()
    ruta = os.path.join(camino, "personajes", personaje)
    with open(ruta, "rt", encoding="utf-8-sig") as renglones:
        dialogos = [x.rstrip().split(";") for x in renglones]
        print_acomodado(dialogos[1][2])
        time.sleep(1)
        print_acomodado(dialogos[1][3])
        print()
        cant = [str(x + 1) for x, _ in enumerate(dialogos[2:])]
        while True:
            for x, y in enumerate(dialogos[2:-1]):
                print(x + 1, "-", y[2])
            print(len(cant), "- Irte")
            opcion = input("\nElige que preguntar: ").strip().lower()
            if opcion == cant[-1]:
                break
            elif opcion in cant:
                print()
                print_acomodado(dialogos[int(opcion) + 1][3])
                print()
        print()
        print_acomodado(dialogos[int(opcion) + 1][2])
        time.sleep(1)
        print_acomodado(dialogos[int(opcion) + 1][3])


def ir(objetivo: str, mapa: list[dict]):
    objetivo_locacion = objetivo.title()
    inicio = dict
    for locacion in mapa:
        if locacion["estado"] == "1":
            inicio = locacion
            break
    if locacion["ubicacion"] == objetivo_locacion:
        print(f"Ya te encuentras en {objetivo_locacion}")
        return
    for locacion in mapa:
        if locacion["ubicacion"] == objetivo_locacion:
            inicio["estado"] = "0"
            locacion["estado"] = "1"
            print(f"Has ido a {objetivo_locacion}")
            print()
            describir_locacion(mapa)
            return
    print(f"No puedes ir a {objetivo_locacion}")


def acciones(accion, mapa, objetos, camino):
    inventario = []
    if not accion:
        print()
        print("Ingrese una opcion valida")
        return
    print()
    accion_input = accion.split()
    accion = accion_input[0]
    objetivo = " ".join(accion_input[1:])
    match accion:
        case "mirar":
            # mirar(objetivo)
            mirar(objetivo, mapa, objetos)
        case "agarrar":
            agarrado = agarrar(objetivo, mapa, objetos)
            if agarrado:
                inventario.append(agarrado)
        case "usar":
            usar(objetivo, inventario, mapa)
        case "hablar":
            hablar(objetivo, mapa, camino)
        case "ir":
            ir(objetivo, mapa)
        case "salir":
            guardar_partida()
        case _:
            print("Esa no es una opcion valida")


def print_acomodado(texto):
    print(textwrap.fill(texto, 80))


def describir_locacion(mapa):
    for locacion in mapa:
        if locacion["estado"] == "1":
            adyacentes = ast.literal_eval(locacion["adyacentes"])
            items = ast.literal_eval(locacion["items"])
            print_acomodado(locacion["texto"])
            print()
            print("Las habitaciones adyacentes son:")
            for adyacente in adyacentes:
                print(f"- {adyacente}")
            print()
            if items and items[0] != " ":
                if len(items) > 1:
                    print(f"En {locacion['ubicacion']} puedes ver:")
                    for item in items:
                        if item[0] != "*":
                            print(f"- {item}")
                    return
                elif items[0][0] != "*":
                    print(f"En {locacion['ubicacion']} puedes ver:")
                    for item in items:
                        if item[0] != "*":
                            print(f"- {item}")
                    return
                else:
                    break
    print("No ves nada de uso en este lugar")


def juego(mapa, objetos, camino):
    describir_locacion(mapa)
    while True:
        accion = input("\n¿Que te gustaria hacer?\n> ").strip().lower()
        acciones(accion, mapa, objetos, camino)


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def iniciar_nueva_partida(campaña):
    camino = os.path.join("historias", campaña)
    intro_archivo = os.path.join(camino, "INICIO.txt")
    intro_mapa = os.path.join(camino, "mapa.csv")
    intro_objetos = os.path.join(camino, "objetos.csv")
    dict_objetos = archivo_a_dict(intro_objetos)
    dict_mapa = archivo_a_dict(intro_mapa)
    limpiar_pantalla()
    print_lento(archivo_a_txt(intro_archivo))
    juego(dict_mapa, dict_objetos, camino)


def continuar_partida():
    # Elige una de las partidas en "partidas", remueva todas las "X" de los otros archivos, y la pasa a el archivo
    # seleccionado, eligiendolo
    pass


def elegir_campaña(carpeta):
    lista_directorios = os.listdir(carpeta)
    while True:
        print("Campañas Disponibles:")
        for x, y in enumerate(lista_directorios):
            print(x + 1, "-", y.replace("_", " ").title())
        campaña = input("Seleccione una campaña: ")
        if campaña in [str(x + 1) for x, _ in enumerate(lista_directorios)]:
            break
        print("Fuera de rango.")
    nombre_directorio = str(lista_directorios[int(campaña) - 1])
    return os.path.join(nombre_directorio)


def guardar_partida():
    quit()


menu_principal()
