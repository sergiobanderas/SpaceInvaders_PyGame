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

selecting_players = True  # The game starts on the player count selection screen
num_players = 1  # Number of players chosen in the selection screen (1 or 2)
active_players = []  # Players taking part in the current game

obstacles = [] # List to store obstacles

# Game clock: milliseconds of real play. It only advances while the game is running,
# so pauses, menus and the game over screen never count towards any timer.
game_time = 0
last_obstacle_spawn_time = 0  # Game time when the last obstacle was spawned

score = 0  # Initialize the score
high_score = 0  # Best score reached while the program is running (kept across restarts)
game_over = False  # Initialize the game over state
paused = False  # Initialize the pause state

survival_time = 0  # Seconds the players have survived

font = pygame.font.Font(None, 36)

# GAME LOOP
running = True
while running:
    dt = clock.tick(FPS)  # Milliseconds since the previous frame

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Player count selection screen: only the 1 and 2 keys are accepted
        elif selecting_players:
            if event.type == pygame.KEYDOWN and event.unicode in ("1", "2"):
                num_players = int(event.unicode)
                active_players = [player, player2] if num_players == 2 else [player]
                selecting_players = False
                # Start the game clock from zero when the game really begins
                game_time = 0
                last_obstacle_spawn_time = 0
        # Toggle pause with ESC (only while the game is still running)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not game_over:
            paused = not paused
        # Change player 1 speed with + and - (KEYDOWN fires once per press)
        elif event.type == pygame.KEYDOWN and not game_over and not paused:
            if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS) or event.unicode == "+":
                player.change_speed(PLAYER_SPEED_STEP)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS) or event.unicode == "-":
                player.change_speed(-PLAYER_SPEED_STEP)
        # Restart with R after a game over: reset everything and go back to the player count selection screen
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            score = 0
            obstacles = []
            for each_player in (player, player2):
                each_player.reset_position()
                each_player.reset_lives()
            player.reset_speed()
            survival_time = 0
            game_over = False
            selecting_players = True  # Timers restart when the new player count is chosen

    if not selecting_players and not game_over and not paused:
        game_time += dt  # Advance the game clock only while playing

        # Survival timer: only updated while the game is running, so it freezes on pause and game over
        survival_time = game_time // 1000

        # Increasing difficulty: every POINTS_PER_DIFFICULTY_LEVEL points the delay drops, down to a minimum
        difficulty_level = score // POINTS_PER_DIFFICULTY_LEVEL
        spawn_delay = max(MIN_SPAWN_OBSTACLE_DELAY, SPAWN_OBSTACLE_DELAY - difficulty_level * SPAWN_DELAY_DECREASE)

        #OBSTACLES spawning logic
        if game_time - last_obstacle_spawn_time > spawn_delay:
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = game_time

        # Players that still have lives left
        alive_players = [p for p in active_players if p.is_alive()]

        # Update the position of each obstacle
        for obstacle in obstacles:
            obstacle.move()
            # A hit costs one life; the invulnerability time prevents losing several lives at once
            for alive_player in alive_players:
                if alive_player.rect.colliderect(obstacle.rect):
                    alive_player.take_hit(game_time)

        # The game ends when every active player has run out of lives
        if not any(p.is_alive() for p in active_players):
            game_over = True

        # Remove obstacles that are off the screen
        visible_obstacles = []
        for obstacle in obstacles:
            if not obstacle.is_off_screen():
                visible_obstacles.append(obstacle)
            else :
                score += 1  # Increment the score for each obstacle that goes off screen
                high_score = max(high_score, score)  # Update the record if it was beaten
        obstacles = visible_obstacles


        # Update the position of the players that are still alive
        if player.is_alive():
            player.moveArrows()
        if num_players == 2 and player2.is_alive():
            player2.moveWASD()  # Update the second player's position

    screen.fill(BACKGROUND_COLOR)  # Blue background

    # Player count selection screen
    if selecting_players:
        title_text = font.render("Number of players?", True, (255, 255, 255))
        options_text = font.render("Press 1 or 2", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height()))
        screen.blit(options_text, (WIDTH // 2 - options_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()
        continue  # Skip the game drawing until the players are chosen

    for active_player in active_players:
        if active_player.is_alive():
            active_player.draw(screen, game_time)  # Draw each player that is still alive

    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw each obstacle

    # Display the score

    score_text = font.render(f"Score: {score}    High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display the survival time
    time_text = font.render(f"Time: {survival_time}s", True, (255, 255, 255))
    screen.blit(time_text, (10, 40))

    # Display player 1 speed
    speed_text = font.render(f"Speed: {player.speed}", True, (255, 255, 255))
    screen.blit(speed_text, (10, 70))

    # Display the lives of each active player, in the player's color
    lives_y = 100
    for index, active_player in enumerate(active_players, start=1):
        lives_text = font.render(f"P{index} Lives: {active_player.lives}", True, active_player.color)
        screen.blit(lives_text, (10, lives_y))
        lives_y += 30

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

# Quit Pygame
pygame.quit()
