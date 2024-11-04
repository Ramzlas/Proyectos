import pandas as pd

# Clase para manejar la información de cada persona
class Persona:
    def __init__(propio, dni, nombre, apellido, edad, email, fecha, lugar):
        propio.dni = dni  # DNI de la persona
        propio.nombre = nombre.strip()  # Limpiar espacios en el nombre
        propio.apellido = apellido.strip()  # Limpiar espacios en el apellido
        propio.edad = edad  # Edad de la persona
        propio.email = email.strip()  # Limpiar espacios en el email
        propio.fecha = fecha  # Fecha asociada a la persona
        propio.lugar = lugar.strip()  # Limpiar espacios en el lugar

# Cargar los datos del archivo CSV
def cargar_datos(archivo):
    try:
        tabla = pd.read_csv(archivo, delimiter=",", encoding="utf-8")  # Leer el archivo CSV
        # Limpiar espacios en las columnas
        tabla["Nombre"] = tabla["Nombre"].str.strip()  # Limpiar espacios en la columna de nombres
        tabla["Apellido"] = tabla["Apellido"].str.strip()  # Limpiar espacios en la columna de apellidos
        tabla["Email"] = tabla["Email"].str.strip()  # Limpiar espacios en la columna de emails
        tabla["Lugar"] = tabla["Lugar"].str.strip()  # Limpiar espacios en la columna de lugares
        return tabla
    except FileNotFoundError:
        print(f"El archivo {archivo} no se encontró.")  # Mensaje si el archivo no se encuentra
    except pd.errors.EmptyDataError:
        print("El archivo está vacío o tiene un formato incorrecto.")  # Mensaje si el archivo está vacío
    return None

# Mostrar los datos filtrados
def mostrar_datos(resultados):
    print(f"{'DNI':<15} {'Nombre':<15} {'Apellido':<15} {'Edad':<5} {'Email':<50} {'Fecha':<15} {'Lugar':<15}")
    print("-" * 160)  # Línea divisoria
    for index, row in resultados.iterrows():
        print(f"{row['DNI']:<15} {row['Nombre']:<15} {row['Apellido']:<15} {row['Edad']:<5} {row['Email']:<50} {row['Fecha']:<15} {row['Lugar']:<15}")

# Filtrar por nombre
def buscar_por_nombre(tabla):
    while True:
        nombre_buscar = input("Ingrese el nombre que desea buscar o presione [Enter] para finalizar: ")
        if nombre_buscar == "":
            break
        nombre_buscar = nombre_buscar.lower().strip()  # Convertir a minúsculas y limpiar espacios

        # Filtramos por nombre
        resultados = tabla[tabla["Nombre"].str.lower() == nombre_buscar]

        if not resultados.empty:
            print(f"\nSe encontraron {len(resultados)} resultado(s) para el nombre \"{nombre_buscar}\":")
            mostrar_datos(resultados)
        else:
            print(f"No se encontraron resultados para el nombre \"{nombre_buscar}\".")

# Filtrar por edad
def filtrar_por_edad(tabla, edad_minima, edad_maxima):
    resultados = tabla[(tabla["Edad"] >= edad_minima) & (tabla["Edad"] <= edad_maxima)]
    return resultados

# Filtrar por rango de edades
def filtrar_por_rango_edades(tabla):
    while True:
        try:
            edad_minima = int(input("Ingrese la edad mínima (0 a 120): "))
            if 0 <= edad_minima <= 120:
                break
        except ValueError:
            print("Error, se deben ingresar enteros.")

    while True:
        try:
            edad_maxima = int(input("Ingrese la edad máxima: "))
            if edad_minima <= edad_maxima <= 120:
                break
        except ValueError:
            print("Error, se deben ingresar enteros.")

    resultados = filtrar_por_edad(tabla, edad_minima, edad_maxima)

    if resultados.empty:
        print(f"No se encontraron personas en el rango ({edad_minima}, {edad_maxima}).")
    else:
        print(f"\nSe encontraron {len(resultados)} resultado(s) en el rango de edad ({edad_minima}, {edad_maxima}):")
        mostrar_datos(resultados)

# Menú principal
def menu():
    tabla = cargar_datos("datos.csv")  # Asegúrate de que este archivo tenga el delimitador correcto
    if tabla is None:
        return
    
    while True:
        print("-" * 160)
        print("|" * 71, "MENÚ DE OPCIONES", "|"* 71)
        print("-" * 160)
        print("1. Busqueda por nombre")
        print("2. Filtrado por edad")
        print("3. Salida del programa")
        print("-" * 160)

        try:
            opcion = int(input("Ingrese la opción (1-3): "))
            print("-" * 160)
            if opcion == 1:
                buscar_por_nombre(tabla)
            elif opcion == 2:
                filtrar_por_rango_edades(tabla)
            elif opcion == 3:
                break
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")
        except ValueError:
            print("Error, ingrese un número entero. Intente nuevamente.")
        print("-" * 160) # Separador

if __name__ == "__main__":
    menu()
