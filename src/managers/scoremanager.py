import pygame
from src.constants import MULTIPLIER, MULTIPLIER_DURATION, MULTIPLIER_TIMER, MAX_MULTIPLIER

class ScoreManager(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.score = 0
        self.high_score = 0
        self.new_high_score_achieved = False
        self.load_high_score() # Load previous high score
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

    def update_high_score(self):
        self.new_high_score_achieved = False # Reset the flag
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_high_score_achieved = True # Set flag when new high score is achieved
            # Save high score to file
            self.save_high_score()

    def save_high_score(self):
        # Save high score to a file
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def load_high_score(self):
        # Load high score from file if it exists
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except (FileNotFoundError, ValueError):
            # If file doesn't exist or content is invalid, keep default
            self.high_score = 0
    
    def reset_score(self):
        self.update_high_score() # make sure high score is updated
        self.score = 0 # Then reset the score

    def reset_high_score(self):
        self.high_score = 0
        self.save_high_score() # Save the reset high score to file

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 70))

        if self.multiplier > 1:
            multiplier_text = self.font.render(f"Multiplier: x{self.multiplier:.1f}", True, (255, 255, 0))
            screen.blit(multiplier_text, (10, 40))