# src/main.py

import pygame
import sys
import numpy as np

# Importa módulos propios de la lógica de datos y el núcleo del juego
from manejador_datos import cargar_y_limpiar_datos
from logica_nucleo import TIPO_MATRIZ, obtener_coordenadas_matriz, colocar_numero, actualizar_errores, es_tablero_completo, es_tablero_valido

import logica_prolog
from logica_prolog import validar_numero_prolog

# --- CONFIGURACIÓN DE PYGAME (INTERFAZ DE USUARIO) ---
# Define las dimensiones de la ventana del juego (Ancho 1200, Alto 750)
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 750 
TITULO_JUEGO = "Escenario 9x9" # Título que se muestra en la barra de la ventana

# --- RUTAS DE ASSETS (IMÁGENES) ---
RUTA_ICONO = 'assets/icono.png'         # Ruta para el ícono de la ventana
RUTA_FONDO_MENU = 'assets/fondo_menu.jpg' # Ruta para la imagen de fondo del menú
RUTA_TITULO_IMAGEN = 'assets/titulo_logo.png' # Ruta para la imagen del título


# --- CONSTANTES DE COLOR ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Color para el fondo de la pantalla de menú (Negro)
COLOR_FONDO_MENU = NEGRO 

# Color para el fondo de la pantalla de juego (Gris Oscuro)
COLOR_FONDO_JUEGO = (50, 50, 50) 

# --- COLORES DE BOTONES ---
COLOR_JUGAR_BASE = (60, 120, 220)       # Azul (Color base)
COLOR_JUGAR_HOVER = (90, 150, 250)      # Azul (Color al pasar el ratón)
COLOR_SALIR_BASE = (255, 215, 0)        # Amarillo/Rubio (Color base)
COLOR_SALIR_HOVER = (255, 230, 80)      # Amarillo/Rubio (Color al pasar el ratón)

# --- COLORES DE BOTONES JUEGO ---
COLOR_REINICIAR_BASE = (220, 100, 60)   # Naranja
COLOR_REINICIAR_HOVER = (250, 130, 90)
COLOR_NUEVO_BASE = (60, 180, 100)       # Verde
COLOR_NUEVO_HOVER = (90, 210, 130)
COLOR_MENU_BASE = (100, 100, 200)       # Azul/Violeta
COLOR_MENU_HOVER = (130, 130, 230)

# --- ESTADOS DE JUEGO ---
ESTADO_MENU = "MENU"
ESTADO_JUEGO = "JUEGO"
ESTADO_VICTORIA = "VICTORIA"
ESTADO_SALIR = "SALIR"

# --- GESTIÓN DE ESTADOS ---
ESTADO_ACTUAL = ESTADO_MENU # Define el estado inicial del juego

# --- CONFIGURACIÓN DEL TABLERO ---
TAMANO_GRILLA = 540                 # Tamaño total en píxeles de la grilla 9x9
TAMANO_CELDA = TAMANO_GRILLA // 9   # Tamaño en píxeles de cada celda (60)
GROSOR_LINEA_FINA = 1               # Grosor de las líneas internas de la grilla
GROSOR_LINEA_GRUESA = 3             # Grosor de las líneas de separación de bloques (3x3)

# Calcula la posición X para centrar la grilla en la pantalla de 1200px de ancho
OFFSET_GRILLA_X = (ANCHO_PANTALLA - TAMANO_GRILLA) // 2 
OFFSET_GRILLA_Y = 150 

# --- COLORES DEL TABLERO (ESTILO) ---
COLOR_FIJO = (0, 0, 150)            # Azul oscuro para números iniciales
COLOR_GRILLA_FINA = (150, 150, 150) # Gris claro para líneas finas
COLOR_GRILLA_GRUESA = (0, 0, 0)     # Negro para líneas gruesas
COLOR_SELECCION = (100, 200, 255)   # Azul claro para la celda seleccionada
COLOR_ERROR = (255, 0, 0)           # Rojo para números inválidos

# --- CLASE DE BOTÓN BÁSICA ---
class Boton:
    """Representa un botón interactivo en la interfaz de Pygame."""
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_actual = color_base
        self.accion = accion
        self.fuente = pygame.font.Font(None, 48)

    def dibujar(self, pantalla):
        # Dibuja el rectángulo del botón con esquinas redondeadas (radio de 8)
        pygame.draw.rect(pantalla, self.color_actual, self.rect, 0, 8) 
        # Renderiza el texto del botón
        superficie_texto = self.fuente.render(self.texto, True, NEGRO)
        # Calcula la posición para centrar el texto dentro del botón
        posicion_texto = (
            self.rect.x + (self.rect.width - superficie_texto.get_width()) // 2,
            self.rect.y + (self.rect.height - superficie_texto.get_height()) // 2
        )
        pantalla.blit(superficie_texto, posicion_texto)

    def manejar_evento(self, evento):
        global ESTADO_ACTUAL
        # Cambia el color si el cursor está sobre el botón
        if evento.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(evento.pos):
                self.color_actual = self.color_hover
            else:
                self.color_actual = self.color_base
        
        # Ejecuta la acción asociada si se hace clic
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos) and self.accion:
                self.accion()

