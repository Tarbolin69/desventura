import csv
import shutil
import ast
import time
import os
import textwrap


def menu_principal() -> None:
    """Menu principal de Desventura.

    Pre: Pregunta al usuario mediante un menu si quiere iniciar una nueva partida, continuar una partida, ver los créditos, o salir.
    Post: Corre la función adecuada a la elección del usuario o sale del programa."""
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
        eleccion = input("\n¿Que te gustaría hacer?\n> ").strip().lower()
        match eleccion:
            case "1":
                nuevo_juego()
            case "2":
                continuar_partida()
            case "3":
                creditos()
            case "0":
                print("¡Hasta pronto!")
                break
            case _:
                print("Opción invalida")


def nuevo_juego() -> None:
    """Iniciar nueva campaña

    Pre: Pregunta al usuario si desea jugar al tutorial, si no, pregunta al usuario que campaña jugar.
    Post: Inicia el juego usando la campaña de tutorial o una de las campañas disponibles dependiendo de la elección del usuario."""
    while True:
        aceptar = input("Desearía ver el tutorial? (Si/No)\n> ").strip().lower()
        if aceptar == "si":
            iniciar_nueva_partida("venturas_en_holand")
            break
        elif aceptar == "no":
            campaña = elegir_campaña("historias")
            iniciar_nueva_partida(campaña)
            break
        else:
            print("Opción invalida")
            print()


def creditos() -> None:
    """Mostrar créditos
    Pre: Lee el archivo <creditos.txt>
    Post: Imprime por pantalla el contenido de <creditos.txt>"""
    try:
        with open("creditos.txt", "rt", encoding="utf-8") as creditos:
            print(creditos.read())
    except Exception as err:
        print("ERROR: " + repr(err))


def archivo_a_dict(camino: str) -> list[dict]:
    """Convierte archivo csv a lista de diccionarios

    Pre: Recibe un camino completo o relativo hacia el archivo csv (delimitado por ;) a leer.
    Post: Se devuelve una lista de diccionarios con key/values obtenidos por cada columna del archivo,
    devuelve una lista de diccionarios vacía si ocurrió un error al leer el archivo"""
    try:
        with open(camino, "rt", encoding="utf-8-sig") as archivo:
            csv_dict = csv.DictReader(archivo, delimiter=";")
            return list(csv_dict)
    except Exception:
        print("El archivo no pudo ser leído")
        return [{}]


def archivo_a_txt(camino: str) -> list[str]:
    """Guardar y formatear archivo .txt a memoria.

    Pre: Recibe un camino completo o relativo hacia el archivo a leer.
    Post: Se devuelve una lista compuesta por las lineas del archivo leído,
    o una lista vacía si ocurrió un error al leer el archivo."""
    try:
        with open(camino, "rt", encoding="utf-8-sig") as archivo:
            archivo_leido = archivo.read().split("\n")
    except Exception:
        print("El archivo no pudo ser leído")
        return [""]
    else:
        return archivo_leido


def acciones_posibles() -> None:
    """Listar acciones posibles

    Pre: Usa y lee un diccionario conteniendo todas las posibles acciones del juego y sus objetivos.
    Post: Imprime cada llave y valor del diccionario en múltiples lineas."""
    acciones = {
        "Mirar": "<objeto/lugar>",
        "Hablar": "<personaje>",
        "Agarrar": "<objeto>",
        "Ir": "<locación",
        "Usar": "<objeto>",
        "Salir": "",
    }
    print()
    print("ACCIONES POSIBLES:")
    for acción, objetivo in acciones.items():
        print(f"- {acción} {objetivo}")


def mirar(
    objetivo: str, mapa: list[dict], objetos: list[dict], inventario: list[dict]
) -> None:
    """Acción 'mirar'

    Pre: Utiliza los contenidos de mapa (para la ubicación), la lista objetos y la lista inventario como el objetivo a mirar.
    Post: Imprime la descripción de una ubicación, un objeto en la ubicación actual o en el inventario,
    o los contenidos del inventario dependiendo del objetivo."""
    objetivo = objetivo.title()
    if objetivo == "Inventario":
        if inventario:
            print("Tu inventario contiene:")
            for item in inventario:
                print(f"- {item['nombre']}")
            return
        else:
            print("Tu inventario esta vació")
            return
    for locacion in mapa:
        if (
            locacion["estado"] in ["1", "3"]
            and objetivo in locacion["items"]
            and len(objetivo)
        ):
            for items in objetos:
                if objetivo == items["nombre"]:
                    print(f"{objetivo}: {items['descripción']}")
                    return
        if objetivo == locacion["ubicacion"] and locacion["estado"] in ["1", "3"]:
            describir_locacion(mapa)
            return
    for item in inventario:
        if objetivo == item["nombre"]:
            print(f"{objetivo}: {item['descripción']}")
            return
    print(f"El {objetivo} no se encuentra")


