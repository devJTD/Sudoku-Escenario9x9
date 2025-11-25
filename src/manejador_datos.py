# src/manejador_datos.py

import pandas as pd
import numpy as np
from generador_sudoku import generar_sudoku

def cargar_y_limpiar_datos(ruta_archivo=None, dificultad='medio'):
    """
    Genera un tablero de Sudoku programáticamente usando NumPy y Prolog.
    
    Args:
        ruta_archivo: (Opcional) Ruta a archivo CSV para compatibilidad futura
        dificultad: Nivel de dificultad ('facil', 'medio', 'dificil')
    
    Retorna:
        Matriz de Sudoku como un objeto NumPy 9x9.
    """
    print(f"Generando tablero de Sudoku con dificultad: {dificultad}")
    
    # Si se proporciona una ruta de archivo, intenta cargar desde CSV (compatibilidad futura)
    if ruta_archivo is not None:
        try:
            print(f"Intentando cargar desde archivo: {ruta_archivo}")
            df_tableros = pd.read_csv(ruta_archivo)
            
            # Define una función para convertir la cadena de 81 caracteres a una matriz
            def cadena_a_matriz(cadena):
                """Convierte la cadena de 81 caracteres a una matriz de NumPy 9x9."""
                cadena_limpia = cadena.replace('.', '0').replace(' ', '0')
                numeros = [int(c) for c in cadena_limpia]
                return np.array(numeros).reshape(9, 9)
            
            df_tableros['matriz_limpia'] = df_tableros['cadena_puzzle'].map(cadena_a_matriz)
            matriz_inicial = df_tableros['matriz_limpia'].iloc[0]
            print("Tablero cargado desde archivo CSV.")
            return matriz_inicial
            
        except (FileNotFoundError, KeyError, Exception) as e:
            print(f"No se pudo cargar desde archivo: {e}")
            print("Generando tablero programáticamente...")
    
    # Genera un nuevo tablero usando el generador
    matriz_inicial = generar_sudoku(dificultad)
    
    if matriz_inicial is None:
        print("ERROR: No se pudo generar el tablero de Sudoku.")
        return None
    
    print("Tablero generado exitosamente.")
    return matriz_inicial