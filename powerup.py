import pygame
import random

from config import *


class PowerUp:
    """A special item that falls down the screen and gives an effect to the player who picks it up"""

    SPEED = "speed"    # Temporary speed boost
    LIFE = "life"      # Recover one life
    SHIELD = "shield"  # Temporary invulnerability

    # Color and letter shown for each kind of power-up
    STYLES = {
        SPEED: ((255, 215, 0), "S"),
        LIFE: ((0, 220, 90), "L"),
        SHIELD: ((180, 180, 255), "I"),
    }

    def __init__(self):
        self.kind = random.choice(list(self.STYLES))  # Random effect
        self.color, self.letter = self.STYLES[self.kind]
        x = random.randint(0, WIDTH - POWERUP_SIZE)
        self.rect = pygame.Rect(x, -POWERUP_SIZE, POWERUP_SIZE, POWERUP_SIZE)
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

    def draw(self, surface, font):
        """Draw the power-up as a circle with its letter, so it looks different from the square obstacles"""
        pygame.draw.circle(surface, self.color, self.rect.center, POWERUP_SIZE // 2)
        letter_text = font.render(self.letter, True, (0, 0, 0))
        surface.blit(letter_text, letter_text.get_rect(center=self.rect.center))
