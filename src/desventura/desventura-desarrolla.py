import os
import csv
import shutil


def print_centro(texto: str):
    """Imprime texto centrado en la terminal."""
    print(texto.center(shutil.get_terminal_size().columns))


def crear_campaña():
    """Crear nueva campaña

    Pre: Pregunta al usuario por el nombre de la campaña.
    Post: Intenta crear una carpeta dentro de la carpeta 'historias' con dicho nombre."""
    try:
        while True:
            campaña_titulo = input("Como se llamara tu campaña? ").strip()
            if campaña_titulo and campaña_titulo != "":
                campaña_titulo = campaña_titulo.lower().replace(" ", "_")
                break
            print("Debes darle un nombre a tu campaña")
        campaña_carpeta = os.path.join("historias", campaña_titulo)
        os.makedirs(campaña_carpeta)
    except OSError:
        print("Ha ocurrido un error al crear la carpeta")
    else:
        return campaña_carpeta


def texto_inicio(campaña: str):
    """Crear introducción a la campaña

    Pre: Pide al usuario que ingrese un texto introductorio a su campaña.
    Post: Crea un archivo con dicho texto el la carpeta de la campaña."""
    print_centro("=== Esta es la introducción de tu campaña ===")
    while True:
        inicio = input("> ").strip()
        if inicio:
            break
        print("Por favor, ingrese algún texto.")
    try:
        archivo_nombre = os.path.join(campaña, "INICIO.txt")
        with open(archivo_nombre, "wt", encoding="utf-8-sig") as introduccion:
            introduccion.write(inicio)
    except Exception as err:
        print("Hubo un error al crear el archivo:" + repr(err))


def texto_final(campaña: str):
    """Crear un texto de victoria para la campaña

    Pre: Pide al usuario que ingrese un texto de victoria a su campaña.
    Post: Crea un archivo con dicho texto el la carpeta de la campaña."""
    print_centro("=== Este es el texto final de tu campaña ===")
    while True:
        final = input("> ").strip()
        if final:
            break
        print("Por favor, ingrese algún texto")
    try:
        archivo_nombre = os.path.join(campaña, "FINAL.txt")
        with open(archivo_nombre, "wt", encoding="utf-8-sig") as despedida:
            despedida.write(final)
    except Exception as err:
        print("Hubo un error al crear el archivo:" + repr(err))


def nombrar_ubicaciones() -> list[dict]:
    """Nombra ubicaciones de la campaña

    Pre: Pide al usuario que ingrese el nombre, descripción y adyacencias de un ubicación en al mapa
    hasta que ingrese 'ADIOS'.
    Post: Devuelve las ubicaciones guardadas en una lista de diccionarios."""
    ubicaciones = []
    print_centro(
        '=== Ingrese al nombrar una ubicación "ADIOS" para terminar de escribir ==='
    )
    print_centro("=== La primera ubicación es el principio de la campaña  ===")
    print_centro(
        "=== La ultima ubicación que escribas sera donde se gane el juego (usando un objeto) ==="
    )
    print_centro(
        "=== ¡Recuerda mencionar si hay algún personaje aquí en la descripción! ==="
    )
    while True:
        ubicacion = input("Nombra la ubicación: ").strip().title()
        if ubicacion.lower() == "adios":
            break
        while True:
            descripcion = input("Dale una descripción a la ubicación: ").strip()
            if descripcion:
                break
            print("Cada ubicación necesita una descripción")
        lugar = {"ubicacion": ubicacion, "descripcion": descripcion, "adyacentes": []}
        ubicaciones.append(lugar)
    print_centro(
        "=== Es recomendable que toda ubicación tenga al menos 1 adyacencia ==="
    )
    for lugar in ubicaciones:
        print(f"Ubicación actual: {lugar['ubicacion']}")
        disponibles = [area["ubicacion"] for area in ubicaciones if area != lugar]
        print(f"Ubicaciones disponibles: {', '.join(disponibles)}")
        print('Ingresar "ADIOS" si no hay mas adyacencias')
        for _ in range(len(disponibles)):
            adyacente = (
                input(f"ingrese una adyacencia a {lugar['ubicacion']}: ")
                .strip()
                .title()
            )
            if adyacente.lower() == "adios":
                break
            if adyacente not in disponibles or adyacente in lugar["adyacentes"]:
                while True:
                    print("Ingrese una ubicacion existente y que no sea ya adyacente")
                adyacente = (
                    input(f"ingrese una adyacencia a {lugar['ubicacion']}: ")
                    .strip()
                    .title()
                )
            else:
                lugar["adyacentes"].append(adyacente)
    return ubicaciones


