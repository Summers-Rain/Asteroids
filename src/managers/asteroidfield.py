import pygame
import random
from src.entities.asteroid import Asteroid
from src.constants import *


class AsteroidField(pygame.sprite.Sprite):
    # Define possible spawn edges with corresponding velocity direction and position generator
    # Each edge is a list containing:
    # 1. A direction vector pointing inward from the edge
    # 2. A function that generates a position along that edge based on a 0-1 parameter
    edges = [
        # Left edge: velocity points right (1,0), position is off left side of screen
        [
            pygame.Vector2(1, 0), # Direction: moving right
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT), # Position: left of screen
        ],
        # Right edge: velocity points left (-1,0), position is off right side of screen
        [
            pygame.Vector2(-1, 0), # Direction: moving left
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ), # Position: right of screen
        ],
        # Top edge: velocity points down (0,1), position is off top of screen
        [
            pygame.Vector2(0, 1), # Direction: moving down
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS), # Position: above screen
        ],
        # Bottom edge: velocity points up (0,-1), position is off bottom of screen
        [
            pygame.Vector2(0, -1), # Direction: moving up
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ), # Position: below screen
        ],
    ]

    def __init__(self):
        # Initialize the sprite and add it to its container groups
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0 # Timer to track when to spawn new asteroids

    def spawn(self, radius, position, velocity):
        # Create a new asteroid with the given parameters
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity # Set the asteroid's velocity
        return asteroid # Return the new asteroid object

    def update(self, dt):
        # Update the spawn timer with the time that has passed
        self.spawn_timer += dt

        # Check if it's time to spawn a new asteroid
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0 # Reset the timer

            # Select a random edge from the predefined edges list
            edge = random.choice(self.edges)
            # Generate a random speed between 40 and 100 pixels per second
            speed = random.randint(40, 100)
            # Set the velocity direction based on the chosen edge
            velocity = edge[0] * speed
            # Add some randomness to the direction by rotating the velocity vector
            # between -30 and 30 degrees
            velocity = velocity.rotate(random.randint(-30, 30))
            # Generate a position along the chosen edge
            # The random.uniform(0, 1) parameter determines where along the edge
            position = edge[1](random.uniform(0, 1))
            # Determine the asteroid size/type (1 to ASTEROID_KINDS)
            kind = random.randint(1, ASTEROID_KINDS)

            # Create and spawn the new asteroid with calculated parameters
            # Size is determined by multiplying the minimum radius by the kind
            asteroid = self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)