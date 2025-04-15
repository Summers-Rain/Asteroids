import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullet import Shot
from scoremanager import ScoreManager

def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Asteroids")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    

    Player.containers = (all_sprites, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (all_sprites, shots, updatable, drawable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroid_field = AsteroidField()
    score_manager = ScoreManager(player)

    updatable.add(score_manager)
    drawable.add(score_manager)

    dt = 0

    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        updatable.update(dt)

        for asteroid in asteroids:
            if not player.is_respawning and player.collision(asteroid):
                if player.respawn():
                    pass
                else:
                    print("Game Over!")
                    pygame.quit()
                    sys.exit()
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision(shot):
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

        for obj in drawable:
             obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()