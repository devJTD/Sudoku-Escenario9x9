# src/manejador_datos.py

import pandas as pd
import numpy as np

def cargar_y_limpiar_datos(ruta_archivo):
    """
    Carga, procesa y transforma una cadena de Sudoku desde un archivo CSV.
    Retorna la primera matriz de Sudoku como un objeto NumPy 9x9.
    """
    print(f"Cargando datos desde: {ruta_archivo}")
    
    try:
        # Carga el archivo CSV en un DataFrame de Pandas
        df_tableros = pd.read_csv(ruta_archivo)
    except FileNotFoundError:
        print("ERROR: Archivo de datos no encontrado.")
        return None
    
    # Define una función para convertir la cadena de 81 caracteres a una matriz
    def cadena_a_matriz(cadena):
        """Convierte la cadena de 81 caracteres a una matriz de NumPy 9x9."""
        # Limpia la cadena, reemplazando caracteres vacíos ('.', ' ') por '0'
        cadena_limpia = cadena.replace('.', '0').replace(' ', '0')
        # Convierte los caracteres numéricos a enteros
        numeros = [int(c) for c in cadena_limpia]
        
        # Convierte la lista de 81 enteros en una matriz NumPy de 9x9
        return np.array(numeros).reshape(9, 9)

    # Aplica la función de limpieza y transformación a la columna 'cadena_puzzle'
    df_tableros['matriz_limpia'] = df_tableros['cadena_puzzle'].map(cadena_a_matriz)
    
    # Retorna la primera matriz procesada, lista para ser usada en el juego
    matriz_inicial = df_tableros['matriz_limpia'].iloc[0]
    return matriz_inicial