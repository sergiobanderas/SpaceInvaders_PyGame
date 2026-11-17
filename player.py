
import pygame
from config import *

class Player:
    """The player controlled by the user"""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        """Initialize the player with a position and size"""
        self.rect = pygame.Rect(x, y, 50, 50)
        self.start_position = (x, y)  # Remember the spawn point for restarts
        self.color = color
        self.speed = speed
        self.start_speed = speed  # Remember the initial speed for restarts
        self.lives = PLAYER_LIVES
        self.invulnerable_until = 0  # Game time (ms) until which the player cannot be hurt

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

    def reset_position(self):
        """Move the player back to its initial position"""
        self.rect.topleft = self.start_position

    def change_speed(self, amount):
        """Change the speed by the given amount, keeping it between the min and max limits"""
        self.speed = max(PLAYER_MIN_SPEED, min(PLAYER_MAX_SPEED, self.speed + amount))

    def reset_speed(self):
        """Restore the player's initial speed"""
        self.speed = self.start_speed

    def is_alive(self):
        """Return True while the player still has lives left"""
        return self.lives > 0

    def is_invulnerable(self, now):
        """Return True if the player cannot be hurt at the given game time"""
        return now < self.invulnerable_until

    def take_hit(self, now):
        """Lose a life unless invulnerable. Returns True if a life was lost"""
        if self.is_invulnerable(now):
            return False
        self.lives -= 1
        self.invulnerable_until = now + INVULNERABILITY_TIME
        return True

    def reset_lives(self):
        """Restore the initial lives and remove any invulnerability"""
        self.lives = PLAYER_LIVES
        self.invulnerable_until = 0

    def keep_inside_screen(self):
        """Clamp the player's rect so it never leaves the window"""
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, surface, now=0):
        """Draw the player on the given surface, blinking while invulnerable"""
        if self.is_invulnerable(now) and (now // BLINK_INTERVAL) % 2 == 0:
            return  # Skip drawing on alternate intervals to create a blink effect
        pygame.draw.rect(surface, self.color, self.rect)