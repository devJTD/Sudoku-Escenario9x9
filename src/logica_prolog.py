# src/logica_prolog.py

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

# Configura las reglas inmediatamente al cargar el módulo
configurar_reglas_sudoku()

# Ejecuta la prueba de conexión inmediatamente al cargar el módulo
probar_conexion_prolog()