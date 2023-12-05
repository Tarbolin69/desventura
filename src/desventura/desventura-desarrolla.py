import os


def crear_campaña():
    try:
        while True:
            campaña_titulo = input("Como se llamara tu campaña? ").strip()
            if campaña_titulo:
                campaña_titulo = campaña_titulo.lower().replace(" ", "_")
                break
            print("Debes darle un nombre a tu campaña")
        campaña_carpeta = os.path.join("historias", campaña_titulo)
        if os.path.exists(campaña_carpeta):
            print("ERROR: Esta campaña ya existe")
            return
        os.makedirs(campaña_carpeta)
    except:
        print("Ha ocurrido un error al crear la carpeta")
        return
    else:
        return campaña_carpeta


def nombrar_ubicaciones():
    ubicaciones = []
    print('\t--- Ingrese "ADIOS" para salir ---')
    print("\t--- La primera ubicacion es el principio de la campaña  ---")
    while True:
        ubicacion = input("Nombrar una de las ubicaciones: ").strip().title()
        if ubicacion.lower() == "adios":
            break
        while True:
            descripcion = input("Dale una descripcion a la ubicacion: ").strip()
            if descripcion:
                break
            print("Cada ubicacion necesita una descripcion")
        ubicaciones.append([ubicacion, descripcion])
    return ubicaciones


def crear_personaje(camino: str):
    multiples = False
    while True:
        if multiples:
            while True:
                crear = input("Desea crear otro personaje? (Si/No): ").strip()
                if crear.lower() == "no":
                    return
                elif crear.lower() == "si":
                    break
                print("Ingrese una opcion valida")
        else:
            while True:
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
        if os.path.exists(archivo_nombre):
            raise FileExistsError
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


def crear_objeto(camino):
    archivo_nombre = os.path.join(camino, "objetos.csv")
    try:
        with open(archivo_nombre, "wt", encoding="utf-8-sig") as objetos:
            objetos.write("nombre;locacion;descripción\n")
            while True:
                print("Para cancelar la carga ingrese SALIR.")
                nombre = input("Ingrese el nombre del objeto: ").strip().title()
                if "salir" in nombre.lower():
                    break
                locacion = (
                    input("Ingrese la ubicacion del objeto en el mapa: ")
                    .strip()
                    .lower()
                )
                descripcion = input("Ingrese la descripcion del objeto: ").strip()
                objetos.write(f"{nombre};{locacion};{descripcion}\n")
    except FileExistsError:
        print("ERROR: <objetos.csv> ya existe")
    except OSError:
        print("ERROR: Ha occurrido un problema en el sistema operativo")
    else:
        print("Los objetos fueron creados correctamente!")


def main():
    campaña = crear_campaña()
    if not campaña:
        return
    crear_personaje(campaña)
    crear_objeto(campaña)


main()
