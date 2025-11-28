# src/nucleo/validacion_prolog.py

from pyswip import Prolog
import numpy as np

# Inicialización del motor de Prolog
motor_prolog = Prolog()

def configurar_reglas_sudoku():
    """
    Define y carga las reglas básicas del Sudoku en el motor de Prolog.
    Actualmente, carga reglas simples para probar la conectividad PySWIP.
    """
    # Predicados de prueba: es_amigo(Persona1, Persona2)
    motor_prolog.assertz("es_amigo(juan, maria)")
    motor_prolog.assertz("es_amigo(juan, pedro)")
    
    print("Reglas básicas de Prolog cargadas.")

def probar_conexion_prolog():
    """
    Verifica la comunicación entre Python (PySWIP) y el motor de Prolog.
    Ejecuta una consulta simple para encontrar amigos de 'juan'.
    """
    print("\n--- Prueba de Conexión Prolog ---")
    
    try:
        # Ejecuta la consulta 'es_amigo(juan, Amigo)'
        consulta = motor_prolog.query("es_amigo(juan, Amigo)")
        
        resultados = []
        for res in consulta:
            amigo = res["Amigo"]
    
            # Decodifica la respuesta de bytes a string si es necesario
            if isinstance(amigo, bytes):
                amigo = amigo.decode('utf-8')
    
            resultados.append(amigo)
        
        if resultados:
            print(f"Conexión exitosa. Amigos encontrados para Juan: {resultados}")
            return True
        else:
            print("ERROR: La consulta a Prolog no retornó resultados. Revisa la instalación de SWI-Prolog y variables de entorno.")
            return False
            
    except Exception as e:
        print(f"ERROR CRÍTICO en PySWIP/Prolog: {e}")
        print("Asegúrate que SWI-Prolog está instalado y accesible en la ruta del sistema.")
        return False

# --- Funciones de Conversión de Datos ---

def matriz_numpy_a_lista(matriz_numpy: np.ndarray) -> list:
    """Convierte la matriz de NumPy (9x9) a una lista de listas de Python nativo."""
    return matriz_numpy.tolist()

def lista_a_matriz_numpy(lista_de_listas: list, tipo_matriz) -> np.ndarray:
    """Convierte una lista de listas de Python a una matriz de NumPy con el tipo de dato especificado."""
    return np.array(lista_de_listas, dtype=tipo_matriz)

# --- Funciones de Validación de Sudoku ---

def configurar_reglas_sudoku_validacion():
    """
    Define las reglas de Prolog para validar movimientos en Sudoku.
    Estas reglas verifican si un número puede colocarse en una posición específica.
    """
    
    # Regla: Verificar si un número NO está en una fila específica
    motor_prolog.assertz("""
        valido_en_fila(Matriz, Fila, Numero) :-
            nth0(Fila, Matriz, FilaLista),
            \\+ member(Numero, FilaLista)
    """)
    
    # Regla: Verificar si un número NO está en una columna específica
    motor_prolog.assertz("""
        valido_en_columna(Matriz, Columna, Numero) :-
            findall(Elem, (member(Fila, Matriz), nth0(Columna, Fila, Elem)), ColumnaLista),
            \\+ member(Numero, ColumnaLista)
    """)
    
    # Regla: Verificar si un número NO está en el bloque 3x3
    motor_prolog.assertz("""
        valido_en_bloque(Matriz, Fila, Columna, Numero) :-
            FilaBloque is Fila // 3,
            ColumnaBloque is Columna // 3,
            FilaInicio is FilaBloque * 3,
            ColumnaInicio is ColumnaBloque * 3,
            findall(Elem,
                (between(0, 2, I),
                 between(0, 2, J),
                 FilaActual is FilaInicio + I,
                 ColumnaActual is ColumnaInicio + J,
                 nth0(FilaActual, Matriz, FilaLista),
                 nth0(ColumnaActual, FilaLista, Elem)),
                BloqueLista),
            \\+ member(Numero, BloqueLista)
    """)
    
    # Regla: Combina las tres validaciones
    motor_prolog.assertz("""
        es_movimiento_valido(Matriz, Fila, Columna, Numero) :-
            valido_en_fila(Matriz, Fila, Numero),
            valido_en_columna(Matriz, Columna, Numero),
            valido_en_bloque(Matriz, Fila, Columna, Numero)
    """)
    
    print("Reglas de validación de Sudoku cargadas en Prolog.")

def validar_numero_prolog(matriz, fila, col, num):
    """
    Interfaz Python para validar si un número puede colocarse en una posición.
    
    Args:
        matriz: Matriz NumPy 9x9 del tablero actual
        fila: Índice de fila (0-8)
        col: Índice de columna (0-8)
        num: Número a validar (1-9)
    
    Returns:
        bool: True si el movimiento es válido, False en caso contrario
    """
    try:
        # Convierte la matriz NumPy a lista de listas para Prolog
        matriz_lista = matriz_numpy_a_lista(matriz)
        
        # Construye la consulta Prolog
        consulta = f"es_movimiento_valido({matriz_lista}, {fila}, {col}, {num})"
        
        # Ejecuta la consulta
        resultado = list(motor_prolog.query(consulta))
        
        # Si hay resultados, el movimiento es válido
        return len(resultado) > 0
        
    except Exception as e:
        print(f"Error en validación Prolog: {e}")
        # En caso de error, retorna False por seguridad
        return False

# Configura las reglas inmediatamente al cargar el módulo
configurar_reglas_sudoku()
configurar_reglas_sudoku_validacion()

# Ejecuta la prueba de conexión inmediatamente al cargar el módulo
probar_conexion_prolog()
