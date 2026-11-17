import pygame
from config import *
from player import Player
from obstacle import Obstacle

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Player Game")
clock = pygame.time.Clock()

# Create a player object
player = Player(375, 530)
player2 = Player(100, 100, PLAYER_COLOR2,2)  # Create a second player object

obstacles = [] # List to store obstacles

last_obstacle_spawn_time = pygame.time.get_ticks()  # Track the last time an obstacle was spawned

score = 0  # Initialize the score
game_over = False  # Initialize the game over state
paused = False  # Initialize the pause state
pause_start_time = 0  # Time when the current pause started

game_start_time = pygame.time.get_ticks()  # Time when the current game started
survival_time = 0  # Seconds the players have survived

font = pygame.font.Font(None, 36)   

# GAME LOOP
running = True  
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Toggle pause with ESC (only while the game is still running)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not game_over:
            paused = not paused
            if paused:
                pause_start_time = pygame.time.get_ticks()
            else:
                # Shift the spawn timer so the paused time does not count towards the next spawn
                paused_duration = pygame.time.get_ticks() - pause_start_time
                last_obstacle_spawn_time += paused_duration
                # Shift the game start time too, so the survival timer ignores the pause
                game_start_time += paused_duration
        # Restart the game with R after a game over
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            score = 0
            obstacles = []
            player.reset_position()
            player2.reset_position()
            last_obstacle_spawn_time = pygame.time.get_ticks()
            game_start_time = pygame.time.get_ticks()
            survival_time = 0
            game_over = False

    if not game_over and not paused:
        #OBSTACLES spawning logic
        current_time = pygame.time.get_ticks()

        # Survival timer: only updated while the game is running, so it freezes on pause and game over
        survival_time = (current_time - game_start_time) // 1000

        if current_time - last_obstacle_spawn_time > SPAWN_OBSTACLE_DELAY:
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = current_time

        # Update the position of each obstacle
        for obstacle in obstacles:
            obstacle.move()
            # The game ends if the obstacle hits either player
            if player.rect.colliderect(obstacle.rect) or player2.rect.colliderect(obstacle.rect):
                game_over = True

        # Remove obstacles that are off the screen
        visible_obstacles = []
        for obstacle in obstacles:
            if not obstacle.is_off_screen():
                visible_obstacles.append(obstacle)
            else :
                score += 1  # Increment the score for each obstacle that goes off screen
        obstacles = visible_obstacles


        # Update the player's position
        player.moveArrows()
        player2.moveWASD()  # Update the second player's position

    screen.fill(BACKGROUND_COLOR)  # Blue background
    player.draw(screen)  # Draw the player rectangle
    player2.draw(screen)  # Draw the second player rectangle
    
    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw each obstacle

    # Display the score
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display the survival time
    time_text = font.render(f"Time: {survival_time}s", True, (255, 255, 255))
    screen.blit(time_text, (10, 40))

    # Display the game over message if the game is over
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))

    # Display the pause message if the game is paused
    if paused:
        pause_text = font.render("PAUSE", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()