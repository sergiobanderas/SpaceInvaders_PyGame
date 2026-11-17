import pygame
from config import *
from player import Player
from obstacle import Obstacle
from powerup import PowerUp
from scores import top_scores, save_score

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
powerups = []  # List to store the power-ups falling on screen

# Game clock: milliseconds of real play. It only advances while the game is running,
# so pauses, menus and the game over screen never count towards any timer.
game_time = 0
last_obstacle_spawn_time = 0  # Game time when the last obstacle was spawned
last_powerup_spawn_time = 0  # Game time when the last power-up was spawned

score = 0  # Initialize the score
best_scores = top_scores()  # Top scores read from scores.txt when the game starts
high_score = best_scores[0][1] if best_scores else 0  # Best score ever saved (kept across restarts)
game_over = False  # Initialize the game over state
paused = False  # Initialize the pause state
entering_name = False  # True while the player types their name after a game over
player_name = ""  # Name being typed

survival_time = 0  # Seconds the players have survived

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 26)  # Used for the power-up letters and effect timers

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
                last_powerup_spawn_time = 0
        # Name entry after a game over: letters build the name, BACKSPACE deletes, ENTER saves
        elif entering_name:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    save_score(player_name.strip() or DEFAULT_PLAYER_NAME, score)
                    best_scores = top_scores()  # Reload so the new score appears in the ranking
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode.isprintable() and event.unicode not in ("", ";") and len(player_name) < MAX_NAME_LENGTH:
                    player_name += event.unicode  # ";" is not allowed because it separates name and score in the file
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
            powerups = []
            for each_player in (player, player2):
                each_player.reset_position()
                each_player.reset_lives()
                each_player.reset_effects()
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

        # POWER-UPS spawning logic
        if game_time - last_powerup_spawn_time > POWERUP_SPAWN_DELAY:
            powerups.append(PowerUp())
            last_powerup_spawn_time = game_time

        # Players that still have lives left
        alive_players = [p for p in active_players if p.is_alive()]

        # Remove temporary effects that have expired
        for alive_player in alive_players:
            alive_player.update_effects(game_time)

        # Move the power-ups and give their effect to the first player that touches them
        remaining_powerups = []
        for powerup in powerups:
            powerup.move()
            collector = None
            for alive_player in alive_players:
                if alive_player.rect.colliderect(powerup.rect):
                    collector = alive_player
                    break
            if collector:
                powerup.apply(collector, game_time)
            elif not powerup.is_off_screen():
                remaining_powerups.append(powerup)
        powerups = remaining_powerups

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
            entering_name = True  # Ask for the player's name before allowing a restart
            player_name = ""

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

        # Best saved scores, from highest to lowest
        ranking_y = HEIGHT // 2 + 70
        ranking_title = font.render(f"TOP {TOP_SCORES_COUNT}", True, (255, 215, 0))
        screen.blit(ranking_title, (WIDTH // 2 - ranking_title.get_width() // 2, ranking_y))
        if not best_scores:
            empty_text = small_font.render("No scores yet", True, (200, 200, 200))
            screen.blit(empty_text, (WIDTH // 2 - empty_text.get_width() // 2, ranking_y + 40))
        for position, (name, saved_score) in enumerate(best_scores, start=1):
            entry_text = small_font.render(f"{position}. {name}  {saved_score}", True, (255, 255, 255))
            screen.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, ranking_y + 10 + position * 28))
        pygame.display.flip()
        continue  # Skip the game drawing until the players are chosen

    for active_player in active_players:
        if active_player.is_alive():
            active_player.draw(screen, game_time)  # Draw each player that is still alive

    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw each obstacle

    for powerup in powerups:
        powerup.draw(screen, small_font)  # Draw each power-up

    # Display the score

    score_text = font.render(f"Score: {score}    High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display the survival time
    time_text = font.render(f"Time: {survival_time}s", True, (255, 255, 255))
    screen.blit(time_text, (10, 40))

    # Display player 1 speed
    speed_text = font.render(f"Speed: {player.current_speed()}", True, (255, 255, 255))
    screen.blit(speed_text, (10, 70))

    # Display the lives of each active player, in the player's color
    lives_y = 100
    for index, active_player in enumerate(active_players, start=1):
        lives_text = font.render(f"P{index} Lives: {active_player.lives}", True, active_player.color)
        screen.blit(lives_text, (10, lives_y))
        # Show the remaining seconds of each active temporary effect next to the lives
        effects = []
        if active_player.speed_boost:
            effects.append(f"SPEED {(active_player.speed_boost_until - game_time) // 1000 + 1}s")
        if active_player.has_shield(game_time):
            effects.append(f"SHIELD {(active_player.shield_until - game_time) // 1000 + 1}s")
        if effects:
            effects_text = small_font.render("  ".join(effects), True, active_player.color)
            screen.blit(effects_text, (lives_text.get_width() + 25, lives_y + 4))
        lives_y += 30

    # Display the game over message if the game is over
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        if entering_name:
            # Name input box with a blinking cursor
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            name_text = font.render(f"Enter your name: {player_name}{cursor}", True, (255, 255, 255))
            screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))
            hint_text = small_font.render("Press ENTER to save", True, (200, 200, 200))
            screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() + 40))
        else:
            restart_text = font.render("Press R to restart", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))

    # Display the pause message if the game is paused
    if paused:
        pause_text = font.render("PAUSE", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
