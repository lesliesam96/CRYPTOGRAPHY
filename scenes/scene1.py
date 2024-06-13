import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen_width, screen_height = 1000, 1000 
pygame.display.set_caption("Pygame Window")

font = pygame.font.Font(None, 36)

class TextInput:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color(0, 0, 255, 128)



        self.color = self.color_inactive
        self.text = ''
        self.active = False
        self.txt_surface = font.render(self.text, True, self.color)
        self.width = max(150, self.txt_surface.get_width() + 10)
        self.label = label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)
                self.width = max(150, self.txt_surface.get_width() + 10)

    def update(self):
        width = max(150, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        label_surface = font.render(self.label, True, BLACK)
        screen.blit(label_surface, (self.rect.x - label_surface.get_width() - 10, self.rect.y + 5))
        
        
class Button:
    def __init__(self, x, y, width, height, label,manager,):
        self.manager = manager
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('dodgerblue2')
        self.label = label

    def handle_event(self,event,manager,username_input, password_input, message_input):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "clicked"
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        label_surface = font.render(self.label, True, BLACK)
        screen.blit(label_surface, (self.rect.x + (self.rect.width - label_surface.get_width()) // 2, self.rect.y + 5))


class IntroScene:
    def __init__(self, screen, gameStateManager):
        self.display = screen
        self.gameStateManager = gameStateManager
        self.switch = False
        self.username = ""
        self.password = ""
        self.message  =""
    def switch(self):
        return self.switch

    def run(self):
        username_input = TextInput((screen_width - 150) // 2, 300, 150, 30, "Username:")
        message_input = TextInput((screen_width - 150) // 2, 350, 150, 30, "Message:")
        password_input = TextInput((screen_width - 150) // 2, 400, 150, 30, "Password:")
        press_e_button = Button((screen_width - 230) // 2, 550, 200, 40, "Press Shift ctrl", self.gameStateManager)
        press_b_button = Button((screen_width - 300) // 2, 950, 400, 40, "Please fill all the fields", self.gameStateManager)
        
        inputs = [username_input,message_input]
        buttons = [press_e_button]
        
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for input_field in inputs:
                    input_field.handle_event(event)

                for button in buttons:
                    button.handle_event(event, self.gameStateManager, username_input, password_input, message_input)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print("Username:", username_input.text)
                        print("Message:", message_input.text)
                        print("Password:", password_input.text)
            for input_field in inputs:
                input_field.update()
            self.display.fill(WHITE)
            title_surface = font.render("Hello and Welcome", True, BLACK)
            self.display.blit(title_surface, ((screen_width - title_surface.get_width()) // 2, 20))
            for input_field in inputs:
                input_field.draw(self.display)
            for button in buttons:
                button.draw(self.display)
            all_keys = pygame.key.get_pressed()
            if all_keys[pygame.K_LCTRL] and (all_keys[pygame.K_LSHIFT] or all_keys[pygame.K_RSHIFT]):
                self.switch = True
                self.username = username_input.text
                self.password = password_input.text
                self.message = message_input.text
                self.password_input = message_input.text
                if len(self.username) > 1:
                    self.gameStateManager.setState("scene2")
                    with open("passfile.txt", "w") as passfile:
                        passfile.write(self.password)
                    print(f"this is a password {self.password}")
                    break
                
                else:
                    buttons.append(press_b_button)
            pygame.display.flip()

