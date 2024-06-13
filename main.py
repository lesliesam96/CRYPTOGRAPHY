# import pygame
import sys
from scenes.scene2 import *
from cripto import MessageEncryptionApp
from scenes.scene1 import *
from app import App
from scenes.halfscene import InterScene
from scenes.homescreen import HomeScreen
import random
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
FPS = 60


class Game:
    def __init__(self):
        pygame.init()
        self.hardness = 1
        self.username = "martin"
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager("homescreen")
        self.intro = IntroScene(self.screen, self.gameStateManager)
        self.homescreen = HomeScreen(self.screen, self.gameStateManager)
        self.scene2 = EncryptionScene(self.screen, self.gameStateManager)
        self.halfscene = InterScene(self.screen, self.gameStateManager)
        self.states = {
            "intro": self.intro,
            "scene2": self.scene2,
            "halfScene": self.halfscene,
            "homescreen": self.homescreen
        }
        self.current_scene = self.states[self.gameStateManager.getState()]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            current_state = self.gameStateManager.getState()
            if current_state == "halfScene" and not hasattr(self, 'game'):

                with open("data/data1.txt", "r") as file:
                    self.hardness = int(file.read())
                self.plain_text = self.intro.message
                
                
                
                self.enc_instance = MessageEncryptionApp(self.intro.password)
                self.enc_message =self.enc_instance.encrypt_message(self.plain_text)

                self.game = App(self.screen, self.gameStateManager, self.intro.username, self.enc_message,self.hardness,self.enc_instance)
                self.states["game"] = self.game
            self.states[current_state].run()
            pygame.display.update()
            self.clock.tick(FPS)
    import random



class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def getState(self):
        return self.currentState

    def setState(self, currentState):
        self.currentState = currentState


if __name__ == "__main__":
    Game().run()
