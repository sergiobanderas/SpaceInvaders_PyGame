# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background
PLAYER_COLOR = (60, 140, 255)  # Blue player
PLAYER_COLOR2 = (255, 140, 60)  # Orange player
PLAYER_SPEED = 6  # Speed of the player movement
PLAYER_MIN_SPEED = 2  # Minimum speed reachable with the - key
PLAYER_MAX_SPEED = 12  # Maximum speed reachable with the + key
PLAYER_SPEED_STEP = 1  # Speed change per key press

OBSTACLE_MIN_SIZE = 20  # Minimum obstacle size in pixels
OBSTACLE_MAX_SIZE = 70  # Maximum obstacle size in pixels

OBSTACLES_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

SPAWN_OBSTACLE_DELAY = 500 #milliseconds

# Increasing difficulty
POINTS_PER_DIFFICULTY_LEVEL = 10  # Every this many points the spawn rate increases
SPAWN_DELAY_DECREASE = 50  # Milliseconds removed from the spawn delay per level
MIN_SPAWN_OBSTACLE_DELAY = 150  # The spawn delay never goes below this value (milliseconds)
