import pygame

class Particle:
    def __init__(self, x, y, velocity, size, color, lifetime):
        self.position = pygame.Vector2(x,y)
        self.velocity = velocity
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.age = 0

    def update(self, dt):
        # Update position
        self.position += self.velocity * dt
        # Age the particle
        self.age += dt
        # Shrink the particle as it ages
        self.size = max(0, self.size * (1 - self.age/self.lifetime))
        # Return True if particle is still alive
        return self.age < self.lifetime
    
    def draw(self, screen):
        # Calculate alpha based on remaining lifetime
        alpha = int(255 * (1 - self.age/self.lifetime))
        # Draw the particle
        if self.size > 0:
            pygame.draw.circle(screen, (*self.color, alpha),
                               (int(self.position.x), int(self.position.y)),
                               int(self.size))