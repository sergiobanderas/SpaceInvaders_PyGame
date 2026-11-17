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
- **Pausa** con la tecla ESC.
- **Tiempo de supervivencia** en segundos, que se congela en pausa y en Game Over.
- **Game Over** cuando cualquiera de los dos jugadores choca con un obstáculo.
- **Reinicio** de la partida con la tecla R tras el Game Over.
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
| Pausar / continuar     | ESC       | ESC       |
| Reiniciar (en Game Over) | R       | R         |
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

### Reto 3 — Colisión del segundo jugador

La partida termina ahora cuando un obstáculo golpea a **cualquiera** de los dos jugadores.

- En el bucle de actualización de obstáculos de `main.py`, la condición de colisión pasa a ser `player.rect.colliderect(obstacle.rect) or player2.rect.colliderect(obstacle.rect)`.
- Se actualizó la lista de características para reflejar el nuevo comportamiento.

### Reto 4 — Pausar el juego

Al pulsar **ESC** el juego se detiene y aparece el mensaje **PAUSE** en el centro de la pantalla. Al pulsar ESC de nuevo, continúa.

- Nueva variable `paused` en `main.py`, que se alterna en el evento `KEYDOWN` con `pygame.K_ESCAPE` (solo si la partida no ha terminado).
- La lógica de actualización solo se ejecuta si `not game_over and not paused`, por lo que durante la pausa los jugadores no se mueven, los obstáculos no caen y no aparecen nuevos.
- Se guarda el instante de inicio de la pausa (`pause_start_time`) y, al reanudar, se suma el tiempo pausado a `last_obstacle_spawn_time`. Así el temporizador de aparición no "cuenta" el tiempo en pausa y no surge un obstáculo justo al continuar.
- El mensaje se dibuja tras el resto de elementos, de modo que el jugador sigue viendo la escena congelada.

### Reto 5 — Reiniciar la partida

Cuando aparece **Game Over**, se muestra el aviso *Press R to restart*. Al pulsar **R** empieza una nueva partida sin cerrar el programa.

- `Player` guarda su posición inicial en `self.start_position` y tiene un nuevo método `reset_position()` que la restaura con `self.rect.topleft = self.start_position`.
- En `main.py`, el evento `KEYDOWN` con `pygame.K_r` (solo si `game_over` es verdadero):
  - pone la puntuación a cero,
  - vacía la lista de obstáculos,
  - devuelve a los dos jugadores a su posición inicial,
  - reinicia el temporizador de aparición de obstáculos,
  - y vuelve a poner `game_over = False`.

### Reto 6 — Tiempo de supervivencia

Debajo de la puntuación se muestra `Time: Ns`, los segundos que llevan sobreviviendo los jugadores.

- Nueva variable `game_start_time`, con el instante (`pygame.time.get_ticks()`) en que empezó la partida.
- `survival_time = (current_time - game_start_time) // 1000` se calcula **solo dentro del bloque de actualización** (`not game_over and not paused`), así que el valor mostrado se congela automáticamente en Game Over.
- Al salir de la pausa, el tiempo pausado se suma también a `game_start_time`, de modo que el contador continúa donde se quedó en lugar de saltar.
- Al reiniciar con R, `game_start_time` vuelve al instante actual y `survival_time` a cero.
