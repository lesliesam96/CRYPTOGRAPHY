import pygame
import sys
sys.path.append("..")

from app import App
from cripto import MessageEncryptionApp

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen_width, screen_height = 1000, 1000
pygame.display.set_caption("Pygame Window")
font = pygame.font.Font(None, 36)
class Slider:
    def __init__(self, x, y, width, height, min_value, max_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.value = min_value
        self.min_value = min_value
        self.max_value = max_value
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.color = self.color_active
                self.update_value(event.pos)
            else:
                self.color = self.color_inactive
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.color_active
                self.update_value(event.pos)
            else:
                self.color = self.color_inactive

    def update_value(self, mouse_pos):
        percent = (mouse_pos[0] - self.rect.left) / self.rect.width
        self.value = round(self.min_value + percent * (self.max_value - self.min_value))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        pygame.draw.circle(screen, BLACK, (int(self.rect.left + (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width), self.rect.centery), 10)

class Button:
    def __init__(self, x, y, width, height, label, screen):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('dodgerblue2')
        self.label = label
        self.font = pygame.font.Font(None, 36)


    def handle_event(self, event, slider_value):
        scores = {
        1:1200,
        2:1400,
        3:2000
        }
        text_surface = self.font.render("Hello, Pygame!", True, (255, 255, 255))  # Text, antialiasing, color
        text_position = (100, 200)
        self.screen.blit(text_surface, text_position)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        label_surface = font.render(self.label, True, BLACK)
        self.screen.blit(label_surface, (self.rect.x + (self.rect.width - label_surface.get_width()) // 2, self.rect.y + 5))

class EncryptionScene:
    def __init__(self, screen, game_manager):
        self.font = pygame.font.Font(None, 36)
        self.screen = screen
        self.gameStateManager = game_manager
        self.difficulty_slider = Slider((screen_width - 400) // 2, 100, 400, 20, 1, 3)
        self.encrypt_button = Button((screen_width - 150) // 2, 200, 150, 40, "Press R",self.screen)
        self.result_message = ""

    def run(self):
        self.screen.fill("red")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.difficulty_slider.handle_event(event)
            message = self.encrypt_button.handle_event(event, self.difficulty_slider.value)
            if message:
                self.result_message = message

        self.screen.fill(WHITE)
                # Draw title
        title_surface = font.render("Choose Game difficulty", True, BLACK)
        self.screen.blit(title_surface, ((screen_width - title_surface.get_width()) // 2, 20))

        # Draw slider
        self.difficulty_slider.draw(self.screen)

        # Draw button
        self.encrypt_button.draw(self.screen)

        # Draw result message
        if self.result_message:
            text_surface = self.font.render(self.result_message, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_width // 2, 300))
            self.screen.blit(text_surface, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:

            scores = {
            1:1200,
            2:1400,
            3:2000
            }
            text_surface = self.font.render("Hello, Pygame!", True, (255, 255, 255))  # Text, antialiasing, color
            text_position = (100, 200)
            self.screen.blit(text_surface, text_position)
            print(f"Encrypt Clicked! Difficulty: {self.difficulty_slider.value}")
            self.result_message =f"""
                
                \n \n Hello Martin, your message has been encryptedn.\n The first half of your private key has been saved to your desktop.\nTo decrypt this message, you will have to complete the Tetris game.
                    \n \nTo get the chance to decrypt the message you will need to get a score of {scores[self.difficulty_slider.value]}, \n Press M to continue
                """
            text_surface = self.font.render(self.result_message, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_width // 2, 300))
            self.screen.blit(text_surface, text_rect)

        if keys[pygame.K_r]:


            with open ("data/data1.txt", "w") as file:
                file.write(str(self.difficulty_slider.value))
            self.gameStateManager.setState("halfScene")
    













        
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_e]:
        #     self.gameStateManager.setState("level")