def agarrar(objetivo: str, mapa: list[dict], objetos: list[dict]) -> dict:
    """Acción 'agarrar'

    Pre: Utiliza el mapa (para la ubicación), la lista de objetos disponibles y el objetivo a agarrar.
    Post: Mueve un objeto con el que puedas interactuar desde la lista de objetos a tu inventario.
    Remueve ese objeto de la lista de objetos disponibles en la ubicación actual."""
    objetivo = objetivo.title()
    objetivo_especial = "*" + objetivo.title()
    for locacion in mapa:
        items_posibles = ast.literal_eval(locacion["items"])
        if (
            locacion["estado"] in ["1", "3"]
            and items_posibles != ""
            and (objetivo in items_posibles or objetivo_especial in items_posibles)
        ):
            for i, objeto in enumerate(objetos):
                if objeto["nombre"] == objetivo:
                    item = objetos.pop(i)
                    locacion["items"] = locacion["items"].replace(objetivo, " ")
                    print(f"Obtuviste {objetivo}")
                    return item
                elif objeto["nombre"] == objetivo_especial:
                    item = objetos.pop(i)
                    locacion["items"] = locacion["items"].replace(
                        objetivo_especial, " "
                    )
                    print(f"Obtuviste {objetivo}")
                    return item
    print(f"No puedes agarrar {objetivo}")
    return {}


def usar(
    objetivo: str, inventario: list[dict], mapa: list[dict], texto_final: list[str]
) -> None:
    """Acción 'usar'

    Pre: Toma el mapa (ubicación), contenidos del inventario, el objetivo a usar y el texto de victoria.
    Post: Usa un objeto que poseas en tu inventario en la ubicación actual.
    Si es el objeto especial (*) y el usuario se encuentra en la sala final (estado = 3),
    imprime el texto de victoria y termina la partida."""
    item_titulo = "*" + objetivo.title()
    final = False
    for item in inventario:
        if item["nombre"] == item_titulo:
            final = True
            break
    if final:
        for locacion in mapa:
            if locacion["estado"] == "3":
                victoria(texto_final)
        print("No puedes usar este item aquí")
    print("No tienes ese item en tu inventario")


def hablar(objetivo: str, mapa: list[dict], camino: str) -> None:
    """Acción 'hablar'

    Pre: Toma el camino de la carpeta de campaña para acceder a los archivos de personaje,
    el mapa (ubicación) y el objetivo (personaje con el cual hablar)
    Post: Abre el menu de dialogo con el personaje objetivo si este se encuentra en tu ubicación actual."""
    personaje = objetivo.strip().lower() + ".csv"
    for locacion in mapa:
        if locacion["estado"] == "1" and locacion["personajes"] == personaje:
            hablar_con_personaje(camino, personaje)
            return
    print(f"No puedes hablar con {objetivo}")


def hablar_con_personaje(camino: str, personaje: str) -> None:
    """Abrir menu de dialogo con personaje seleccionado

    Pre: Se recibe el camino a la carpeta de la campaña y el nombre del personaje objetivo.
    Post: Abre un menu que permite seleccionar las opciones de dialogo disponibles para ese personaje."""
    ruta = os.path.join(camino, "personajes", personaje)
    with open(ruta, "rt", encoding="utf-8-sig") as renglones:
        diálogos = [x.rstrip().split(";") for x in renglones]
        print_acomodado(diálogos[1][2])
        time.sleep(1)
        print_acomodado(diálogos[1][3])
        print()
        cantidad = [str(x + 1) for x, _ in enumerate(diálogos[2:])]
        while True:
            for x, y in enumerate(diálogos[2:-1]):
                print(x + 1, "-", y[2])
            print(len(cantidad), "- Irte")
            opción = input("\nElige que preguntar: ").strip().lower()
            if opción == cantidad[-1]:
                break
            elif opción in cantidad:
                print()
                print_acomodado(diálogos[int(opción) + 1][3])
                print()
        print()
        print_acomodado(diálogos[int(opción) + 1][2])
        time.sleep(1)
        print_acomodado(diálogos[int(opción) + 1][3])


