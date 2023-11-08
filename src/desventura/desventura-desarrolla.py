def crear_personaje():
    nombre = input("Cual es en nombre de tu personaje? ")
    nombre_acomodado = nombre.strip().title()
    nombre_archivo = nombre.strip().lower().replace(" ", "_")
    linea = 1
    try:
        with open(f"{nombre_archivo}.csv", "wt", encoding="utf-8") as personaje:
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
                personaje.write(f"{nombre_acomodado};{linea};{pregunta};{respuesta}\n")
                linea += 1
            salir = input(
                'Como dejas de interactuar con este personaje? (e.j <"¡Me voy!" *Sale corriendo*): '
            )
            adios = input(
                'Que dice tu personaje como despedida? (e.j <"Espero que te coman los perros">): '
            )
            personaje.write(f"{nombre_acomodado};{linea};{salir};{adios}\n")
    except FileExistsError:
        print("Este personaje ya existe.")
    except OSError:
        print("Tenes la compu jodida.")
    else:
        print(f"¡{nombre_acomodado} fue creado correctamente!")


crear_personaje()
