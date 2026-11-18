
import pygame
from config import *
from assets import load_image

class Player:
    """The player controlled by the user"""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED, image_name=PLAYER_IMAGE):
        """Initialize the player with a position, a color for the HUD and a ship image"""
        self.image = load_image(image_name, PLAYER_WIDTH)
        self.rect = self.image.get_rect(topleft=(x, y))  # The rect takes the size of the image
        self.start_position = (x, y)  # Remember the spawn point for restarts
        self.color = color
        self.speed = speed
        self.start_speed = speed  # Remember the initial speed for restarts
        self.lives = PLAYER_LIVES
        self.invulnerable_until = 0  # Game time (ms) until which the player cannot be hurt
        self.shield_until = 0  # Game time (ms) until which the shield power-up protects the player
        self.speed_boost = 0  # Extra speed from the speed power-up
        self.speed_boost_until = 0  # Game time (ms) when the speed boost ends

    def moveArrows(self):
        """Update the player's position based on keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.current_speed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.current_speed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.current_speed()
        if keys[pygame.K_DOWN]:
            self.rect.y += self.current_speed()

        self.keep_inside_screen()

    def moveWASD(self):
        """Update the player's position based on WASD keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_a]:
            self.rect.x -= self.current_speed()
        if keys[pygame.K_d]:
            self.rect.x += self.current_speed()
        if keys[pygame.K_w]:
            self.rect.y -= self.current_speed()
        if keys[pygame.K_s]:
            self.rect.y += self.current_speed()

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
        return now < self.invulnerable_until or self.has_shield(now)

    def has_shield(self, now):
        """Return True while the shield power-up is active"""
        return now < self.shield_until

    def current_speed(self):
        """Base speed plus any temporary boost"""
        return self.speed + self.speed_boost

    def activate_speed_boost(self, now):
        """Temporarily increase the speed (speed power-up)"""
        self.speed_boost = SPEED_BOOST_AMOUNT
        self.speed_boost_until = now + POWERUP_DURATION

    def activate_shield(self, now):
        """Temporarily make the player invulnerable (shield power-up)"""
        self.shield_until = now + POWERUP_DURATION

    def add_life(self):
        """Recover one life, never going above the maximum (life power-up)"""
        self.lives = min(PLAYER_MAX_LIVES, self.lives + 1)

    def update_effects(self, now):
        """Remove temporary effects whose duration has finished"""
        if self.speed_boost and now >= self.speed_boost_until:
            self.speed_boost = 0
        # The shield needs no cleanup: has_shield() compares against shield_until every frame

    def reset_effects(self):
        """Remove every power-up effect"""
        self.speed_boost = 0
        self.speed_boost_until = 0
        self.shield_until = 0

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
        # Blink only for the post-hit invulnerability; the shield is shown with an outline instead
        if now < self.invulnerable_until and (now // BLINK_INTERVAL) % 2 == 0:
            return  # Skip drawing on alternate intervals to create a blink effect
        surface.blit(self.image, self.rect)  # Draw the ship image at the player's position
        if self.has_shield(now):
            pygame.draw.rect(surface, (255, 255, 255), self.rect.inflate(12, 12), 3)