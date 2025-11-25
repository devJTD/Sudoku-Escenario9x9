# src/logica_nucleo.py

import numpy as np

# Define el tipo de dato para las matrices de Sudoku (entero de 8 bits)
TIPO_MATRIZ = np.dtype('int8')

# Función Pura: Colocar un número (Garantizando Inmutabilidad)
def colocar_numero(matriz: np.ndarray, fila: int, columna: int, numero: int) -> np.ndarray:
    """
    Devuelve una NUEVA matriz con el número colocado en la posición (fila, columna).
    Asegura la inmutabilidad al trabajar sobre una copia de la matriz original.
    """
    # Verifica que las coordenadas y el número estén dentro de los rangos válidos
    if not (0 <= fila < 9 and 0 <= columna < 9 and 0 <= numero <= 9):
        raise ValueError("Coordenadas o número fuera de rango.")
    
    # Crea una copia de la matriz de entrada para evitar la mutación de datos
    nueva_matriz = matriz.copy()
    
    # Asigna el nuevo valor a la celda en la copia
    nueva_matriz[fila, columna] = numero
    
    # Retorna la nueva matriz con el cambio aplicado
    return nueva_matriz

# Funciones Puras Iniciales para la validación
def es_valido_en_fila(matriz: np.ndarray, fila: int, numero: int) -> bool:
    """Verifica si el número dado no se repite en la fila especificada de la matriz."""
    return numero not in matriz[fila, :]

# Función Pura: Mapeo de Coordenadas (Interacción UI)
def obtener_coordenadas_matriz(pos_mouse: tuple, offset_x: int, offset_y: int, tamano_celda: int) -> tuple:
    """
    Convierte la posición del mouse (x, y) en coordenadas de matriz (fila, columna).
    Retorna (fila, columna) si el clic es válido dentro de la grilla, o None si está fuera.
    """
    mouse_x, mouse_y = pos_mouse
    
    # Calcula la columna y fila relativas
    columna = (mouse_x - offset_x) // tamano_celda
    fila = (mouse_y - offset_y) // tamano_celda
    
    # Verifica si las coordenadas están dentro del rango 0-8
    if 0 <= fila < 9 and 0 <= columna < 9:
        return (int(fila), int(columna))
    else:
        return None

# Función Pura: Actualizar Matriz de Errores (Inmutabilidad)
def actualizar_errores(matriz_errores: np.ndarray, fila: int, columna: int, es_error: bool) -> np.ndarray:
    """
    Devuelve una NUEVA matriz de errores con el estado actualizado para la celda.
    """
    nueva_matriz = matriz_errores.copy()
    nueva_matriz[fila, columna] = 1 if es_error else 0
    return nueva_matriz

# Función Pura: Verificar si el tablero está completo (sin ceros)
def es_tablero_completo(matriz: np.ndarray) -> bool:
    """Retorna True si no hay ceros en la matriz."""
    return not np.any(matriz == 0)

# Función Pura: Verificar si el tablero es una solución válida de Sudoku
def es_tablero_valido(matriz: np.ndarray) -> bool:
    """
    Verifica si el tablero completo cumple con todas las reglas del Sudoku.
    Asume que el tablero está completo (sin ceros).
    """
    # Verificar filas
    for i in range(9):
        fila = matriz[i, :]
        if not es_grupo_valido(fila):
            return False
            
    # Verificar columnas
    for j in range(9):
        columna = matriz[:, j]
        if not es_grupo_valido(columna):
            return False
            
    # Verificar bloques 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            bloque = matriz[i:i+3, j:j+3].flatten()
            if not es_grupo_valido(bloque):
                return False
                
    return True

def es_grupo_valido(grupo: np.ndarray) -> bool:
    """Verifica si un grupo de 9 números contiene todos los dígitos del 1 al 9."""
    # Ordena el grupo y verifica si es igual a [1, 2, ..., 9]
    return np.array_equal(np.sort(grupo), np.arange(1, 10))