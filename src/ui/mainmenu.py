import pygame
import sys
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class MainMenu:
    def __init__(self, score_manager=None):
        self.score_manager = score_manager

    def main_menu(self, screen):
        menu_font = pygame.font.Font(None, 64)
        high_score_font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 32)
        
        title_text = menu_font.render("ASTEROIDS", True, (255, 255, 255))

        # Handle the case where score_manager might be None
        high_score = 0
        if self.score_manager:
            high_score = self.score_manager.high_score

        high_score_text = high_score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        start_text = small_font.render("Press SPACE to Start", True, (255, 255, 255))
        reset_text = small_font.render("Press R to reset High Score", True, (255, 255, 255))
        exit_text = small_font.render("Press ESC to Exit", True, (255, 255, 255))
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/5))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        reset_rect = reset_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))
        
        # Menu loop
        in_menu = True
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False  # Exit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        in_menu = False  # Start the game
                    elif event.key == pygame.K_r:
                        if self.score_manager:
                            self.score_manager.reset_high_score()
                            #update the high score text using the score manager
                            high_score_text = high_score_font.render(f"High Score: {self.score_manager.high_score}", True, (255, 255, 255))
                        else:
                            # If no score manager, just display 0
                            high_score_text = high_score_font.render(f"High Score: 0", True, (255, 255, 255))

                        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        return False  # Exit the game
            
            # Draw the menu
            screen.fill((0, 0, 0))  # Black background
            screen.blit(title_text, title_rect)
            screen.blit(high_score_text, high_score_rect) # Display high score
            screen.blit(start_text, start_rect)
            screen.blit(reset_text, reset_rect) # Display reset instructions
            screen.blit(exit_text, exit_rect)
            
            pygame.display.flip()
            
        return True  # Continue to game