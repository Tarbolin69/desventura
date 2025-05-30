import os


def crear_campaña():
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
        return
    else:
        return campaña_carpeta


def nombrar_ubicaciones():
    ubicaciones = []
    print('\t--- Ingrese "ADIOS" para salir ---')
    print("\t--- La primera ubicacion es el principio de la campaña  ---")
    while True:
        ubicacion = input("Nombra la ubicacion: ").strip().title()
        if ubicacion.lower() == "adios":
            break
        while True:
            descripcion = input("Dale una descripcion a la ubicacion: ").strip()
            if descripcion:
                break
            print("Cada ubicacion necesita una descripcion")
        lugar = {"ubicacion": ubicacion, "descripcion": descripcion, "adyacentes": []}
        ubicaciones.append(lugar)
    print("--- Es recomendable que toda ubicacion tenga al menos 1 adyacencia ---")
    for lugar in ubicaciones:
        print(f"Ubicación actual: {lugar['ubicacion']}")
        disponibles = [area["ubicacion"] for area in ubicaciones if area != lugar]
        print(f"Ubicaciones disponibles: {", ".join(disponibles)}")
        print('Ingresar "ADIOS" si no hay mas adyacencias')
        for _ in range(len(disponibles)):
            adyacente = (
                input(f"Ingrese adyacencia a {lugar["ubicacion"]}: ").strip().title()
            )
            if adyacente.lower() == "adios":
                break
            if adyacente not in disponibles or adyacente in lugar["adyacentes"]:
                print("Ingrese una ubicacion existente y que no sea ya adyacente")
            else:
                lugar["adyacentes"].append(adyacente)
    return ubicaciones


def crear_personaje(camino):
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
            print("Ingrese una opcion valida")
        multiples = True
        nombre = input("Cual es en nombre de tu personaje? ")
        nombre_acomodado = nombre.strip().title()
        nombre_archivo = nombre.strip().lower().replace(" ", "_")
        camino_archivo = os.path.join(camino, "personajes")
        os.mkdir(camino_archivo)
        archivo_nombre = os.path.join(camino_archivo, f"{nombre_archivo}.csv")
        linea = 1
        print(archivo_nombre)
        try:
            with open(archivo_nombre, "wt", encoding="utf-8-sig") as personaje:
                personaje.write("nombre;opcion;pregunta;respuesta\n")
                interactuar = input("Interaccion inicial (e.j <Hablar con el viejo>): ")
                descripcion = input(
                    "Ingresa el texto que aparecera cuando se interactua con tu personaje: "
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
            print("Ha occurrido un problema en el sistema operativo")
        else:
            print(f"¡{nombre_acomodado} fue creado correctamente!")
        # poner un for que te pregunte en que ubicacion se encuentra cada personaje
        # mas o menos lo mismo que en los objetos


def crear_objetos(camino, ubicaciones):
    archivo_nombre = os.path.join(camino, "objetos.csv")
    try:
        with open(archivo_nombre, "wt", encoding="utf-8-sig") as objetos:
            objetos.write("nombre;locacion;descripción\n")
            while True:
                print('Para cancelar la carga ingrese "ADIOS".')
                nombre = input("Ingrese el nombre del objeto: ").strip().title()
                if "adios" in nombre.lower():
                    break
                print("--- Ubicaciones disponibles ---")
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
        print("ERROR: Ha occurrido un problema en el sistema operativo")
    else:
        print("Los objetos fueron creados correctamente!")


def mapa_linea(lugar, objetos, estado, personajes):
    ubicacion = lugar["ubicacion"]
    adyacentes = lugar["adyacentes"]
    descripcion = lugar["descripcion"]
    items = []
    for objeto in objetos:
        if objeto["locacion"] == ubicacion:
            items.append(objeto["nombre"])
    if items == "":
        items = "NADA"
    # FALTA ITERAR SOBRE TODOS LOS ARCHIVOS EN LA CARPETA PERSONAJES
    # Y HACER LO MISMO QUE CON LOS ITEMS
    # Y PARA HACER HABRIA QUE PREGUNTA EN QUE UBICACION SE ENCUENTRAN
    # COMO SE HACE CON LOS ITEMS
    return f"{lugar};{estado};{adyacentes};{descripcion};{items};personajes"


def crear_mapa(camino, lugares):
    archivo_nombre = os.path.join(camino, "mapa.csv")
    try:
        with open(archivo_nombre, "wt", encoding="utf-8-sig") as mapa:
            mapa.write("ubicacion;estado;adyacentes;texto;items;personajes\n")
            estado = 1
            for lugar in lugares:
                # falta obtener todos los argumentos requeridos
                # 2 hay que obtenerlos leyendo archivos
                mapa.write(mapa_linea(lugar, 0, estado, 0))
                estado = 0
    except FileExistsError:
        print("Ya existe este mapa")
    except OSError:
        print("No se ha podido escribir el mapa")


def main():
    campaña = crear_campaña()
    if not campaña:
        return
    ubicaciones = nombrar_ubicaciones()
    crear_personaje(campaña)
    crear_objetos(campaña, ubicaciones)
    crear_mapa(campaña, ubicaciones)


main()