def crear_personaje(camino: str):
    """Crear personajes en la campaña

    Pre: Pide al usuario que ingrese el nombre de su personaje, cuales son las preguntas que se le pueden hacer
    a ese personaje, y sus respuestas.
    Post: Guarda toda la información en un csv en la carpeta de 'personajes' dentro de la carpeta de la campaña."""
    multiples = False
    while True:
        while True:
            if multiples:
                crear = input("Desea crear otro personaje? (Si/No): ").strip()
            else:
                crear = input("Desea crear un personaje? (Si/No): ").strip()
            if crear.lower() == "no":
                return
            elif crear.lower() == "si":
                break
            print("Ingrese una opción valida")
        multiples = True
        nombre = input("Cual es en nombre de tu personaje? ")
        nombre_acomodado = nombre.strip().title()
        nombre_archivo = nombre.strip().lower().replace(" ", "_")
        camino_archivo = os.path.join(camino, "personajes")
        os.mkdir(camino_archivo)
        archivo_nombre = os.path.join(camino_archivo, f"{nombre_archivo}.csv")
        linea = 1
        try:
            with open(archivo_nombre, "wt", encoding="utf-8-sig") as personaje:
                personaje.write("nombre;opcion;pregunta;respuesta\n")
                interactuar = input("Interacción inicial (e.j <Te acercas al viejo>): ")
                descripcion = input(
                    "Ingresa el texto que aparecerá cuando se interactúa con tu personaje: "
                )
                personaje.write(f"{nombre_acomodado};0;{interactuar};{descripcion}\n")
                while True:
                    pregunta = input(
                        "Ingrese una pregunta que hacer al personaje (ADIOS para salir): "
                    )
                    if pregunta.upper() == "ADIOS":
                        break
                    respuesta = input("Ingrese la respuesta del personaje: ")
                    personaje.write(
                        f"{nombre_acomodado};{linea};{pregunta};{respuesta}\n"
                    )
                    linea += 1
                salir = input(
                    'Como dejas de interactuar con este personaje? (e.j <"¡Me voy!" *Sale corriendo*): '
                )
                adios = input(
                    'Que dice tu personaje como despedida? (e.j <"Espero que te coman los perros">): '
                )
                personaje.write(f"{nombre_acomodado};{linea};{salir};{adios}\n")
        except FileExistsError:
            print("ERROR: Este personaje ya existe.")
        except OSError:
            print("Ha ocurrido un problema en el sistema operativo")
        else:
            print(f"¡{nombre_acomodado} fue creado correctamente!")


def crear_objetos(campaña: str, ubicaciones: list[dict]):
    """Crear objetos en la campaña

    Pre: Pide al usuario que ingrese el nombre del objeto, su descripción, y la ubicación del objeto en el mapa
    (usando la variable conteniendo las ubicaciones de la campaña).
    a ese personaje, y sus respuestas.
    Post: Guarda toda la información en <objetos.csv> en la carpeta de la campaña."""
    archivo_nombre = os.path.join(campaña, "objetos.csv")
    try:
        with open(archivo_nombre, "wt", encoding="utf-8-sig") as objetos:
            objetos.write("nombre;locacion;descripción\n")
            print_centro("== DEBE DE HABER 1 ITEM QUE EMPIECE CON * ==")
            print_centro("== ESTE ITEM SERA REQUERIDO PARA GANAR EL JUEGO ==")
            print("| Este item estará oculto, y el jugador no sabrá donde se encuentra")
            print(
                "| Asi que algo, o alguien, tendrá que decirle donde puede AGARRAR dicho item"
            )
            while True:
                print('Para cancelar la carga ingrese "ADIOS".')
                nombre = input("Ingrese el nombre del objeto: ").strip().title()
                if nombre.lower() == "adios":
                    break
                print_centro("--- Ubicaciones disponibles ---")
                for ubicacion in ubicaciones:
                    print("\t- " + ubicacion["ubicacion"])
                while True:
                    locacion = (
                        input("Ingrese la ubicacion del objeto en el mapa: ")
                        .strip()
                        .title()
                    )
                    if any(locacion in _["ubicacion"] for _ in ubicaciones):
                        break
                    print("Ingrese una ubicacion valida")
                while True:
                    descripcion = input("Ingrese la descripcion del objeto: ").strip()
                    if descripcion:
                        break
                    print("Ingrese una descripcion valida")
                objetos.write(f"{nombre};{locacion};{descripcion}\n")
    except FileExistsError:
        print("ERROR: <objetos.csv> ya existe")
    except OSError:
        print("ERROR: Ha ocurrido un problema en el sistema operativo")
    except Exception:
        print("Ha ocurrido un error al intentar escribir el archivo")
    else:
        print("Los objetos fueron creados correctamente!")


