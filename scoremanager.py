import pygame
from constants import MULTIPLIER, MULTIPLIER_DURATION, MULTIPLIER_TIMER, MAX_MULTIPLIER

class ScoreManager(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.score = 0
        self.multiplier = MULTIPLIER
        self.multiplier_timer = MULTIPLIER_TIMER
        self.multiplier_duration = MULTIPLIER_DURATION
        self.max_multiplier = MAX_MULTIPLIER
        self.font = pygame.font.SysFont("Arial", 30)

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.multiplier_timer > self.multiplier_duration and self.multiplier > 1:
            self.multiplier = 1

    def add_points(self, base_points):
        self.score += int(base_points * self.multiplier)

        self.multiplier += 0.5
        if self.multiplier > self.max_multiplier:
            self.multiplier = self.max_multiplier

        self.multiplier_timer = pygame.time.get_ticks()

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 70))

        if self.multiplier > 1:
            multiplier_text = self.font.render(f"Multiplier: x{self.multiplier:.1f}", True, (255, 255, 0))
            screen.blit(multiplier_text, (10, 40))