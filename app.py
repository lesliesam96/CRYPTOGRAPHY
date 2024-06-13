import pygame

from gameSettings import *
from tetrisMain import Tetris, Text
import sys
import pathlib


import pygame as pg
import pygame_gui
import tkinter as tk
from tkinter import messagebox

import tkinter as tk
from tkinter import messagebox  # Use messagebox instead of simpledialog
from cryptography.hazmat.primitives import serialization
import hashlib


class CustomDialog:
    def __init__(self, private_key):
        self.private_key = private_key
        self.message = "Here is your hashed private key:"

    def show_dialog(self):
        result = messagebox.showinfo(
            "Hashed Private Key", f"{self.message}\n\n {self.private_key}")
        return result


# Example usage:
if __name__ == "__main__":
    example_private_key = None
    dialog = CustomDialog(example_private_key)
    dialog.show_dialog()


class App:
    timer = 10

    def __init__(self, screen="None", gameManager=None, username="", enc_message="mess",   hardness=1, enc_instace=None):
        self
        pg.init()
        score = 200 if hardness == 1 else (500 if hardness == 2 else 1000)
        pg.display.set_caption('Cryptris')
        self.iteration = 1
        self.start_score = score * self.iteration
        self.required_score = score * self.iteration
        self.username = username
        self.encrypted_message = enc_message
        with open("file.key", "rb") as key:
            self.private_key = key.read()
        hardness = hardness
        self.ANIM_TIME_INTERVAL = 150

        self.hardness = int(hardness)
        self.screen = screen
        self.gameManager = gameManager
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.enc_instace = enc_instace
        dialog = CustomDialog(self.private_key_to_10_digits(
            self.enc_instace.private_key))
        dialog.show_dialog()

        self.tetris = Tetris(self, enc_instace)
        self.text = Text(self)
        self.score = 0
        self.timer = 10
        self.required_time = 1000
        self.manager = pygame_gui.UIManager((WIN_W, WIN_H))
        self.display_game_over = False
        self.expected_score_reached = False
        self.plainmsg = None

        self.total_score = 1000 + score
        self.cumulative_score = 0
        self.cumulative_score_valve = False
        self.encrypted_message_checker = True

    def private_key_to_10_digits(self, private_key):
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        sha256 = hashlib.sha256()
        sha256.update(private_key_bytes)
        result = int(sha256.hexdigest()[:10], 16)
        self.ten_digit_key = result
        return result

    def game_over(self, status):
        pg.font.init()
        font = pg.font.Font(None, 36)
        message = f"Hello {self.username}\n"
        message += "Congratulations! Message decrypted! You got lucky though."
        self.encrypted_message_checker = False
        self.decryption_message = f"\nDecrypted Message: \n{self.insert_newline_every_10_characters(self.tetris.decrypted())}"
        message += "\n"
        message += "\n"
        message += "\n"
        message += self.decryption_message
        message += "\n"
        message += "\n"
        message += "\nPress R to Continue or Q to quit."
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        # Restart the game
                        self.restart_game(status)
                        return
                    if event.key == pg.K_q:
                        # Quit the game
                        pg.quit()
                        quit()

            self.screen.fill((0, 0, 0))
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIN_W // 2, WIN_H // 3))
            self.screen.blit(text, text_rect)
            if self.expected_score_reached:
                text = font.render(self.decryption_message,
                                   True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIN_W // 2, WIN_H // 2))
                self.screen.blit(text, text_rect)
            pg.display.update()
            self.screen.fill((0, 0, 0))
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIN_W // 2, WIN_H // 3))
            self.screen.blit(text, text_rect)
            pg.display.update()

    def restart_game(self, status):
        self.tetris.valve = True
        if status == "win":
            self.expected_score_reached = False
            self.required_score += 200  # Add 200 to the required score
            self.cumulative_score += self.required_score
        else:
            self.expected_score_reached = False
            self.required_score = self.required_score  # Add 200 to the required score

    def insert_newline_every_10_characters(self, input_string):
        result = ""
        for i, char in enumerate(input_string, start=1):
            result += char
            if i % 50 == 0:
                result += '\n'
        return result

    def display_decrypted_message(self):
        self.screen.fill(BG_COLOR)  # Clear the screen

    def quit_game(self):
        pg.quit()
        sys.exit()

    def load_images(self):
        files = [item for item in pathlib.Path(
            SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(
            image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, self.ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.tetris.update()
        self.required_time -= 1 / FPS
        if self.expected_score_reached:
            self.display_game_over = True
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.display_game_over:
                    self.quit_game()
                else:
                    pg.quit()
                    sys.exit()
            self.manager.process_events(event)  # Process GUI events
        if self.display_game_over:
            self.manager.update(1 / FPS)
            self.manager.draw_ui(self.screen)
        else:
            self.screen.fill(color=BG_COLOR)
            self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
            self.tetris.draw()
            self.text.draw()
            pg.display.flip()

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while self.timer > 0:  # Check the timer
            self.check_events()
            self.update()
            self.draw()

            # Check if decryption conditions are met
            if self.score >= self.required_score and self.timer >= 0:
                self.encrypted_message = self.text.encrypted_message


if __name__ == '__main__':
    app = App()
    app.run()
