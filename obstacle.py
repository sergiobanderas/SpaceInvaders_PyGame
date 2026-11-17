import pygame
import random

from config import *

class Obstacle:
    """An obstacle that the player must avoid"""

    def __init__(self):
        size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)  # Random size in pixels
        x = random.randint(0, WIDTH - size)
        self.rect = pygame.Rect(x, -size , size, size)
        self.color = random.choice(OBSTACLES_COLORS)  # Random color for the obstacle
        self.speed = random.randint(2, 7)  # Random speed for the obstacle

    def move(self):
        """Move the obstacle down the screen"""
        self.rect.y += self.speed

    def is_off_screen(self):
        """Check if the obstacle has moved off the screen"""
        return self.rect.y > HEIGHT

    def draw(self, surface):
        """Draw the obstacle on the given surface"""
        pygame.draw.rect(surface, self.color, self.rect)