def ir(objetivo: str, mapa: list[dict]) -> None:
    """Acción 'ir'

    Pre: Toma el mapa (ubicación) y la ubicación objetivo a la cual navegar.
    Post: Cambia el 'estado' de la ubicación objetivo a '1' o '3' (indicando que el usuario se encuentra hay)
    y el 'estado' de la ubicación inicial a '0' o '2' (indicando que el usuario no se encuentra hay)"""
    objetivo_locacion = objetivo.title()
    inicio = dict()
    for locacion in mapa:
        if locacion["estado"] in ["1", "3"]:
            inicio = locacion
            break
    if inicio["ubicacion"] == objetivo_locacion:
        print(f"Ya te encuentras en {objetivo_locacion}")
        return
    for locacion in mapa:
        if locacion["ubicacion"] == objetivo_locacion:
            if inicio["estado"] == "3":
                inicio["estado"] = "2"
                locacion["estado"] = "1"
                print(f"Has ido a {objetivo_locacion}")
                print()
                describir_locacion(mapa)
                return
            elif inicio["estado"] == "1" and locacion["estado"] == "0":
                inicio["estado"] = "0"
                locacion["estado"] = "1"
                print(f"Has ido a {objetivo_locacion}")
                print()
                describir_locacion(mapa)
                return
            elif inicio["estado"] == "1" and locacion["estado"] == "2":
                inicio["estado"] = "0"
                locacion["estado"] = "3"
                print(f"Has ido a {objetivo_locacion}")
                print()
                describir_locacion(mapa)
                return
    print(f"No puedes ir a {objetivo_locacion}")


def acciones(
    acción: str,
    mapa: list[dict],
    objetos: list[dict],
    camino: str,
    inventario: list[dict],
    texto_final: list[str],
    campaña: str,
) -> None:
    """Lógica para las acciones en el juego.

    Pre: Hereda todas los argumentos esenciales para que el juego funcione,
    obtenidos usando los archivos de la carpeta de campaña seleccionada.

    Post: Usa el input de 'acción' del usuario y lo divide en dos partes: <acción> <objetivo>.
    <acción> es usada para seleccionar la acción, mientras que <objetivo> se convierte en el
    argumento de dicha acción."""
    if not acción:
        print()
        print("Ingrese una opción valida")
        return
    print()
    acción_input = acción.strip().split()
    acción = acción_input[0]
    objetivo = " ".join(acción_input[1:])
    match acción:
        case "mirar":
            mirar(objetivo, mapa, objetos, inventario)
        case "agarrar":
            agarrado = agarrar(objetivo, mapa, objetos)
            if agarrado:
                inventario.append(agarrado)
        case "usar":
            usar(objetivo, inventario, mapa, texto_final)
        case "hablar":
            hablar(objetivo, mapa, camino)
        case "ir":
            ir(objetivo, mapa)
        case "salir":
            guardar_partida(campaña, mapa, objetos, inventario)
        case _:
            print("Esa no es una opción valida")
            acciones_posibles()


def print_acomodado(texto: str) -> None:
    """Acomodar print con largo máximo.

    Pre: Toma un str de cualquier largo como argumento.
    Post: Imprime el str con un largo de linea máximo de 80 caracteres. Acomoda a nueva linea si lo excede."""
    print(textwrap.fill(texto, 80))


def describir_locacion(mapa: list[dict]) -> None:
    """Describe locación actual.

    Pre: mapa para obtener la locación actual del usuario.
    Post: Imprime la descripción, lista de items y adyacencias de la ubicación actual (que puede ser '1' o '3')."""
    for locacion in mapa:
        if locacion["estado"] in ["1", "3"]:
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


def juego(
    mapa: list[dict],
    objetos: list[dict],
    camino: str,
    texto_final: list[str],
    inventario: list[dict],
    campaña: str,
):
    """Loop central del juego.

    Pre: Toma la lista de: objetos, mapa e inventario como también el texto de victoria
    y el camino a la carpeta de la campaña.
    Post: Pide al usuario que ingrese una acción continuamente
    hasta que se gane el juego o se ingrese la opción de salir."""
    describir_locacion(mapa)
    while True:
        acción = input("\n¿Que te gustaría hacer?\n> ").strip().lower()
        acciones(acción, mapa, objetos, camino, inventario, texto_final, campaña)


