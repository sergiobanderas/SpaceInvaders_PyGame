# CLAUDE.md

## Idioma

- **Código, nombres de variables, funciones, clases y comentarios del código: en inglés.**
- **Comunicación con Claude (respuestas, explicaciones y mensajes en el chat): en español.**

## Proyecto

Juego en Python con Pygame. Punto de entrada: `main.py`.

- `config.py`: constantes del juego (tamaño de ventana, FPS, colores, velocidades).
- `player.py`: clase `Player` (movimiento con flechas o WASD y dibujado).
- `obstacle.py`: clase `Obstacle` (aparición aleatoria, caída y dibujado).
- `powerup.py`: clase `PowerUp` (objetos especiales: velocidad, vida y escudo).

## Ejecución

```bash
pip install pygame
python main.py
```

## Convenciones

- Seguir PEP 8 en el código nuevo.
- Las constantes configurables van en `config.py`.
- Cada clase del juego en su propio módulo.

## Flujo de trabajo: retos

- Cada reto se implementa en **un único commit**.
- Cada reto añade su propia subsección `### Reto N — <título>` en la sección `## Retos` del `README.md`, explicando qué se ha hecho y cómo.
