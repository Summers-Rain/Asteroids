import pygame
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, size_factor=20):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        
        self.size_factor = size_factor
        self.max_radius = size_factor * EXPLOSION_SIZE_MULTIPLIER

        self.radius = 1
        self.growth_rate = self.max_radius / EXPLOSION_GROWTH_RATIO
        self.duration = EXPLOSION_BASE_DURATION
        self.age = 0

        self.image = pygame.Surface((self.max_radius*2, self.max_radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.age += 1
        if self.age <= self.duration / 2:
            self.radius = min(self.radius + self.growth_rate, self.max_radius)
        else:
            self.radius = max(self.radius - self.growth_rate, 0)

        self.image.fill ((0,0,0,0))
        pygame.draw.circle(self.image, (255, 165, 0),
                           (self.max_radius, self.max_radius), self.radius)
        
        if self.age >= self.duration:
            self.kill()
