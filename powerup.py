import pygame
import random

from config import *
from assets import load_image


class PowerUp:
    """A special item that falls down the screen and gives an effect to the player who picks it up"""

    SPEED = "speed"    # Temporary speed boost
    LIFE = "life"      # Recover one life
    SHIELD = "shield"  # Temporary invulnerability

    # Image shown for each kind of power-up
    IMAGES = {
        SPEED: SPEED_POWERUP_IMAGE,
        LIFE: LIFE_POWERUP_IMAGE,
        SHIELD: SHIELD_POWERUP_IMAGE,
    }

    def __init__(self):
        self.kind = random.choice(list(self.IMAGES))  # Random effect
        self.image = load_image(self.IMAGES[self.kind], POWERUP_SIZE)
        x = random.randint(0, WIDTH - self.image.get_width())
        self.rect = self.image.get_rect(bottomleft=(x, 0))  # Start just above the screen
        self.speed = POWERUP_FALL_SPEED

    def move(self):
        """Move the power-up down the screen"""
        self.rect.y += self.speed

    def is_off_screen(self):
        """Check if the power-up has moved off the screen"""
        return self.rect.y > HEIGHT

    def apply(self, player, now):
        """Give this power-up's effect to the player at the given game time"""
        if self.kind == self.SPEED:
            player.activate_speed_boost(now)
        elif self.kind == self.LIFE:
            player.add_life()
        elif self.kind == self.SHIELD:
            player.activate_shield(now)

    def draw(self, surface):
        """Draw the power-up image on the given surface"""
        surface.blit(self.image, self.rect)
