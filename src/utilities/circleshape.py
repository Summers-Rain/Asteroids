import pygame

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self)

        if hasattr(self, "containers"):
            self.add(*self.containers) 

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (int(x), int(y))

    def draw(self, screen):
        pass

    def update(self, dt):
        pass
    
    def collision(self, CircleShape):
        distance = self.position.distance_to(CircleShape.position)
        sum_of_radii = self.radius + CircleShape.radius

        if distance <= sum_of_radii:
            return True
        else:
            return False