
import pygame
from config import *

class Player:
    """The player controlled by the user"""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        """Initialize the player with a position and size"""
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.speed = speed

    def moveArrows(self):
        """Update the player's position based on keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.keep_inside_screen()

    def moveWASD(self):
        """Update the player's position based on WASD keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.keep_inside_screen()

    def keep_inside_screen(self):
        """Clamp the player's rect so it never leaves the window"""
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, surface):
        """Draw the player on the given surface"""
        pygame.draw.rect(surface, self.color, self.rect)