# src/nucleo/logica_sudoku.py

import numpy as np

# Tipo de dato para matrices de Sudoku (entero de 8 bits)
TIPO_MATRIZ = np.dtype('int8')

# Función pura: Coloca un número en la matriz sin mutar el original
def colocar_numero(matriz: np.ndarray, fila: int, columna: int, numero: int) -> np.ndarray:
    # Retorna una nueva matriz con el número colocado en (fila, columna)
    if not (0 <= fila < 9 and 0 <= columna < 9 and 0 <= numero <= 9):
        raise ValueError("Coordenadas o número fuera de rango.")
    
    nueva_matriz = matriz.copy()
    nueva_matriz[fila, columna] = numero
    return nueva_matriz

# Verifica si el número no se repite en la fila
def es_valido_en_fila(matriz: np.ndarray, fila: int, numero: int) -> bool:
    return numero not in matriz[fila, :]

# Convierte posición del mouse a coordenadas de matriz (fila, columna)
def obtener_coordenadas_matriz(pos_mouse: tuple, offset_x: int, offset_y: int, tamano_celda: int) -> tuple:
    mouse_x, mouse_y = pos_mouse
    columna = (mouse_x - offset_x) // tamano_celda
    fila = (mouse_y - offset_y) // tamano_celda
    
    # Verifica si las coordenadas están dentro del rango válido
    if 0 <= fila < 9 and 0 <= columna < 9:
        return (int(fila), int(columna))
    else:
        return None

# Actualiza la matriz de errores para una celda específica
def actualizar_errores(matriz_errores: np.ndarray, fila: int, columna: int, es_error: bool) -> np.ndarray:
    nueva_matriz = matriz_errores.copy()
    nueva_matriz[fila, columna] = 1 if es_error else 0
    return nueva_matriz

# Verifica si el tablero está completo (sin ceros)
def es_tablero_completo(matriz: np.ndarray) -> bool:
    return not np.any(matriz == 0)

# Verifica si el tablero cumple todas las reglas del Sudoku
def es_tablero_valido(matriz: np.ndarray) -> bool:
    # Verifica filas
    for i in range(9):
        fila = matriz[i, :]
        if not es_grupo_valido(fila):
            return False
    # Verifica columnas
    for j in range(9):
        columna = matriz[:, j]
        if not es_grupo_valido(columna):
            return False
            
    # Verifica bloques 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            bloque = matriz[i:i+3, j:j+3].flatten()
            if not es_grupo_valido(bloque):
                return False
                
    return True

def es_grupo_valido(grupo: np.ndarray) -> bool:
    # Verifica si un grupo contiene todos los dígitos del 1 al 9
    return np.array_equal(np.sort(grupo), np.arange(1, 10))

# Retorna una copia de la matriz solución
def resolver_tablero(matriz_solucion: np.ndarray) -> np.ndarray:
    return matriz_solucion.copy()
