import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        pygame.sprite.Sprite.__init__(self)
        CircleShape.__init__(self, x, y, SHOT_RADIUS)
        self.velocity = velocity
        self.add(self.containers)

    def update(self, dt):
        self.position += self.velocity * dt

        if (self.position.x < -self.radius or 
            self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or 
            self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)