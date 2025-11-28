# src/datos/gestor_puntuaciones.py
import csv
import os
from datetime import datetime

def guardar_puntuacion_jugador(nombre, tiempo, errores, pistas, puntaje, estado):
    # Guarda la puntuación del jugador en el archivo CSV
    # Define estructura del archivo CSV
    archivo = 'puntuaciones.csv'
    nuevo_header = ['Nombre', 'Tiempo', 'Errores', 'Pistas', 'Puntaje', 'Estado', 'Fecha']
    filas_existentes = []
    header_actual = []

    # Lee el archivo existente si existe
    if os.path.isfile(archivo):
        try:
            with open(archivo, 'r', newline='') as f:
                reader = csv.reader(f)
                try:
                    # Lee el encabezado y las filas
                    header_actual = next(reader)
                    filas_existentes = list(reader)
                except StopIteration:
                    # Archivo vacío
                    pass
        except Exception as e:
            print(f"Error al leer archivo: {e}")

    # Migra el archivo al nuevo formato si es necesario
    if header_actual and 'Puntaje' not in header_actual:
        print("Migrando archivo de puntuaciones al nuevo formato...")
        filas_migradas = []
        # Actualiza cada fila al nuevo formato
        for fila in filas_existentes:
            # Convierte formato antiguo (5 columnas) al nuevo (7 columnas)
            if len(fila) == 5:
                # Inserta puntaje y estado por defecto
                fila.insert(4, 0) 
                fila.insert(5, 'N/A')
            filas_migradas.append(fila)
        filas_existentes = filas_migradas
    
    # Escribe el archivo con la nueva puntuación
    try:
        with open(archivo, 'w', newline='') as f:
            writer = csv.writer(f)
            # Escribe encabezado, filas existentes y nueva fila
            writer.writerow(nuevo_header)
            writer.writerows(filas_existentes)
            writer.writerow([nombre, f"{tiempo:.2f}", errores, pistas, puntaje, estado, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print("Puntuación guardada.")
    except Exception as e:
        print(f"Error al guardar puntuación: {e}")

def cargar_puntuaciones_jugador(nombre_filtro=None):
    # Carga las puntuaciones del CSV, opcionalmente filtradas por jugador
    # Lee el archivo CSV si existe
    archivo = 'puntuaciones.csv'
    puntuaciones = []
    if os.path.isfile(archivo):
        try:
            with open(archivo, 'r') as f:
                reader = csv.DictReader(f)
                # Filtra por nombre si se especificó
                for row in reader:
                    if nombre_filtro:
                        # Solo incluye puntuaciones del jugador especificado
                        if row['Nombre'] == nombre_filtro:
                            puntuaciones.append(row)
                    else:
                        # Incluye todas las puntuaciones
                        puntuaciones.append(row)
        except Exception as e:
            print(f"Error al cargar puntuaciones: {e}")
    return puntuaciones
