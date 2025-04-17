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
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Asteroids")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    MAIN_MENU = 0
    PLAYING = 1
    GAME_OVER = 2

    menu = MainMenu()

    current_state = MAIN_MENU
    clock = pygame.time.Clock()

    updatable = None
    drawable = None
    asteroids = None
    all_sprites = None
    shots = None
    player = None
    score_manager = None

    dt = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_state == GAME_OVER and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_state = MAIN_MENU

        if current_state == MAIN_MENU:
            continue_to_game = menu.main_menu(screen)

            if continue_to_game:
                updatable = pygame.sprite.Group()
                drawable = pygame.sprite.Group()
                asteroids = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                shots = pygame.sprite.Group()
                explosions = pygame.sprite.Group()

                Player.containers = (all_sprites, updatable, drawable)
                Asteroid.containers = (asteroids, updatable, drawable)
                AsteroidField.containers = (updatable,)
                Shot.containers = (all_sprites, shots, updatable, drawable)

                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                asteroid_field = AsteroidField()
                score_manager = ScoreManager(player)

                updatable.add(score_manager)
                drawable.add(score_manager)

                current_state = PLAYING

        elif current_state == PLAYING:

            updatable.update(dt)
            explosions.update()

            for asteroid in asteroids:
                if not player.is_respawning and player.collision(asteroid):
                    if player.respawn():
                        pass
                    else:
                        print("Game Over!")
                        current_state = GAME_OVER
        
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collision(shot):
                        explosion = Explosion(asteroid.rect.center, size_factor=asteroid.radius)
                        explosions.add(explosion)
                        asteroid.split()
                        shot.kill()

                        base_points = 0
                        if asteroid.radius > 30:
                            base_points = 50
                        elif asteroid.radius > 15:
                            base_points = 100
                        else:
                            base_points = 150

                        score_manager.add_points(base_points)
            screen.fill((0, 0, 0))
            explosions.draw(screen)

        elif current_state == GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            font = pygame.font.SysFont(None, 64)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            score_text = font.render(f"Score: {score_manager.score}", True, (255, 255, 255))

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 50))
            
            menu_text = font.render("Press SPACE to return to menu", True, (255, 255, 255))
            screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2,
                                    SCREEN_HEIGHT // 2 - menu_text.get_height() // 2 + 150))

        if current_state != MAIN_MENU:
            for obj in drawable:
                obj.draw(screen)

        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()