def mapa_linea(lugar: dict, objetos, estado: int, personajes: str) -> str:
    """Crea cada linea de <mapa.csv> usando los valores obtenidos en las previas funciones
    usadas para crear la campaña."""
    ubicacion = lugar["ubicacion"]
    adyacentes = lugar["adyacentes"]
    descripcion = lugar["descripcion"]
    items = []
    for objeto in objetos:
        if ubicacion in objeto["locacion"]:
            items.append(objeto["nombre"])
    if items == "":
        items = "NADA"
    if not personajes:
        personajes = "NADIE"
    return f"{ubicacion};{estado};{adyacentes};{descripcion};{items};{personajes}\n"


def leer_objetos(archivo: str):
    """Convertir una lista de diccionarios a un archivo csv."""
    try:
        with open(archivo, "rt", encoding="utf-8-sig") as ob:
            objetos = csv.DictReader(ob, delimiter=";")
            return list(objetos)
    except Exception:
        print("Ocurrió un error al intentar leer objetos")
        return []


def crear_mapa(camino: str, lugares: list[dict]):
    """Crear mapa de campaña

    Pre: Toma el camino a la carpeta de campaña y la lista de ubicaciones en el mapa.
    Post: Lee los archivos <objetos.csv> y todos los personajes el la carpeta de personajes
    y los usa para crear <mapa.csv>. Pregunta al usuario en que ubicacion del mapa se encuentra
    cada personaje."""
    archivo_nombre = os.path.join(camino, "mapa.csv")
    camino_archivo = os.path.join(camino, "personajes")
    archivo_objetos = os.path.join(camino, "objetos.csv")
    objetos = leer_objetos(archivo_objetos)
    lista_personajes = os.listdir(camino_archivo)
    try:
        with open(archivo_nombre, "wt", encoding="utf-8-sig") as mapa:
            mapa.write("ubicacion;estado;adyacentes;texto;items;personajes\n")
            estado = 1
            for i, lugar in enumerate(lugares):
                personajes = []
                print_centro("=== Personajes disponibles ===")
                print_centro('=== Ingrese "ADIOS" para salir ===')
                print_centro(
                    "=== O si es que no hay mas personajes en esa ubicacion ==="
                )
                for personaje in lista_personajes:
                    personaje_arreglado = personaje[:-4].replace("_", " ").title()
                    print(f"\t- {personaje_arreglado}")
                while True:
                    personaje_eleccion = input(
                        f"Ingrese el nombre de un personaje que se encuentra en {lugar['ubicacion']}: "
                    )
                    if personaje_eleccion.strip().lower() == "adios":
                        break
                    elif (
                        personaje_eleccion.strip().lower().replace(" ", "_") + ".csv"
                        in lista_personajes
                        and personaje_eleccion not in personajes
                    ):
                        personajes.append(personaje.strip())
                        print("Personaje añadido!")
                    else:
                        print("Ese personaje no existe o esta repetido")
                if i == len(lugares) - 1:
                    estado = 2
                mapa.write(mapa_linea(lugar, objetos, estado, ",".join(personajes)))
                estado = 0
    except FileExistsError:
        print("Ya existe este mapa")
    except OSError:
        print("No se ha podido escribir el mapa")


def main():
    campaña = crear_campaña()
    if not campaña:
        return
    texto_inicio(campaña)
    ubicaciones = nombrar_ubicaciones()
    crear_objetos(campaña, ubicaciones)
    crear_personaje(campaña)
    crear_mapa(campaña, ubicaciones)
    texto_final(campaña)


main()
