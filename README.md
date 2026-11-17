# SpaceInvaders_PyGame

Juego arcade 2D desarrollado en Python con [Pygame](https://www.pygame.org/). Actualmente es un prototipo de esquivar obstáculos que servirá de base para un juego de tipo *shoot 'em up* espacial.

## Características

- Ventana de 800×600 a 60 FPS.
- **Dos jugadores** en el mismo teclado:
  - Jugador 1 (azul): se mueve con las **flechas**.
  - Jugador 2 (naranja): se mueve con **W A S D** (más lento).
- **Obstáculos** que caen desde la parte superior:
  - Aparecen cada 500 ms en una posición horizontal aleatoria.
  - Color y velocidad aleatorios.
  - Se eliminan al salir de la pantalla.
- **Puntuación**: +1 por cada obstáculo esquivado que sale de la pantalla.
- **Game Over** cuando el jugador 1 choca con un obstáculo.
- Configuración centralizada en `config.py` (tamaño, FPS, colores, velocidades, frecuencia de aparición).

## Estructura

| Archivo        | Descripción                                             |
|----------------|---------------------------------------------------------|
| `main.py`      | Inicialización, bucle principal, colisiones y HUD.      |
| `config.py`    | Constantes del juego.                                   |
| `player.py`    | Clase `Player`: movimiento (flechas / WASD) y dibujado. |
| `obstacle.py`  | Clase `Obstacle`: creación aleatoria, caída y dibujado. |

## Requisitos e instalación

- Python 3.8+
- Pygame

```bash
pip install pygame
python main.py
```

## Controles

| Acción                 | Jugador 1 | Jugador 2 |
|------------------------|-----------|-----------|
| Mover arriba/abajo     | ↑ / ↓     | W / S     |
| Mover izquierda/derecha| ← / →     | A / D     |
| Salir                  | Cerrar ventana | |

## Retos

### Reto 1 — Límites de pantalla

Los dos jugadores ya no pueden salir de la ventana por ninguno de los cuatro lados.

- Se añadió el método `Player.keep_inside_screen()`, que usa `self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))` para recolocar el rectángulo del jugador dentro de la pantalla.
- Se llama al final de `moveArrows()` y de `moveWASD()`, así que funciona para ambos jugadores.

### Reto 2 — Tamaños aleatorios

Cada obstáculo tiene ahora un tamaño aleatorio entre 20 y 70 píxeles.

- Se añadieron las constantes `OBSTACLE_MIN_SIZE` y `OBSTACLE_MAX_SIZE` en `config.py`.
- En `Obstacle.__init__()` el tamaño se calcula con `random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)`.
- La posición horizontal se sigue eligiendo con `random.randint(0, WIDTH - size)`, que usa el tamaño real del obstáculo, así que siempre aparece completamente dentro del ancho de la ventana.
