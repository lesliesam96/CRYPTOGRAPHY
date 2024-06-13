import pygame
import sys

class HomeScreen:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.width, self.height = pygame.display.get_surface().get_size()

    def draw(self):
        # Set background color to white
        self.screen.fill((255, 255, 255))

        # Draw title at the top center
        font = pygame.font.Font(None, 36)
        title_text = font.render("Cryptris", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Draw buttons in the center
        button_font = pygame.font.Font(None, 30)

        # Draw Arcade button
        arcade_button_text = button_font.render("Start game Press a", True, (0, 0, 0))
        arcade_button_rect = arcade_button_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.screen.blit(arcade_button_text, arcade_button_rect)

        # Draw File Mode button
        file_mode_button_text = button_font.render("", True, (0, 0, 0))
        file_mode_button_rect = file_mode_button_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(file_mode_button_text, file_mode_button_rect)

        return arcade_button_rect, file_mode_button_rect

    def run(self):
        arcade_button_rect, file_mode_button_rect = self.draw()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            all_keys = pygame.key.get_pressed()
            if all_keys[pygame.K_a]:
                self.gameStateManager.setState("intro")
                break

            # if all_keys[pygame.K_f]:
            #     self.gameStateManager.setState("fileMode")
            #     break
            pygame.display.flip()

