# SpaceInvaders_PyGame

Juego arcade 2D desarrollado en Python con [Pygame](https://www.pygame.org/). Actualmente es un prototipo de esquivar obstáculos que servirá de base para un juego de tipo *shoot 'em up* espacial.

## Características

- Ventana de 800×600 a 60 FPS.
- **Pantalla inicial** para elegir **1 o 2 jugadores**.
- Hasta **dos jugadores** en el mismo teclado:
  - Jugador 1 (azul): se mueve con las **flechas**.
  - Jugador 2 (naranja): se mueve con **W A S D** (más lento).
- **Obstáculos** que caen desde la parte superior:
  - Aparecen inicialmente cada 500 ms en una posición horizontal aleatoria.
  - Color y velocidad aleatorios.
  - Se eliminan al salir de la pantalla.
- **Puntuación**: +1 por cada obstáculo esquivado que sale de la pantalla.
- **Pausa** con la tecla ESC.
- **Tiempo de supervivencia** en segundos, que se congela en pausa y en Game Over.
- **Dificultad progresiva**: cada 10 puntos los obstáculos aparecen 50 ms antes (mínimo 150 ms).
- **Velocidad ajustable** del jugador 1 con + y − (entre 2 y 12).
- **Récord de puntuación** (*High Score*) que se conserva entre partidas.
- **Ranking guardado en `scores.txt`**: al terminar se pide el nombre y la pantalla inicial muestra el TOP 5.
- **Sistema de vidas**: cada jugador tiene 3 vidas y 2 s de invulnerabilidad (parpadeo) tras cada impacto.
- **Power-ups** cada 8 s: velocidad temporal (S), vida extra (L) o escudo de invulnerabilidad (I).
- **Game Over** cuando todos los jugadores activos se quedan sin vidas.
- **Reinicio** de la partida con la tecla R tras el Game Over.
- Configuración centralizada en `config.py` (tamaño, FPS, colores, velocidades, frecuencia de aparición).

## Estructura

| Archivo        | Descripción                                             |
|----------------|---------------------------------------------------------|
| `main.py`      | Inicialización, bucle principal, colisiones y HUD.      |
| `config.py`    | Constantes del juego.                                   |
| `player.py`    | Clase `Player`: movimiento (flechas / WASD) y dibujado. |
| `obstacle.py`  | Clase `Obstacle`: creación aleatoria, caída y dibujado. |
| `powerup.py`   | Clase `PowerUp`: objetos especiales y sus efectos.      |
| `scores.py`    | Lectura y guardado de récords en `scores.txt`.          |

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
| Velocidad + / −        | + / −     | —         |
| Elegir jugadores (inicio) | 1 / 2  | —         |
| Escribir nombre (fin)  | Teclado + ENTER | — |
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

Cuando aparece **Game Over**, se muestra el aviso *Press R to restart*. Al pulsar **R** empieza una nueva partida sin cerrar el programa (desde el Reto 10, pasando antes por la pantalla de selección de jugadores).

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

### Reto 7 — Dificultad progresiva

Cada 10 puntos los obstáculos aparecen con más frecuencia: el intervalo de aparición se reduce 50 ms por nivel, sin bajar nunca de 150 ms.

| Puntos  | Intervalo |
|---------|-----------|
| 0–9     | 500 ms    |
| 10–19   | 450 ms    |
| 20–29   | 400 ms    |
| …       | …         |
| 70 o más| 150 ms    |

- Nuevas constantes en `config.py`: `POINTS_PER_DIFFICULTY_LEVEL = 10`, `SPAWN_DELAY_DECREASE = 50` y `MIN_SPAWN_OBSTACLE_DELAY = 150`.
- En cada fotograma, `main.py` calcula:
  - `difficulty_level = score // POINTS_PER_DIFFICULTY_LEVEL`
  - `spawn_delay = max(MIN_SPAWN_OBSTACLE_DELAY, SPAWN_OBSTACLE_DELAY - difficulty_level * SPAWN_DELAY_DECREASE)`
- `max()` garantiza el límite inferior de 150 ms.
- Como el intervalo se deriva directamente de la puntuación, al reiniciar con R (puntuación a cero) la dificultad vuelve sola al nivel inicial.

### Reto 8 — Cambiar velocidad

El jugador 1 aumenta su velocidad con **+** y la reduce con **−**, siempre entre 2 y 12. La velocidad actual se muestra en pantalla como `Speed: N`.

- Nuevas constantes en `config.py`: `PLAYER_MIN_SPEED = 2`, `PLAYER_MAX_SPEED = 12` y `PLAYER_SPEED_STEP = 1`.
- Nuevo método `Player.change_speed(amount)`, que limita el resultado con `max(PLAYER_MIN_SPEED, min(PLAYER_MAX_SPEED, self.speed + amount))`.
- En `main.py` se usa el evento `KEYDOWN`, que se dispara **una sola vez por pulsación** (a diferencia de `key.get_pressed()`, que seguiría sumando mientras la tecla esté mantenida).
- Se aceptan `K_PLUS`/`K_MINUS`, las teclas del teclado numérico (`K_KP_PLUS`/`K_KP_MINUS`) y también el carácter escrito (`event.unicode`), para que funcione con distintas distribuciones de teclado.
- Solo se puede cambiar mientras se juega (no en pausa ni en Game Over).
- Al reiniciar con R, `Player.reset_speed()` devuelve al jugador su velocidad inicial.

### Reto 9 — Récord de puntuación

Junto a la puntuación actual se muestra el récord: `Score: N    High Score: M`.

- Nueva variable `high_score` en `main.py`, inicializada a cero al arrancar el programa.
- Cada vez que la puntuación sube, se actualiza con `high_score = max(high_score, score)`.
- El reinicio con R pone `score` a cero pero **no** toca `high_score`, así que el récord se conserva entre partidas.
- El récord vive en memoria: se pierde al cerrar el programa.

### Reto 10 — Elegir número de jugadores al empezar

Al arrancar, el juego muestra la pantalla *Number of players? — Press 1 or 2*. Solo se aceptan las teclas **1** y **2**; según la elección aparecen uno o dos jugadores.

- Nuevas variables en `main.py`:
  - `selecting_players`: indica si estamos en la pantalla de selección.
  - `num_players`: número de jugadores elegido.
  - `active_players`: lista con los jugadores que participan (`[player]` o `[player, player2]`).
- Mientras `selecting_players` es verdadero, solo se procesan las teclas 1/2 (se comprueba `event.unicode`, así funcionan tanto la fila de números como el teclado numérico). No funcionan la pausa ni el cambio de velocidad.
- Al elegir, se ponen en marcha los temporizadores de aparición y de supervivencia, para que el tiempo pasado en el menú no cuente.
- Las colisiones, el dibujado y el reinicio recorren `active_players`, y `player2.moveWASD()` solo se llama si hay dos jugadores. Así, en modo de un jugador, el jugador 2 ni se ve ni puede chocar.
- La pantalla de selección hace `continue` tras dibujarse, de modo que no se muestra el HUD hasta que empieza la partida.
- Al reiniciar con R se vuelve a la pantalla de selección, de modo que se puede cambiar el número de jugadores en cada partida.

### Reto 11 — Sistema de vidas

Cada jugador empieza con **3 vidas**. Un impacto le quita una vida en lugar de terminar la partida, y después tiene **2 segundos de invulnerabilidad** (el jugador parpadea) para no perder varias vidas con la misma colisión. La partida termina cuando **todos** los jugadores activos se quedan sin vidas; el jugador que se queda sin vidas desaparece mientras el otro sigue jugando.

- Nuevas constantes en `config.py`: `PLAYER_LIVES = 3`, `INVULNERABILITY_TIME = 2000` y `BLINK_INTERVAL = 100`.
- Nuevos atributos y métodos en `Player`:
  - `lives` e `invulnerable_until` (instante de juego hasta el que no recibe daño).
  - `is_alive()`, `is_invulnerable(now)`, `take_hit(now)` (resta una vida solo si no es invulnerable) y `reset_lives()`.
  - `draw(surface, now)` se salta el dibujado en intervalos alternos mientras es invulnerable, creando el parpadeo.
- En `main.py`, solo los jugadores vivos se mueven, se dibujan y pueden chocar. El marcador muestra `P1 Lives` / `P2 Lives` en el color de cada jugador.
- **Reloj de juego (`game_time`)**: se sustituye `pygame.time.get_ticks()` por un contador propio que suma el `dt` de `clock.tick(FPS)` **solo mientras se está jugando**. Así la invulnerabilidad, la aparición de obstáculos y el tiempo de supervivencia se detienen solos en pausa, menú y Game Over, y ya no hace falta desplazar cada temporizador al reanudar (simplifica lo hecho en los retos 4 y 6).
- Al reiniciar con R se restauran las vidas de ambos jugadores.

### Reto 12 — Objetos especiales (power-ups)

Cada 8 segundos de juego cae un objeto especial (un círculo con una letra, para distinguirlo de los obstáculos cuadrados). El primer jugador vivo que lo toca recibe su efecto:

| Objeto | Color    | Efecto                                                          |
|--------|----------|-----------------------------------------------------------------|
| **S**  | Amarillo | +4 de velocidad durante 5 s.                                    |
| **L**  | Verde    | Recupera una vida (máximo 5).                                   |
| **I**  | Lila     | Escudo: invulnerable durante 5 s (contorno blanco alrededor).   |

- Nueva clase `PowerUp` en el archivo independiente `powerup.py`, con `move()`, `is_off_screen()`, `draw()` y `apply(player, now)`, que aplica el efecto según su tipo (`SPEED`, `LIFE` o `SHIELD`, elegido al azar).
- Nuevas constantes en `config.py`: `POWERUP_SPAWN_DELAY`, `POWERUP_SIZE`, `POWERUP_FALL_SPEED`, `POWERUP_DURATION`, `SPEED_BOOST_AMOUNT` y `PLAYER_MAX_LIVES`.
- Cambios en `Player`:
  - `current_speed()` = velocidad base + `speed_boost`; el movimiento usa ahora esta velocidad.
  - `activate_speed_boost(now)`, `activate_shield(now)`, `add_life()` y `reset_effects()`.
  - `is_invulnerable(now)` también tiene en cuenta el escudo (`has_shield(now)`).
- **Los efectos temporales desaparecen solos**: cada fotograma se llama a `update_effects(game_time)`, que elimina el aumento de velocidad cuando pasa su duración; el escudo se compara directamente con `shield_until`. Como usan `game_time`, el tiempo de los efectos no corre durante la pausa.
- El marcador muestra junto a las vidas los segundos que quedan de cada efecto (`SPEED 3s`, `SHIELD 2s`), y `Speed:` muestra la velocidad real incluyendo el aumento.
- Al reiniciar se eliminan los power-ups de la pantalla y los efectos de los jugadores.

### Reto 13 — Guardar récords en fichero

Los récords se guardan en el archivo `scores.txt`. Al terminar cada partida se pide el nombre del jugador con una entrada de texto hecha en Pygame, y la pantalla inicial muestra las **5 mejores puntuaciones** de mayor a menor.

- Nuevo módulo `scores.py`:
  - `load_scores()` lee el fichero (una línea `nombre;puntos` por partida), ignora líneas mal formadas y devuelve la lista ordenada de mayor a menor con `sort(key=..., reverse=True)`.
  - `top_scores()` devuelve las 5 primeras.
  - `save_score(name, score)` añade una línea al final del fichero (modo `"a"`).
  - La ruta se calcula a partir de la carpeta de `scores.py`, así el fichero se encuentra aunque el juego se lance desde otra carpeta.
- Nuevas constantes en `config.py`: `SCORES_FILE`, `TOP_SCORES_COUNT`, `MAX_NAME_LENGTH` y `DEFAULT_PLAYER_NAME`.
- **Entrada de texto en Pygame** (estado `entering_name` en `main.py`):
  - Cada `KEYDOWN` añade `event.unicode` al nombre (máximo 12 caracteres; el `;` no se admite porque separa nombre y puntos en el fichero).
  - BACKSPACE borra el último carácter y ENTER guarda la puntuación. Si el nombre está vacío se guarda como `Player`.
  - Se dibuja un cursor parpadeante. Mientras se escribe, la tecla R escribe una "r" en lugar de reiniciar; el aviso *Press R to restart* aparece tras guardar.
- Al iniciar el juego se lee el fichero y la pantalla de selección de jugadores muestra el **TOP 5**. Tras guardar se vuelve a leer, así que la nueva puntuación aparece en el ranking al volver a esa pantalla.
- El **High Score** del Reto 9 se inicializa ahora con la mejor puntuación del fichero, de modo que se conserva también entre ejecuciones.
- `scores.txt` se añade a `.gitignore`, ya que son datos locales de cada equipo.