def print_centro(texto: str) -> None:
    """Centrar print

    Pre: Toma un str de cualquier largo.
    Post: Imprime texto centrado en la terminal."""
    print(texto.center(shutil.get_terminal_size().columns))


def limpiar_pantalla() -> None:
    """Limpia la terminal (tanto en Windows como UNIX)."""
    os.system("cls" if os.name == "nt" else "clear")


def iniciar_nueva_partida(campaña: str) -> None:
    """Iniciar nueva partida usando una carpeta de campaña.

    Pre: Toma el camino a la carpeta de campaña.
    Post: Usando el camino dado, lee los archivos de INICIO y FINAL, imprime los contenidos de INICIO,
    y crea listas de diccionarios usando los csv de mapa y objetos. Inicializa el inventario, y empieza
    el loop del juego."""
    inventario = []
    camino = os.path.join("historias", campaña)
    intro_archivo = os.path.join(camino, "INICIO.txt")
    fin_archivo = os.path.join(camino, "FINAL.txt")
    intro_mapa = os.path.join(camino, "mapa.csv")
    intro_objetos = os.path.join(camino, "objetos.csv")
    dict_objetos = archivo_a_dict(intro_objetos)
    dict_mapa = archivo_a_dict(intro_mapa)
    limpiar_pantalla()
    inicio_texto = archivo_a_txt(intro_archivo)
    fin_texto = archivo_a_txt(fin_archivo)
    if inicio_texto:
        for linea in inicio_texto:
            print_acomodado(linea)
    juego(dict_mapa, dict_objetos, camino, fin_texto, inventario, campaña)


def iniciar_partida(campaña: str) -> None:
    """Continua una partida usando una carpeta de partida guardada.

    Pre: Toma el camino de la campaña a continuar
    Post: Usando la carpeta de partidas mas el camino dado, lee los archivos de INICIO y FINAL, imprime
    los contenidos de INICIO, y crea listas de diccionarios usando los csv de mapa y objetos. Inicializa
    el inventario usando el csv del inventario guardado, y empieza el loop del juego."""
    camino = os.path.join("partidas", campaña)
    intro_archivo = os.path.join(camino, "INICIO.txt")
    fin_archivo = os.path.join(camino, "FINAL.txt")
    intro_mapa = os.path.join(camino, "mapa.csv")
    intro_objetos = os.path.join(camino, "objetos.csv")
    inventario = os.path.join(camino, "inventario.csv")
    dict_objetos = archivo_a_dict(intro_objetos)
    dict_mapa = archivo_a_dict(intro_mapa)
    dict_inventario = archivo_a_dict(inventario)
    limpiar_pantalla()
    print(dict_mapa)
    inicio_texto = archivo_a_txt(intro_archivo)
    fin_texto = archivo_a_txt(fin_archivo)
    if inicio_texto:
        for linea in inicio_texto:
            print_acomodado(linea)
    juego(dict_mapa, dict_objetos, camino, fin_texto, dict_inventario, campaña)


def guardar_partida(
    camino: str, mapa: list[dict], objetos: list[dict], inventario: list[dict]
):
    """Guardar estado actual de la campaña.

    Pre: Toma el camino de la campaña actual mas las listas de diccionarios usadas durante la
    misma (mapa, objetos, inventario).
    Post: Crea una nueva carpeta en la carpeta 'partidas' con el estado actual de la campaña,
    incluyendo el inventario, antes de salir. Si el usuario ingresa 'no', simplemente sale del programa."""
    while True:
        elección = input("\n¿Te gustaría guardar (Si/No)?\n> ").strip().lower()
        if elección == "no":
            quit()
        elif elección == "si":
            camino_completo = os.path.join("historias", camino)
            n_partida = "1"
            partida = os.path.join("partidas", camino + "_" + n_partida)
            while os.path.exists(partida):
                n_partida += "0"
                partida = os.path.join("partidas", camino + "_" + n_partida)
            os.mkdir(partida)
            crear_copia_aventura(camino_completo, partida)
            crear_mapa_guardado(mapa, partida)
            crear_objetos_guardado(objetos, partida)
            crear_inventario_csv(inventario, partida)
            quit()
        print("Ingrese una opción valida")


