import pygame
import sys
from .constants import *
from src.entities.player import Player
from src.entities.asteroid import Asteroid
from src.entities.bullet import Shot
from src.entities.explosion import Explosion
from src.managers.asteroidfield import AsteroidField
from src.managers.scoremanager import ScoreManager
from src.ui.mainmenu import MainMenu

def main():
    # Initialize pygame modules
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Asteroids")

    # Create the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game state constants
    MAIN_MENU = 0
    PLAYING = 1
    GAME_OVER = 2

    # Create the main menu
    menu = MainMenu()

    # Set initial game state
    current_state = MAIN_MENU
    clock = pygame.time.Clock() # Clock for controlling frame rate

    # Initialize game objects as None
    player = None
    updatable = None # Group for objects that need to be updated
    drawable = None # Group for objects that need to be drawn
    asteroids = None
    all_sprites = None
    shots = None
    explosions = None
    asteroid_field = None
    score_manager = None

    dt = 0  # Delta time for frame rate independent movement

    # Main game loop
    running = True
    while running:
        dt = clock.tick(60) / 1000 # Get time since last frame in seconds

        # Process all game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Game over state event handling
            if current_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_state = MAIN_MENU # Return
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        # MAIN MENU state logic
        if current_state == MAIN_MENU:
            menu = MainMenu(score_manager)
            continue_to_game = menu.main_menu(screen)

            if continue_to_game:
                # Initialize all sprite groups
                updatable = pygame.sprite.Group()   # Objects that need update() called
                drawable = pygame.sprite.Group()    # Objects that need draw() called
                asteroids = pygame.sprite.Group()   # All asteroid objects
                all_sprites = pygame.sprite.Group() # All game entities
                shots = pygame.sprite.Group()       # Player bullets
                explosions = pygame.sprite.Group()  # Explosion animations

                # Set container groups for each entity type
                # This allows new instances to automatically be added to the right groups
                Player.containers = (all_sprites, updatable, drawable)
                Asteroid.containers = (asteroids, updatable, drawable)
                AsteroidField.containers = (updatable,)
                Shot.containers = (all_sprites, shots, updatable, drawable)

                # Create game objects
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)    # Player ship at center
                asteroid_field = AsteroidField()                        # manages asteroid spawning
                score_manager = ScoreManager(player)                    # Tracks score and lives

                # Add score manager to appropriate groups
                updatable.add(score_manager)
                drawable.add(score_manager)

                # Reset score for a new game
                score_manager.reset_score()

                # Change state to playing
                current_state = PLAYING

        # PLAYING state logic
        elif current_state == PLAYING:
            updatable.update(dt)    # Update all game objects
            explosions.update()     # Update explosion animations

            screen.fill((0, 0, 0))  # Clear screen with black background

            # Collision detection: player vs asteroids
            for asteroid in asteroids:
                # Check if player is vulnerable to hits (not dead and not respawning)
                if not player.is_dead and not player.is_respawning and player.collision(asteroid):
                    # Create explosion at player position
                    player_explosion = Explosion(player.position.copy(), size_factor=PLAYER_EXPLOSION_SIZE)
                    explosions.add(player_explosion)
                    if player.respawn():
                        pass
                    else:
                        score_manager.update_high_score() # Update highscore based on current score
                        current_state = GAME_OVER
        
            # Collision detection: bullets vs asteroids
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collision(shot):
                        # Create explosion at asteroid position
                        explosion = Explosion(asteroid.rect.center, size_factor=asteroid.radius)
                        explosions.add(explosion)
                        asteroid.split() # Split asteroid into smaller pieces
                        shot.kill()      # Remove bullet

                        # Award points based on asteroid size
                        base_points = 0
                        if asteroid.radius > 30:
                            base_points = 50        # Large asteroid
                        elif asteroid.radius > 15:
                            base_points = 100       # Medium asteroid
                        else:
                            base_points = 150       # Small asteroid

                        score_manager.add_points(base_points)

            explosions.draw(screen) # Draw all active explosions

             # Draw respawn countdown if player is dead but has lives left
            if player.is_dead and player.lives >= 0:
                #Calculate seconds left until respawn
                elapsed = (pygame.time.get_ticks() - player.death_timer) / 1000
                respawn_seconds_left = max(0, int(RESPAWN_DELAY - elapsed))

                if elapsed < RESPAWN_DELAY:
                    # Create and position respawn timer text
                    font = pygame.font.SysFont(None, 48)
                    respawn_text = font.render(f"Respawning in: {respawn_seconds_left}", True, (255, 0, 0))

                    # Position text in center of screen
                    text_x = SCREEN_WIDTH // 2 - respawn_text.get_width() // 2
                    text_y = SCREEN_HEIGHT // 2 - respawn_text.get_height() // 2

                    # Draw the text to the screen
                    screen.blit(respawn_text, (text_x, text_y)) # Display countdown to player

        # GAME OVER state logic
        elif current_state == GAME_OVER:
            # Handle events even when game is over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # player clicked the window close button
                    running = False             # Exit the main game loop
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Player pressed Escape
                    running = False             # Exit the main game loop
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Player pressed Space
                    current_state = MAIN_MENU # Change state back to main menu

            # Create font for text rendering
            font = pygame.font.SysFont(None, 64) # Default system font at size 64

            # Render the "Game Over" text in red
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            # Render the player's findal score in white
            score_text = font.render(f"Score: {score_manager.score}", True, (255, 255, 255))
            # Render the high score in white
            high_score_text = font.render(f"High Score: {score_manager.high_score}", True, (255, 255, 255))

            # Position and draw the "Game Over" text centered but slightly above center
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
            # Position and draw the score text centered but slightly below center
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 50))
            # Position and draw the high score text below the score text
            screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - high_score_text.get_height() // 2 + 100))
            
            # Check if a new high score was achieved and display a special message
            if score_manager.new_high_score_achieved:
                # Create a pulsing/flashing effect by using time
                flash_speed = 500 # miliseconds
                flash_on = (pygame.time.get_ticks() % (flash_speed * 2)) < flash_speed

                if flash_on:
                    # Create a celebratory message in a bright color
                    high_score_msg_font = pygame.font.SysFont(None, 64)
                    high_score_msg = high_score_msg_font.render("NEW HIGH SCORE!", True, (255, 215, 0))

                    # Position it above the high score display
                    screen.blit(high_score_msg, (SCREEN_WIDTH // 2 - high_score_msg.get_width() // 2, 
                                                 SCREEN_HEIGHT // 2 - 150))
            
            # Render instructions to return to main menu
            menu_text = font.render("Press SPACE to return to menu", True, (255, 255, 255))
            # Position and draw the menu instrcutions text well below center
            screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2,
                                    SCREEN_HEIGHT // 2 - menu_text.get_height() // 2 + 150))
        
        # For states other than MAIN_MENU draw all drawable objects
        if current_state != MAIN_MENU:
            for obj in drawable:
                obj.draw(screen) # Call draw method on each game object
        pygame.display.flip()    # Update the full display Surface to the screen
    
    pygame.quit()   # Clean up pygame resources when game loop exits
    sys.exit()      # Exit the program completely