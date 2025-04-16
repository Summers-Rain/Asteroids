import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class MainMenu:
    def main_menu(self, screen):
        menu_font = pygame.font.Font(None, 64)
        small_font = pygame.font.Font(None, 32)
        
        title_text = menu_font.render("ASTEROIDS", True, (255, 255, 255))
        start_text = small_font.render("Press SPACE to Start", True, (255, 255, 255))
        exit_text = small_font.render("Press ESC to Exit", True, (255, 255, 255))
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        
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
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        return False  # Exit the game
            
            # Draw the menu
            screen.fill((0, 0, 0))  # Black background
            screen.blit(title_text, title_rect)
            screen.blit(start_text, start_rect)
            screen.blit(exit_text, exit_rect)
            
            pygame.display.flip()
            
        return True  # Continue to game