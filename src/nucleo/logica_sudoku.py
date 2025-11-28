# src/nucleo/logica_sudoku.py

import numpy as np

# Tipo de dato para matrices de Sudoku (entero de 8 bits)
TIPO_MATRIZ = np.dtype('int8')

# FUNCIÓN PURA: Coloca un número en la matriz sin mutar el original
# Inmutabilidad: Usa .copy() para crear una nueva matriz, nunca modifica la entrada
# Pureza: Mismo input siempre produce mismo output, sin efectos secundarios
def colocar_numero(matriz: np.ndarray, fila: int, columna: int, numero: int) -> np.ndarray:
    # Valida los parámetros de entrada
    if not (0 <= fila < 9 and 0 <= columna < 9 and 0 <= numero <= 9):
        raise ValueError("Coordenadas o número fuera de rango.")
    
    # INMUTABILIDAD: Crea una copia para no modificar la matriz original
    nueva_matriz = matriz.copy()
    # Modifica solo la copia, preservando el estado original
    nueva_matriz[fila, columna] = numero
    # Retorna la nueva matriz (no modifica la entrada)
    return nueva_matriz

# FUNCIÓN PURA: Verifica si el número no se repite en la fila
# Pureza: Solo lee datos, no modifica nada, siempre retorna el mismo resultado
# Sin efectos secundarios: No altera estado externo ni la matriz de entrada
def es_valido_en_fila(matriz: np.ndarray, fila: int, numero: int) -> bool:
    return numero not in matriz[fila, :]

# FUNCIÓN PURA: Convierte posición del mouse a coordenadas de matriz
# Pureza: Transformación determinista sin efectos secundarios
# Mismo input (pos_mouse, offsets) siempre produce mismo output
def obtener_coordenadas_matriz(pos_mouse: tuple, offset_x: int, offset_y: int, tamano_celda: int) -> tuple:
    mouse_x, mouse_y = pos_mouse
    # Cálculos puros basados solo en los parámetros de entrada
    columna = (mouse_x - offset_x) // tamano_celda
    fila = (mouse_y - offset_y) // tamano_celda
    
    # Verifica si las coordenadas están dentro del rango válido
    if 0 <= fila < 9 and 0 <= columna < 9:
        return (int(fila), int(columna))
    else:
        return None

# FUNCIÓN PURA: Actualiza la matriz de errores para una celda específica
# Inmutabilidad: Crea y retorna una nueva matriz, no modifica la original
# Pureza: Determinista, sin efectos secundarios
def actualizar_errores(matriz_errores: np.ndarray, fila: int, columna: int, es_error: bool) -> np.ndarray:
    # INMUTABILIDAD: Crea una copia para preservar el estado original
    nueva_matriz = matriz_errores.copy()
    # Actualiza solo la copia
    nueva_matriz[fila, columna] = 1 if es_error else 0
    # Retorna nueva matriz sin mutar la entrada
    return nueva_matriz

# FUNCIÓN PURA: Verifica si el tablero está completo (sin ceros)
# Pureza: Solo lectura, no modifica datos, resultado determinista
def es_tablero_completo(matriz: np.ndarray) -> bool:
    return not np.any(matriz == 0)

# FUNCIÓN PURA: Verifica si el tablero cumple todas las reglas del Sudoku
# Pureza: Solo lectura de datos, sin mutaciones, resultado predecible
def es_tablero_valido(matriz: np.ndarray) -> bool:
    # Verifica filas (usa slicing que no modifica la matriz original)
    for i in range(9):
        fila = matriz[i, :]  # Slicing crea una vista, no modifica original
        if not es_grupo_valido(fila):
            return False
    # Verifica columnas
    for j in range(9):
        columna = matriz[:, j]  # Vista de solo lectura
        if not es_grupo_valido(columna):
            return False
            
    # Verifica bloques 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            bloque = matriz[i:i+3, j:j+3].flatten()  # Crea nueva vista
            if not es_grupo_valido(bloque):
                return False
                
    return True

# FUNCIÓN PURA: Verifica si un grupo contiene todos los dígitos del 1 al 9
# Pureza: Operación de solo lectura, sin efectos secundarios
def es_grupo_valido(grupo: np.ndarray) -> bool:
    # np.sort crea un nuevo array, no modifica el original
    return np.array_equal(np.sort(grupo), np.arange(1, 10))

# FUNCIÓN PURA: Retorna una copia de la matriz solución
# Inmutabilidad: Usa .copy() para evitar que el llamador modifique la solución original
# Pureza: Siempre retorna una copia nueva, sin efectos secundarios
def resolver_tablero(matriz_solucion: np.ndarray) -> np.ndarray:
    # INMUTABILIDAD: Retorna copia para proteger el estado original
    return matriz_solucion.copy()
