# src/interfaz/componentes_graficos.py
import pygame
from interfaz.constantes_visuales import NEGRO

class BotonInteractivo:
    # Botón con efectos hover y acción al hacer clic
    
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, accion=None):
        # Inicializa las propiedades del botón
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_actual = color_base
        self.accion = accion
        self.fuente = pygame.font.Font(None, 48)

    def dibujar(self, pantalla):
        # Dibuja el botón con bordes redondeados
        pygame.draw.rect(pantalla, self.color_actual, self.rect, 0, 8) 
        # Renderiza y centra el texto
        superficie_texto = self.fuente.render(self.texto, True, NEGRO)
        posicion_texto = (
            self.rect.x + (self.rect.width - superficie_texto.get_width()) // 2,
            self.rect.y + (self.rect.height - superficie_texto.get_height()) // 2
        )
        pantalla.blit(superficie_texto, posicion_texto)

    def manejar_evento(self, evento):
        # Cambia el color cuando el mouse está sobre el botón
        if evento.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(evento.pos):
                self.color_actual = self.color_hover
            else:
                self.color_actual = self.color_base
        
        # Ejecuta la acción cuando se hace clic
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos) and self.accion:
                self.accion()

class CampoTexto:
    # Campo de texto editable para entrada del usuario
    
    def __init__(self, x, y, ancho, alto, texto=''):
        # Inicializa las propiedades del campo de texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_inactivo = pygame.Color('lightskyblue3')
        self.color_activo = pygame.Color('dodgerblue2')
        self.color = self.color_inactivo
        self.texto = texto
        self.fuente = pygame.font.Font(None, 32)
        self.txt_surface = self.fuente.render(texto, True, self.color)
        self.activo = False

    def manejar_evento(self, evento):
        # Maneja eventos de mouse y teclado, retorna el texto actualizado o None
        texto_actualizado = None
        
        # Activa/desactiva el campo al hacer clic
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.activo = not self.activo
            else:
                self.activo = False
            self.color = self.color_activo if self.activo else self.color_inactivo
        
        # Procesa entrada de teclado si el campo está activo
        if evento.type == pygame.KEYDOWN:
            if self.activo:
                # Enter desactiva el campo
                if evento.key == pygame.K_RETURN:
                    self.activo = False
                    self.color = self.color_inactivo
                # Backspace borra el último carácter
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    # Añade el carácter si no excede el límite
                    if len(self.texto) < 15:
                        self.texto += evento.unicode
                
                # Actualiza la superficie de texto
                self.txt_surface = self.fuente.render(self.texto, True, self.color)
                texto_actualizado = self.texto
                
        return texto_actualizado
                
    def dibujar(self, pantalla):
        # Dibuja el texto y el borde del campo
        pantalla.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(pantalla, self.color, self.rect, 2)
