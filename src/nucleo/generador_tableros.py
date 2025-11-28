# src/nucleo/generador_tableros.py

import numpy as np
import random
from nucleo.logica_sudoku import TIPO_MATRIZ
from nucleo.validacion_prolog import validar_numero_prolog

def es_valido_python(matriz, fila, col, num):
    # Valida si un número puede colocarse en una posición (fallback de Prolog)
    # Verifica fila
    if num in matriz[fila, :]:
        return False
    
    # Verifica columna
    if num in matriz[:, col]:
        return False
    
    # Calcula el inicio del bloque 3x3
    fila_bloque = (fila // 3) * 3
    col_bloque = (col // 3) * 3
    # Extrae el bloque 3x3 correspondiente
    bloque = matriz[fila_bloque:fila_bloque + 3, col_bloque:col_bloque + 3]
    # Verifica el bloque 3x3
    if num in bloque:
        return False
    
    return True

def resolver_sudoku(matriz):
    # Resuelve un tablero de Sudoku usando backtracking
    # NOTA: Esta función MODIFICA la matriz de entrada (no es pura)
    # Se usa para generación interna, no para lógica de juego del usuario
    # Busca la primera celda vacía
    for fila in range(9):
        for col in range(9):
            # Si encuentra una celda vacía
            if matriz[fila, col] == 0:
                # Intenta números del 1 al 9
                for num in range(1, 10):
                    # Valida con Prolog primero
                    if validar_numero_prolog(matriz, fila, col, num):
                        # MUTACIÓN CONTROLADA: Modifica la matriz para backtracking
                        matriz[fila, col] = num
                        
                        # Recursivamente intenta resolver el resto
                        if resolver_sudoku(matriz):
                            return True
                        
                        # BACKTRACKING: Deshace el cambio si no funcionó
                        matriz[fila, col] = 0
                    # Si Prolog falla, usa validación Python
                    elif es_valido_python(matriz, fila, col, num):
                        matriz[fila, col] = num
                        
                        if resolver_sudoku(matriz):
                            return True
                        
                        # BACKTRACKING: Restaura el estado anterior
                        matriz[fila, col] = 0
                
                # Si ningún número funciona, retorna False
                return False
    
    # Si no hay celdas vacías, el tablero está resuelto
    return True

def generar_tablero_completo():
    # Genera un tablero de Sudoku 9x9 completo y válido usando backtracking
    print("\n" + "-"*60)
    print("[TABLERO] Iniciando generación de tablero completo...")
    print("-"*60)
    # Crea una matriz vacía
    matriz = np.zeros((9, 9), dtype=TIPO_MATRIZ)
    
    # Función auxiliar para llenar el tablero recursivamente
    # NOTA: Esta función interna MODIFICA 'matriz' (closure sobre variable externa)
    # Esto es aceptable porque es parte del proceso de generación interno
    def llenar_tablero(fila, col):
        # Si llegamos al final, terminamos
        if fila == 9:
            return True
        
        # Calcula la siguiente posición
        siguiente_fila = fila if col < 8 else fila + 1
        siguiente_col = (col + 1) % 9
        
        # Crea una lista de números aleatorios del 1 al 9
        numeros = list(range(1, 10))
        random.shuffle(numeros)
        
        # Intenta cada número
        for num in numeros:
            # Valida con Prolog primero
            if validar_numero_prolog(matriz, fila, col, num):
                # MUTACIÓN CONTROLADA: Modifica la matriz durante la generación
                matriz[fila, col] = num
                
                # Recursivamente llena el resto del tablero
                if llenar_tablero(siguiente_fila, siguiente_col):
                    return True
                
                # BACKTRACKING: Deshace el cambio si falla
                matriz[fila, col] = 0
            # Fallback a validación Python
            elif es_valido_python(matriz, fila, col, num):
                matriz[fila, col] = num
                
                if llenar_tablero(siguiente_fila, siguiente_col):
                    return True
                
                # BACKTRACKING: Restaura el estado
                matriz[fila, col] = 0
        
        # Si ningún número funciona, retrocede
        return False
    
    # Inicia el llenado desde la posición (0, 0)
    if llenar_tablero(0, 0):
        print("[SUCCESS] Tablero completo generado exitosamente")
        return matriz
    else:
        print("[ERROR] No se pudo generar el tablero")
        return None

def crear_puzzle(tablero_completo, dificultad='medio'):
    # Crea un puzzle removiendo números de un tablero completo según la dificultad
    # Define cuántos números remover
    niveles_dificultad = {
        'facil': (35, 40),    # 35-40 números removidos
        'medio': (45, 50),    # 45-50 números removidos
        'dificil': (55, 60)   # 55-60 números removidos
    }
    
    # Obtiene el rango de números a remover
    if dificultad not in niveles_dificultad:
        print(f"[WARNING] Dificultad '{dificultad}' no reconocida. Usando 'medio'")
        dificultad = 'medio'
    
    # Calcula cuántos números remover
    min_remover, max_remover = niveles_dificultad[dificultad]
    num_remover = random.randint(min_remover, max_remover)
    
    print(f"[TABLERO] Creando puzzle - Dificultad: {dificultad.upper()}")
    print(f"[TABLERO] Números a remover: {num_remover}")
    
    # INMUTABILIDAD: Crea una copia para no modificar el tablero completo original
    puzzle = tablero_completo.copy()
    
    # Crea una lista de todas las posiciones (81 celdas) y las mezcla
    posiciones = [(fila, col) for fila in range(9) for col in range(9)]
    random.shuffle(posiciones)
    
    # Remueve números de posiciones aleatorias
    removidos = 0
    for fila, col in posiciones:
        # Si ya se removieron suficientes números, termina
        if removidos >= num_remover:
            break
        
        # Guarda el valor original (no usado actualmente)
        valor_original = puzzle[fila, col]
        
        # Remueve el número (lo pone en 0)
        puzzle[fila, col] = 0
        removidos += 1
    
    print(f"[SUCCESS] Puzzle creado con {removidos} números removidos")
    return puzzle

def generar_sudoku(dificultad='medio'):
    # Genera un puzzle de Sudoku completo con la dificultad especificada
    # Genera un tablero completo
    tablero_completo = generar_tablero_completo()

    # Muestra la solución en consola para depuración
    if tablero_completo is not None:
        print("\n" + "="*60)
        print("[DEBUG] TABLERO COMPLETO (SOLUCIÓN):")
        print("="*60)
        print(tablero_completo)
        print("="*60 + "\n")
    
    # Si falla la generación, retorna None
    if tablero_completo is None:
        return None
    
    # Crea el puzzle removiendo números
    puzzle = crear_puzzle(tablero_completo, dificultad)
    
    # Retorna el puzzle y la solución
    return puzzle, tablero_completo
