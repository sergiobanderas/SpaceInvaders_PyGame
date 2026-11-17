# CLAUDE.md

## Idioma

- **Código, nombres de variables, funciones, clases y comentarios del código: en inglés.**
- **Comunicación con Claude (respuestas, explicaciones y mensajes en el chat): en español.**

## Proyecto

Juego en Python con Pygame. Punto de entrada: `main.py`.

- `config.py`: constantes del juego (tamaño de ventana, FPS, colores, velocidades).
- `player.py`: clase `Player` (movimiento con flechas o WASD y dibujado).
- `obstacle.py`: clase `Obstacle` (aparición aleatoria, caída y dibujado).

## Ejecución

```bash
pip install pygame
python main.py
```

## Convenciones

- Seguir PEP 8 en el código nuevo.
- Las constantes configurables van en `config.py`.
- Cada clase del juego en su propio módulo.
