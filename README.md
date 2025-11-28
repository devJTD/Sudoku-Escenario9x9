# 🎮 Sudoku Escenario 9x9

Un juego de Sudoku interactivo desarrollado en Python con Pygame, que implementa **programación multiparadigma** combinando programación funcional, orientada a objetos e imperativa, con validación lógica mediante Prolog.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Paradigmas de Programación](#-paradigmas-de-programación)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Características Técnicas](#-características-técnicas)
- [Contribuir](#-contribuir)

---

## ✨ Características

### Funcionalidades del Juego
- ✅ **Generación Automática de Tableros**: Tableros únicos generados mediante algoritmos de backtracking
- ✅ **Validación en Tiempo Real**: Validación de movimientos usando Prolog
- ✅ **Tres Niveles de Dificultad**: Fácil, Medio y Difícil
- ✅ **Sistema de Pistas**: Ayuda cuando te quedas atascado
- ✅ **Detección de Errores**: Resalta números incorrectos en rojo
- ✅ **Contador de Errores**: Límite de 10 errores antes de perder
- ✅ **Cronómetro**: Mide tu tiempo de resolución
- ✅ **Sistema de Puntuación**: Basado en tiempo, errores y pistas usadas
- ✅ **Historial de Partidas**: Guarda tus estadísticas en CSV
- ✅ **Interfaz Gráfica Intuitiva**: Diseñada con Pygame

### Controles del Juego
- 🖱️ **Clic Izquierdo**: Seleccionar celda
- ⌨️ **Números 1-9**: Colocar número en celda seleccionada
- ⌨️ **Backspace/Delete**: Borrar número de celda
- 🔘 **Botones**: Reiniciar, Nuevo Juego, Pista, Resolver, Menú

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una **arquitectura modular en capas** con separación de responsabilidades:

```
┌─────────────────────────────────────┐
│      Interfaz de Usuario (UI)      │  ← Pygame, Componentes Gráficos
├─────────────────────────────────────┤
│     Lógica de Negocio (Core)       │  ← Funciones Puras, Inmutabilidad
├─────────────────────────────────────┤
│    Validación Lógica (Prolog)      │  ← PySWIP, Reglas Declarativas
├─────────────────────────────────────┤
│   Persistencia de Datos (Data)     │  ← CSV, Gestión de Archivos
└─────────────────────────────────────┘
```

---

## 📦 Requisitos Previos

### Software Necesario

1. **Python 3.8 o superior**
   ```bash
   python --version
   ```

2. **SWI-Prolog** (para validación lógica)
   - **Windows**: Descarga desde [swi-prolog.org](https://www.swi-prolog.org/download/stable)
   - **Linux**: 
     ```bash
     sudo apt-get install swi-prolog
     ```
   - **macOS**: 
     ```bash
     brew install swi-prolog
     ```

3. **pip** (gestor de paquetes de Python)
   ```bash
   pip --version
   ```

---

## 🚀 Instalación

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Sudoku-Escenario9x9.git
cd Sudoku-Escenario9x9
```

### Paso 2: Crear Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Verificar Instalación de SWI-Prolog

```bash
swipl --version
```

Si no está en el PATH, añade la ruta de instalación a las variables de entorno.

---

## 🎮 Uso

### Ejecutar el Juego

```bash
python src/principal.py
```

### Flujo del Juego

1. **Menú Principal**
   - Ingresa tu nombre de usuario
   - Selecciona "Jugar" para iniciar
   - "Ver Puntuaciones" para ver tu historial
   - "Salir" para cerrar el juego

2. **Pantalla de Juego**
   - Selecciona una celda con el mouse
   - Ingresa números del 1-9 con el teclado
   - Usa los botones laterales para:
     - **Reiniciar**: Vuelve al estado inicial del tablero
     - **Nuevo Juego**: Genera un tablero completamente nuevo
     - **Pista**: Revela un número aleatorio
     - **Resolver**: Muestra la solución completa
     - **Menú**: Vuelve al menú principal

3. **Condiciones de Victoria/Derrota**
   - **Victoria**: Completa el tablero correctamente
   - **Derrota**: Comete 10 errores

---

## 📁 Estructura del Proyecto

```
Sudoku-Escenario9x9/
│
├── src/                          # Código fuente principal
│   ├── datos/                    # Capa de persistencia
│   │   ├── __init__.py          # Inicialización del módulo
│   │   ├── cargador_tableros.py # Generación de tableros
│   │   └── gestor_puntuaciones.py # Gestión de CSV
│   │
│   ├── interfaz/                 # Capa de presentación
│   │   ├── __init__.py          # Inicialización del módulo
│   │   ├── componentes_graficos.py # Botones, campos de texto
│   │   ├── constantes_visuales.py  # Colores, dimensiones
│   │   └── renderizador_juego.py   # Funciones de dibujo
│   │
│   ├── nucleo/                   # Lógica de negocio
│   │   ├── __init__.py          # Inicialización del módulo
│   │   ├── generador_tableros.py # Algoritmo de generación
│   │   ├── logica_sudoku.py     # Funciones puras
│   │   └── validacion_prolog.py # Integración con Prolog
│   │
│   ├── utilidades/               # Código compartido
│   │   ├── __init__.py          # Inicialización del módulo
│   │   └── estados_juego.py     # Constantes de estados
│   │
│   └── principal.py              # Punto de entrada del juego
│
├── assets/                       # Recursos gráficos (opcional)
│   ├── icono.png
│   ├── fondo_menu.jpg
│   └── titulo_logo.png
│
├── puntuaciones.csv              # Historial de partidas
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este archivo
```

### Descripción de Módulos

#### 📊 `datos/` - Persistencia
- **`cargador_tableros.py`**: Genera nuevos tableros de Sudoku
- **`gestor_puntuaciones.py`**: Lee/escribe puntuaciones en CSV

#### 🎨 `interfaz/` - Presentación
- **`componentes_graficos.py`**: Clases de UI (Botones, Campos de Texto)
- **`constantes_visuales.py`**: Configuración visual (colores, tamaños)
- **`renderizador_juego.py`**: Funciones de renderizado con Pygame

#### 🧠 `nucleo/` - Lógica de Negocio
- **`logica_sudoku.py`**: **Funciones puras** e inmutables
- **`generador_tableros.py`**: Algoritmo de backtracking
- **`validacion_prolog.py`**: Integración con SWI-Prolog

#### 🔧 `utilidades/` - Compartido
- **`estados_juego.py`**: Constantes de estados del juego

---

## 🧩 Paradigmas de Programación

Este proyecto implementa **programación multiparadigma**:

### 1. **Programación Funcional** 🔵
- **Funciones Puras**: No modifican estado externo
- **Inmutabilidad**: Uso de `.copy()` para evitar mutaciones
- **Ejemplos**:
  ```python
  # Función pura que retorna nueva matriz
  def colocar_numero(matriz, fila, columna, numero):
      nueva_matriz = matriz.copy()  # Inmutabilidad
      nueva_matriz[fila, columna] = numero
      return nueva_matriz  # No modifica la entrada
  ```

### 2. **Programación Lógica** 🟢
- **Prolog**: Validación declarativa de reglas de Sudoku
- **Ejemplos**:
  ```prolog
  % Regla: Número válido si no está en fila, columna ni bloque
  es_movimiento_valido(Matriz, Fila, Columna, Numero) :-
      valido_en_fila(Matriz, Fila, Numero),
      valido_en_columna(Matriz, Columna, Numero),
      valido_en_bloque(Matriz, Fila, Columna, Numero).
  ```

### 3. **Programación Orientada a Objetos** 🟡
- **Clases**: `BotonInteractivo`, `CampoTexto`
- **Encapsulación**: Estado y comportamiento juntos
- **Ejemplos**:
  ```python
  class BotonInteractivo:
      def __init__(self, x, y, texto, accion):
          self.rect = pygame.Rect(x, y, ancho, alto)
          self.accion = accion
      
      def manejar_evento(self, evento):
          if self.rect.collidepoint(evento.pos):
              self.accion()
  ```

### 4. **Programación Imperativa** 🔴
- **Bucles**: Iteración sobre matrices
- **Condicionales**: Lógica de control de flujo
- **Estado Mutable**: Solo en generación interna (backtracking)

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **Python** | 3.8+ | Lenguaje principal |
| **Pygame** | 2.0+ | Interfaz gráfica y eventos |
| **NumPy** | Latest | Manipulación eficiente de matrices |
| **PySWIP** | Latest | Integración Python-Prolog |
| **SWI-Prolog** | 8.0+ | Motor de inferencia lógica |
| **Pandas** | Latest | Procesamiento de datos CSV |

---

## 🔬 Características Técnicas

### Funciones Puras e Inmutabilidad

El módulo `nucleo/logica_sudoku.py` implementa **funciones puras**:

```python
# ✅ FUNCIÓN PURA
def colocar_numero(matriz, fila, columna, numero):
    # Crea una NUEVA matriz, no modifica la original
    nueva_matriz = matriz.copy()
    nueva_matriz[fila, columna] = numero
    return nueva_matriz  # Inmutabilidad garantizada

# ✅ FUNCIÓN PURA
def actualizar_errores(matriz_errores, fila, columna, es_error):
    # Retorna NUEVA matriz de errores
    nueva_matriz = matriz_errores.copy()
    nueva_matriz[fila, columna] = 1 if es_error else 0
    return nueva_matriz
```

**Beneficios**:
- ✅ Predecibilidad: Mismo input → mismo output
- ✅ Sin efectos secundarios
- ✅ Facilita testing y debugging
- ✅ Código más mantenible

### Validación con Prolog

Reglas declarativas para validar movimientos:

```prolog
% Verifica que el número no esté en la fila
valido_en_fila(Matriz, Fila, Numero) :-
    nth0(Fila, Matriz, FilaLista),
    \+ member(Numero, FilaLista).

% Verifica que el número no esté en la columna
valido_en_columna(Matriz, Columna, Numero) :-
    findall(Elem, (member(Fila, Matriz), nth0(Columna, Fila, Elem)), ColumnaLista),
    \+ member(Numero, ColumnaLista).
```

### Generación de Tableros

Algoritmo de **backtracking** con validación:

1. Genera tablero completo usando recursión
2. Remueve números según dificultad
3. Garantiza solución única

---

## 📊 Sistema de Puntuación

```
Puntaje = 10,000 - (Tiempo × 2) - (Errores × 100) - (Pistas × 200)
```

- **Tiempo**: Penaliza por cada segundo
- **Errores**: -100 puntos por error
- **Pistas**: -200 puntos por pista usada

---

## 🐛 Solución de Problemas

### Error: "No module named 'pyswip'"
```bash
pip install pyswip
```

### Error: "SWI-Prolog not found"
- Verifica que SWI-Prolog esté instalado
- Añade la ruta de instalación al PATH del sistema

### Error: "pygame.error: No available video device"
- Asegúrate de tener un entorno gráfico disponible
- En Linux, instala: `sudo apt-get install python3-pygame`

---

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **Tu Nombre** - *Desarrollo Inicial* - [Tu GitHub](https://github.com/tu-usuario)

---

## 🙏 Agradecimientos

- Pygame Community por la excelente documentación
- SWI-Prolog por el motor de inferencia lógica
- Comunidad de Python por las librerías utilizadas

---

## 📞 Contacto

- **Email**: tu-email@ejemplo.com
- **GitHub**: [@tu-usuario](https://github.com/tu-usuario)
- **LinkedIn**: [Tu Perfil](https://linkedin.com/in/tu-perfil)

---

**¡Disfruta jugando Sudoku! 🎮✨**
