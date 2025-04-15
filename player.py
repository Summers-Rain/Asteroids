import pygame
from circleshape import CircleShape
from constants import *
from bullet import Shot

class Player(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y):
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.lives = INITIAL_LIVES
        self.is_respawning = False
        self.respawn_timer = 0
        self.respawn_duration = RESPAWN_INVULNERABILITY_TIME
        self.flicker_counter = 0
        self.rotation = 0
        self.timer = 0

    def draw(self, screen):
        if self.is_respawning and self.flicker_counter % 6 >= 3:
            return
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.is_respawning:
            current_time = pygame.time.get_ticks()
            if current_time - self.respawn_timer > self.respawn_duration:
                self.is_respawning = False
            self.flicker_counter += 1

        if self.timer > 0:
            self.timer -= dt

    def respawn(self):
        if self.lives > 0:
            self.lives -= 1
            self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.velocity = pygame.Vector2(0, 0)
            self.rotation = 0
            self.is_respawning = True
            self.respawn_timer = pygame.time.get_ticks()
            return True
        return False

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.timer > 0:
            return
        else:
            velocity = direction * PLAYER_SHOOT_SPEED
            shot = Shot(self.position.x, self.position.y, velocity)
            self.timer = PLAYER_SHOOT_COOLDOWN


