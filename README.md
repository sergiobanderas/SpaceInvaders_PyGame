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