# --- FUNCIONES DE ACCIÓN ---
def iniciar_juego():
    """Cambia el estado global del juego a ESTADO_JUEGO."""
    global ESTADO_ACTUAL
    print("Transición a la pantalla de JUEGO.")
    ESTADO_ACTUAL = ESTADO_JUEGO

def salir_juego():
    """Cambia el estado global del juego a ESTADO_SALIR."""
    global ESTADO_ACTUAL
    print("Saliendo del juego.")
    ESTADO_ACTUAL = ESTADO_SALIR

# --- FUNCIONES DE RENDERIZADO ---

def dibujar_grilla(pantalla):
    """ Dibuja las líneas de la estructura del tablero de Sudoku 9x9. """
    
    # 1. Dibuja el fondo blanco del tablero principal
    pygame.draw.rect(
        pantalla, 
        BLANCO, 
        (OFFSET_GRILLA_X, OFFSET_GRILLA_Y, TAMANO_GRILLA, TAMANO_GRILLA)
    )
    
    # 2. Itera para dibujar las 10 líneas verticales y 10 horizontales
    for i in range(10): 
        # Determina si la línea es gruesa (cada 3 celdas) o fina
        grosor_linea = GROSOR_LINEA_GRUESA if i % 3 == 0 else GROSOR_LINEA_FINA
        color_linea = COLOR_GRILLA_GRUESA if i % 3 == 0 else COLOR_GRILLA_FINA
        
        # Líneas verticales
        posicion = OFFSET_GRILLA_X + i * TAMANO_CELDA
        pygame.draw.line(
            pantalla, 
            color_linea, 
            (posicion, OFFSET_GRILLA_Y), 
            (posicion, OFFSET_GRILLA_Y + TAMANO_GRILLA), 
            grosor_linea
        )
        
        # Líneas horizontales
        posicion = OFFSET_GRILLA_Y + i * TAMANO_CELDA
        pygame.draw.line(
            pantalla, 
            color_linea, 
            (OFFSET_GRILLA_X, posicion), 
            (OFFSET_GRILLA_X + TAMANO_GRILLA, posicion), 
            grosor_linea
        )

def dibujar_seleccion(pantalla, celda_seleccionada):
    """Dibuja un recuadro de selección sobre la celda activa."""
    if celda_seleccionada:
        fila, columna = celda_seleccionada
        x = OFFSET_GRILLA_X + columna * TAMANO_CELDA
        y = OFFSET_GRILLA_Y + fila * TAMANO_CELDA
        
        # Dibuja un rectángulo con borde grueso para resaltar la selección
        pygame.draw.rect(
            pantalla, 
            COLOR_SELECCION, 
            (x, y, TAMANO_CELDA, TAMANO_CELDA), 
            4 # Grosor del borde
        )

def dibujar_numeros(pantalla, matriz_actual, matriz_fija, matriz_errores):
    """ Renderiza los números contenidos en la matriz NumPy sobre la grilla. """
    fuente_numero = pygame.font.Font(None, 40)

    for fila in range(9):
        for columna in range(9):
            numero = matriz_actual[fila, columna]
            
            if numero != 0:
                # Determina si el número es fijo (parte del puzle inicial)
                es_fijo = matriz_fija[fila, columna] != 0
                es_error = matriz_errores[fila, columna] != 0
                
                if es_error:
                    color_texto = COLOR_ERROR
                elif es_fijo:
                    color_texto = COLOR_FIJO
                else:
                    color_texto = NEGRO
                
                texto_superficie = fuente_numero.render(str(numero), True, color_texto)
                
                # Calcula la posición para centrar el número en su celda
                pos_x = OFFSET_GRILLA_X + columna * TAMANO_CELDA + (TAMANO_CELDA - texto_superficie.get_width()) // 2
                pos_y = OFFSET_GRILLA_Y + fila * TAMANO_CELDA + (TAMANO_CELDA - texto_superficie.get_height()) // 2
                
                pantalla.blit(texto_superficie, (pos_x, pos_y))

