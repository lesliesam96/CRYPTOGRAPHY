import time

class InterScene:
	def __init__(self, screen, gameStateManager):
		time.sleep(0.5)
		self.gameStateManager = gameStateManager
	def run(self):

		self.gameStateManager.setState("game")
			