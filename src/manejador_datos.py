# src/manejador_datos.py

import numpy as np
from generador_sudoku import generar_sudoku

def cargar_y_limpiar_datos(dificultad='medio'):
    """
    Genera un tablero de Sudoku programáticamente usando NumPy y Prolog.
    
    Args:
        dificultad: Nivel de dificultad ('facil', 'medio', 'dificil')
    
    Retorna:
        Tuple (Matriz Inicial, Matriz Solución) como objetos NumPy 9x9.
    """
    print(f"Generando tablero de Sudoku con dificultad: {dificultad}")
    
    # Genera un nuevo tablero usando el generador
    matriz_inicial, matriz_solucion = generar_sudoku(dificultad)
    
    if matriz_inicial is None:
        print("ERROR: No se pudo generar el tablero de Sudoku.")
        return None, None
    
    print("Tablero generado exitosamente.")
    return matriz_inicial, matriz_solucion