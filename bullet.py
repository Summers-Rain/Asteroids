import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        CircleShape.__init__(self, x, y, SHOT_RADIUS)
        pygame.sprite.Sprite.__init__(self)
        self.velocity = velocity

    def update(self, dt):
        self.position += self.velocity * dt
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)