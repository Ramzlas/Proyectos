import pandas as pd
import numpy as np

# Función para cargar los datos del archivo CSV
def cargar_datos(archivo):
    try:
        tabla = pd.read_csv(archivo)  # Leer el archivo CSV

        # Asegurarse de que no haya espacios en blanco en las columnas
        tabla['Nombre'] = tabla['Nombre'].str.strip()
        tabla['Apellido'] = tabla['Apellido'].str.strip()
        tabla['Fecha de Nacimiento'] = tabla['Fecha de Nacimiento'].str.strip()

        # Calcular la edad automáticamente a partir de la fecha de nacimiento
        tabla['Fecha de Nacimiento'] = pd.to_datetime(tabla['Fecha de Nacimiento'], format='%d/%m/%Y')
        today = pd.to_datetime('today')

        # Calcular la edad de manera más precisa usando apply
        tabla['Edad'] = tabla['Fecha de Nacimiento'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)))

        # Agregar la columna 'Estado' basada en la Nota
        condiciones = [
            (tabla['Nota'] >= 7),  # Apto para promoción
            (tabla['Nota'] >= 4)   # Aprobado
        ]
        opciones = ['Apto para promoción', 'Aprobado']

        # Usamos np.select para asignar el estado según las condiciones
        tabla['Estado'] = np.select(condiciones, opciones, default='Desaprobado')  # Usar np.select

        return tabla
    except FileNotFoundError:
        print(f"El archivo {archivo} no se encontró.")
    except pd.errors.EmptyDataError:
        print("El archivo está vacío o tiene un formato incorrecto.")
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
    return None

# Mostrar los datos filtrados
def mostrar_datos(resultados):
    print(f"{'Nombre':<15} {'Apellido':<15} {'Fecha de Nacimiento':<20} {'Edad':<5} {'Nota':<5} {'Estado':<20}")
    print("-" * 80)  # Separador para mejorar la legibilidad
    for index, row in resultados.iterrows():
        print(f"{row['Nombre']:<15} {row['Apellido']:<15} {row['Fecha de Nacimiento'].strftime('%d/%m/%Y'):<20} {row['Edad']:<5} {row['Nota']:<5} {row['Estado']:<20}")

# Función para buscar por nombre
def buscar_por_nombre(tabla):
    while True:
        nombre_buscar = input("Ingrese el nombre que desea buscar o presione [Enter] para finalizar: ")
        if nombre_buscar == "":
            break
        nombre_buscar = nombre_buscar.lower().strip()

        # Filtramos por nombre
        resultados = tabla[tabla['Nombre'].str.lower() == nombre_buscar]

        if not resultados.empty:
            print(f"\nSe encontraron {len(resultados)} resultado(s) para el nombre \"{nombre_buscar}\":")
            mostrar_datos(resultados)
        else:
            print(f"No se encontraron resultados para el nombre \"{nombre_buscar}\".")

# Función para filtrar por estado
def filtrar_por_estado(tabla):
    while True:
        estado_buscar = input("Ingrese el estado (Apto para promoción, Aprobado, Desaprobado) o presione [Enter] para finalizar: ")
        if estado_buscar == "":
            break
        estado_buscar = estado_buscar.strip()

        # Filtramos por estado
        resultados = tabla[tabla['Estado'].str.lower() == estado_buscar.lower()]

        if not resultados.empty:
            print(f"\nSe encontraron {len(resultados)} resultado(s) para el estado \"{estado_buscar}\":")
            mostrar_datos(resultados)
        else:
            print(f"No se encontraron resultados para el estado \"{estado_buscar}\".")

# Función para filtrar por rango de notas
def filtrar_por_rango_notas(tabla):
    while True:
        try:
            nota_minima = float(input("Ingrese la nota mínima: "))
            if 0 <= nota_minima <= 10:
                break
        except ValueError:
            print("Error, se debe ingresar un número válido.")

    while True:
        try:
            nota_maxima = float(input("Ingrese la nota máxima: "))
            if 0 <= nota_maxima <= 10 and nota_maxima >= nota_minima:
                break
        except ValueError:
            print("Error, se debe ingresar un número válido.")

    resultados = tabla[(tabla['Nota'] >= nota_minima) & (tabla['Nota'] <= nota_maxima)]

    if resultados.empty:
        print(f"No se encontraron personas en el rango de notas ({nota_minima}, {nota_maxima}).")
    else:
        print(f"\nSe encontraron {len(resultados)} resultado(s) en el rango de notas ({nota_minima}, {nota_maxima}):")
        mostrar_datos(resultados)

# Menú principal
def menu():
    archivo = "datos.csv"  # Archivo CSV
    tabla = cargar_datos(archivo)  # Cargar los datos desde el archivo CSV
    if tabla is None:
        return
    
    while True:
        print("-" * 80)
        print("|" * 25, "MENÚ DE OPCIONES", "|" * 25)
        print("-" * 80)
        print("1. Búsqueda por nombre")
        print("2. Filtrado por estado (Apto para promoción, Aprobado, Desaprobado)")
        print("3. Filtrar por rango de notas")
        print("4. Salir")
        print("-" * 80)

        try:
            opcion = int(input("Ingrese la opción (1-4): "))
            print("-" * 80)
            if opcion == 1:
                buscar_por_nombre(tabla)
            elif opcion == 2:
                filtrar_por_estado(tabla)
            elif opcion == 3:
                filtrar_por_rango_notas(tabla)
            elif opcion == 4:
                break
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")
        except ValueError:
            print("Error, ingrese un número entero. Intente nuevamente.")
        print("-" * 80)

if __name__ == "__main__":
    menu()