def dibujar_victoria(pantalla):
    """Muestra una pantalla de victoria superpuesta."""
    # Fondo semitransparente
    superficie_transparente = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    superficie_transparente.set_alpha(200)
    superficie_transparente.fill(NEGRO)
    pantalla.blit(superficie_transparente, (0, 0))
    
    fuente_victoria = pygame.font.Font(None, 100)
    texto_victoria = fuente_victoria.render("¡FELICIDADES!", True, (0, 255, 0))
    texto_subtitulo = pygame.font.Font(None, 50).render("Has completado el Sudoku correctamente.", True, BLANCO)
    texto_instruccion = pygame.font.Font(None, 30).render("Haz clic para volver al menú", True, (200, 200, 200))
    
    # Centrar textos
    rect_victoria = texto_victoria.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 50))
    rect_sub = texto_subtitulo.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20))
    rect_inst = texto_instruccion.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 80))
    
    pantalla.blit(texto_victoria, rect_victoria)
    pantalla.blit(texto_subtitulo, rect_sub)
    pantalla.blit(texto_instruccion, rect_inst)

# --- FUNCIÓN DE EJECUCIÓN PRINCIPAL ---
def ejecutar_juego():
    """Función principal para inicializar y ejecutar el bucle del juego."""
    
    # 1. Inicialización de Pygame, ajuste de tamaño de ventana y título
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption(TITULO_JUEGO)
    
    # 2. Carga Condicional de ASSETS: ÍCONO
    # Intenta cargar la imagen del ícono. Si falla (archivo no encontrado o error de Pygame), usa el predeterminado.
    try:
        icono_imagen = pygame.image.load(RUTA_ICONO)
        pygame.display.set_icon(icono_imagen)
    except (FileNotFoundError, pygame.error):
        print(f"Advertencia: No se pudo cargar el ícono desde {RUTA_ICONO}. Usando el predeterminado.")
    
    # 3. Carga Condicional de ASSETS: FONDO MENÚ
    # Intenta cargar y escalar la imagen de fondo. Si falla, el fondo_menu_imagen será None.
    fondo_menu_imagen = None
    try:
        fondo_menu_imagen = pygame.image.load(RUTA_FONDO_MENU).convert()
        # Escala la imagen al tamaño de la pantalla
        fondo_menu_imagen = pygame.transform.scale(fondo_menu_imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except (FileNotFoundError, pygame.error):
        print(f"Advertencia: No se pudo cargar la imagen de fondo del menú desde {RUTA_FONDO_MENU}. Usando color negro.")
    
    # 4. Carga Condicional de ASSETS: TÍTULO IMAGEN
    # Intenta cargar la imagen del título. Si falla, titulo_imagen será None.
    titulo_imagen = None
    try:
        titulo_imagen = pygame.image.load(RUTA_TITULO_IMAGEN).convert_alpha()
    except (FileNotFoundError, pygame.error):
        print(f"Advertencia: No se pudo cargar la imagen de título desde {RUTA_TITULO_IMAGEN}. Usando renderizado de texto.")


    # 5. Carga y Preparación de Datos (Matriz de Sudoku)
    # Genera un tablero de Sudoku programáticamente
    matriz_inicial = cargar_y_limpiar_datos()
    
    if matriz_inicial is None:
        pygame.quit()
        sys.exit()

    # Crea dos copias: una para los números fijos y otra para el estado actual del juego
    matriz_fija = matriz_inicial.copy().astype(TIPO_MATRIZ)
    matriz_actual = matriz_inicial.copy().astype(TIPO_MATRIZ)
    
    # Inicializa la matriz de errores (0 = válido, 1 = error)
    matriz_errores = np.zeros((9, 9), dtype=TIPO_MATRIZ)
    
    print(f"Matriz de juego inicial cargada (NumPy):\n{matriz_actual}")

    # --- ESTADO DE SELECCIÓN ---
    celda_seleccionada = None # Tupla (fila, columna) o None

    # --- CREACIÓN Y POSICIONAMIENTO DE BOTONES ---
    ANCHO_BOTON = 250
    ALTO_BOTON = 70 
    ESPACIO_Y = 120
    # Posición X centrada para los botones
    POSICION_X_BOTON = (ANCHO_PANTALLA - ANCHO_BOTON) // 2

    # Posición Y inicial, ajustada para que los botones aparezcan más abajo
    POSICION_Y_INICIO = ALTO_PANTALLA // 2 + 50 

    boton_jugar = Boton(
        POSICION_X_BOTON, 
        POSICION_Y_INICIO,
        ANCHO_BOTON, ALTO_BOTON, "Jugar", 
        COLOR_JUGAR_BASE, COLOR_JUGAR_HOVER, iniciar_juego
    )

    boton_salir = Boton(
        POSICION_X_BOTON, 
        POSICION_Y_INICIO + ESPACIO_Y,
        ANCHO_BOTON, ALTO_BOTON, "Salir", 
        COLOR_SALIR_BASE, COLOR_SALIR_HOVER, salir_juego
    )

    botones_menu = [boton_jugar, boton_salir]

    # --- BOTONES DEL JUEGO ---
    def accion_reiniciar():
        nonlocal matriz_actual, matriz_errores
        matriz_actual = matriz_fija.copy().astype(TIPO_MATRIZ)
        matriz_errores = np.zeros((9, 9), dtype=TIPO_MATRIZ)
        print("Tablero reiniciado.")

    def accion_nuevo_juego():
        nonlocal matriz_actual, matriz_fija, matriz_errores, matriz_inicial
        nueva_matriz = cargar_y_limpiar_datos()
        if nueva_matriz is not None:
            matriz_inicial = nueva_matriz
            matriz_fija = matriz_inicial.copy().astype(TIPO_MATRIZ)
            matriz_actual = matriz_inicial.copy().astype(TIPO_MATRIZ)
            matriz_errores = np.zeros((9, 9), dtype=TIPO_MATRIZ)
            print("Nuevo juego generado.")

    def accion_volver_menu():
        global ESTADO_ACTUAL
        ESTADO_ACTUAL = ESTADO_MENU
        print("Regresando al menú.")

    # Configuración de posición para botones laterales
    X_BOTONES_JUEGO = 950
    Y_INICIO_BOTONES = 200
    ANCHO_BOTON_JUEGO = 200
    ALTO_BOTON_JUEGO = 60
    ESPACIO_BOTONES = 80

    boton_reiniciar = Boton(
        X_BOTONES_JUEGO, Y_INICIO_BOTONES, 
        ANCHO_BOTON_JUEGO, ALTO_BOTON_JUEGO, 
        "Reiniciar", COLOR_REINICIAR_BASE, COLOR_REINICIAR_HOVER, accion_reiniciar
    )
    
    boton_nuevo = Boton(
        X_BOTONES_JUEGO, Y_INICIO_BOTONES + ESPACIO_BOTONES, 
        ANCHO_BOTON_JUEGO, ALTO_BOTON_JUEGO, 
        "Nuevo Juego", COLOR_NUEVO_BASE, COLOR_NUEVO_HOVER, accion_nuevo_juego
    )

    boton_menu_juego = Boton(
        X_BOTONES_JUEGO, Y_INICIO_BOTONES + ESPACIO_BOTONES * 2, 
        ANCHO_BOTON_JUEGO, ALTO_BOTON_JUEGO, 
        "Menú", COLOR_MENU_BASE, COLOR_MENU_HOVER, accion_volver_menu
    )

    botones_juego = [boton_reiniciar, boton_nuevo, boton_menu_juego]

    # --- BUCLE PRINCIPAL DEL JUEGO (Pygame Loop) ---
    global ESTADO_ACTUAL
    while ESTADO_ACTUAL != ESTADO_SALIR: 
        
        # 3. Manejo de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ESTADO_ACTUAL = ESTADO_SALIR
            
            # Procesa eventos solo para los botones del menú si el juego está en ESTADO_MENU
            if ESTADO_ACTUAL == ESTADO_MENU:
                for boton in botones_menu:
                    boton.manejar_evento(evento)
            
            # Manejo de eventos en ESTADO_JUEGO
            elif ESTADO_ACTUAL == ESTADO_JUEGO:
                # Manejo de botones del juego
                for boton in botones_juego:
                    boton.manejar_evento(evento)

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Obtiene las coordenadas de la matriz usando la función pura
                    celda_seleccionada = obtener_coordenadas_matriz(
                        evento.pos, 
                        OFFSET_GRILLA_X, 
                        OFFSET_GRILLA_Y, 
                        TAMANO_CELDA
                    )

                if evento.type == pygame.KEYDOWN:
                    if celda_seleccionada:
                        fila, columna = celda_seleccionada
                        
                        # Verifica si la celda es editable (no es un número fijo)
                        if matriz_fija[fila, columna] == 0:
                            numero = None
                            
                            # Mapeo de teclas numéricas
                            if evento.key == pygame.K_1 or evento.key == pygame.K_KP1: numero = 1
                            elif evento.key == pygame.K_2 or evento.key == pygame.K_KP2: numero = 2
                            elif evento.key == pygame.K_3 or evento.key == pygame.K_KP3: numero = 3
                            elif evento.key == pygame.K_4 or evento.key == pygame.K_KP4: numero = 4
                            elif evento.key == pygame.K_5 or evento.key == pygame.K_KP5: numero = 5
                            elif evento.key == pygame.K_6 or evento.key == pygame.K_KP6: numero = 6
                            elif evento.key == pygame.K_7 or evento.key == pygame.K_KP7: numero = 7
                            elif evento.key == pygame.K_8 or evento.key == pygame.K_KP8: numero = 8
                            elif evento.key == pygame.K_9 or evento.key == pygame.K_KP9: numero = 9
                            elif evento.key == pygame.K_BACKSPACE or evento.key == pygame.K_DELETE: numero = 0
                            
                            if numero is not None:
                                try:
                                    # 1. Prepara una matriz temporal con la celda vacía para validar
                                    matriz_para_validar = colocar_numero(matriz_actual, fila, columna, 0)
                                    
                                    # 2. Validación en vivo con Prolog
                                    if numero != 0:
                                        es_valido = validar_numero_prolog(matriz_para_validar, fila, columna, numero)
                                        es_error = not es_valido
                                    else:
                                        es_error = False
                                    
                                    # 3. Actualización Inmutable
                                    matriz_actual = colocar_numero(matriz_actual, fila, columna, numero)
                                    
                                    # 4. Actualiza la matriz de errores
                                    matriz_errores = actualizar_errores(matriz_errores, fila, columna, es_error)
                                    
                                    # --- VERIFICACIÓN DE VICTORIA ---
                                    if not es_error and es_tablero_completo(matriz_actual):
                                        if es_tablero_valido(matriz_actual):
                                            print("¡VICTORIA! Tablero completado correctamente.")
                                            ESTADO_ACTUAL = ESTADO_VICTORIA
                                    
                                except ValueError as e:
                                    print(f"Error al colocar número: {e}")

            # Manejo de eventos en ESTADO_VICTORIA
            elif ESTADO_ACTUAL == ESTADO_VICTORIA:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    ESTADO_ACTUAL = ESTADO_MENU

        # 4. Lógica de Renderizado
        
        if ESTADO_ACTUAL == ESTADO_MENU:
            # Dibuja el fondo del menú
            if fondo_menu_imagen:
                pantalla.blit(fondo_menu_imagen, (0, 0))
            else:
                pantalla.fill(COLOR_FONDO_MENU) 
            
            # Dibuja el título
            if titulo_imagen:
                posicion_x = ANCHO_PANTALLA // 2 - titulo_imagen.get_width() // 2
                pantalla.blit(titulo_imagen, (posicion_x, 80)) 
            else:
                try:
                    fuente_titulo = pygame.font.Font(None, 80)
                    texto_titulo = fuente_titulo.render(TITULO_JUEGO, True, BLANCO)
                    posicion_x = ANCHO_PANTALLA // 2 - texto_titulo.get_width() // 2
                    pantalla.blit(texto_titulo, (posicion_x, 80))
                except:
                    pass

            # Dibuja los botones del menú
            for boton in botones_menu:
                boton.dibujar(pantalla)
            
        elif ESTADO_ACTUAL == ESTADO_JUEGO:
            # Dibuja el fondo del modo JUEGO
            pantalla.fill(COLOR_FONDO_JUEGO) 
            
            # Renderiza un título más pequeño
            try:
                fuente_titulo = pygame.font.Font(None, 40)
                texto_titulo = fuente_titulo.render(TITULO_JUEGO, True, BLANCO)
                posicion_x = ANCHO_PANTALLA // 2 - texto_titulo.get_width() // 2
                pantalla.blit(texto_titulo, (posicion_x, 30))
            except:
                pass
            
            # Dibuja el Tablero de Sudoku y los números
            dibujar_grilla(pantalla)
            dibujar_seleccion(pantalla, celda_seleccionada)
            dibujar_numeros(pantalla, matriz_actual, matriz_fija, matriz_errores)

            # Dibuja los botones del juego
            for boton in botones_juego:
                boton.dibujar(pantalla)

        elif ESTADO_ACTUAL == ESTADO_VICTORIA:
            # Dibuja el juego de fondo
            pantalla.fill(COLOR_FONDO_JUEGO)
            dibujar_grilla(pantalla)
            dibujar_numeros(pantalla, matriz_actual, matriz_fija, matriz_errores)
            # Superpone la pantalla de victoria
            dibujar_victoria(pantalla)

        # 5. Actualiza la pantalla
        pygame.display.flip()

    # Lógica de salida del juego
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    ejecutar_juego()