def elegir_campaña(carpeta: str) -> str:
    """Lista todas las campañas disponibles

    Pre: Toma el camino hacia la carpeta de campañas.
    Post: Lista campañas disponibles para jugar y le pregunta al usuario cual quiere elegir.
    Devuelve el camino a dicha campaña."""
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


def crear_copia_aventura(camino: str, partida: str) -> None:
    """Copiar archivos esenciales.

    Pre: Toma el camino a la carpeta de campañas y a la carpeta de partidas guardadas.
    Post: Crea una copia de los archivos estáticos de la campaña a guardar."""
    inicio = os.path.join(camino, "INICIO.txt")
    final = os.path.join(camino, "FINAL.txt")
    personajes = os.path.join(camino, "personajes")
    personajes_partida = os.path.join(partida, "personajes")
    shutil.copy(inicio, partida)
    shutil.copy(final, partida)
    shutil.copytree(personajes, personajes_partida)


def crear_mapa_guardado(mapa: list[dict], partida: str) -> None:
    """Copiar estado de mapa.

    Pre: Toma el camino a la carpeta de campañas y a la carpeta de partidas guardadas.
    Post: Guarda el estado actual del mapa a un archivo csv en la carpeta de partidas"""
    mapa_locacion = os.path.join(partida, "mapa.csv")
    header = ["ubicacion", "estado", "adyacentes", "texto", "items", "personajes"]
    try:
        with open(
            mapa_locacion,
            "wt",
            encoding="utf-8-sig",
            newline="",
        ) as nuevo_mapa:
            dict_a_csv = csv.DictWriter(nuevo_mapa, fieldnames=header, delimiter=";")
            dict_a_csv.writeheader()
            dict_a_csv.writerows(mapa)
    except Exception:
        print("No se pudo guardar el mapa")


def crear_objetos_guardado(objetos: list[dict], partida: str) -> None:
    """Copiar estado de objetos.

    Pre: Toma el camino a la carpeta de campañas y a la carpeta de partidas guardadas.
    Post: Guarda el estado actual de los objetos a un archivo csv en la carpeta de partidas"""
    objetos_locacion = os.path.join(partida, "objetos.csv")
    header = ["nombre", "locacion", "descripción"]
    try:
        with open(
            objetos_locacion,
            "wt",
            encoding="utf-8-sig",
            newline="",
        ) as nuevo_objetos:
            dict_a_csv = csv.DictWriter(nuevo_objetos, fieldnames=header, delimiter=";")
            dict_a_csv.writeheader()
            dict_a_csv.writerows(objetos)
    except Exception:
        print("No se pudo guardar los objetos")


def crear_inventario_csv(inventario: list[dict], partida: str) -> None:
    """Copiar estado de inventario.

    Pre: Toma el camino a la carpeta de campañas y a la carpeta de partidas guardadas como
    también el estado actual del inventario del usuario.
    Post: Guarda el estado actual del inventario a un archivo csv en la carpeta de partidas"""
    inventario_locacion = os.path.join(partida, "inventario.csv")
    header = ["nombre", "locacion", "descripción"]
    try:
        with open(
            inventario_locacion,
            "wt",
            encoding="utf-8-sig",
            newline="",
        ) as nuevo_inventario:
            dict_a_csv = csv.DictWriter(
                nuevo_inventario, fieldnames=header, delimiter=";"
            )
            dict_a_csv.writeheader()
            dict_a_csv.writerows(inventario)
    except Exception:
        print("No se pudo guardar los objetos")


def continuar_partida() -> None:
    """Continuar campaña guardada.

    Pre: Pregunta al usuario si desea continuar una partida.
    Post: Lista las partidas guardadas en la carpeta de partidas si se desea continuar."""
    while True:
        aceptar = input("¿Desearía continuar una partida? (Si/No)\n> ").strip().lower()
        if aceptar == "si":
            campaña = elegir_campaña("partidas")
            iniciar_partida(campaña)
            break
        elif aceptar == "no":
            break
        else:
            print("Opción invalida")


def victoria(texto_final: list[str]):
    """Imprime el texto de victoria y termina el juego, saliendo del programa."""
    limpiar_pantalla()
    for linea in texto_final:
        print_acomodado(linea)
    print_centro("===== HAS GANADO =====")
    quit()


menu_principal()
