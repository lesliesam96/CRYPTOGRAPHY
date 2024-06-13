import pygame

from gameSettings import *
import math
from tetrominoBlock import Tetromino
import pygame.freetype as ft
import random
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cripto import MessageEncryptionApp

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
import os
import hashlib


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)
        self.timer_font = ft.Font(FONT_PATH)
        self.timer_position = (WIN_W * 0.595, WIN_H * 0.3)
        self.timer_duration = random.randint(30, 50)
        self.app = app
        self.font = ft.Font(FONT_PATH)
        message_to_encrypt = "Your secret message"
        key = Fernet.generate_key()
        fernet = Fernet(key)

        encrypted_message = fernet.encrypt(message_to_encrypt.encode())

        self.decMsg = fernet.decrypt(encrypted_message)

        self.encrypted_message = encrypted_message

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        def n_sin(t): return (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw_decrypted_message(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.12),
                            text=f'Decrypted Message:', fgcolor='white',
                            size=20)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='Encrypted message', fgcolor='white',  # Change color to white
                            size=25,  # Set the font size to 16
                            )
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.06),
                            text=f'{self.app.encrypted_message}', fgcolor='white',
                            size=20)
        if self.app.encrypted_message and self.app.encrypted_message_checker:
            self.font.render_to(self.app.screen, (WIN_W * 0.600, WIN_H * 0.1),
                                text='Dencrypted message', fgcolor='white',  # Change color to white
                                size=25,  # Set the font size to 16
                                )

            self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.15),
                                text=f'message has not been decrypted', fgcolor='white',
                                size=20)
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.56),
                            # text=f'Required Score: {self.app.required_score}', fgcolor='white',
                            text=f' ', fgcolor='white',
                            size=20)

        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67),
                            text='score', fgcolor='white',  # Change color to white
                            size=20,  # Set the font size to 16
                            bgcolor='black')

        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)
        if (self.app.expected_score_reached):
            print(self.app.tetris.score)


class Tetris(Text):
    def __init__(self, app, enc_instance):
        self.enc_instance = enc_instance
        self.font = ft.Font(FONT_PATH)
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self, )
        self.next_tetromino = Tetromino(
            self, current=False, level=self.app.hardness)
        self.speed_up = False
        self.timer_font = ft.Font(FONT_PATH)
        self.timer_position = (WIN_W * 0.595, WIN_H * 0.3)
        self.timer_duration = 2000000000099900909
        self.expected_score_reached = False
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
        self.blocks_count = 4
        self.blocks_counter = 0
        self.valve = True
        self.root = tk.Tk()
        self.root.withdraw()
        self.new_block_generation = True
        self.column_totals = [0] * FIELD_W
        self.total_blocks = FIELD_W * FIELD_H
        self.blocks_counter = 0
        self.check_for_game_over = False
        self.ten_digit_key = 0

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        if self.score >= self.app.required_score:
            if self.valve:
                self.valve = False
        self.full_lines = 0

    def calculate_column_totals(self):
        for x in range(FIELD_W):
            self.column_totals[x] = sum(
                1 if self.field_array[y][x] else -1 for y in range(FIELD_H))
        # if all(total == -20 for total in self.column_totals):  # To decrpt the message you have to eliminate al the blocks includin the fast falling on at the begining of the game
        if self.score >=100: # the testin line to test that decryption works
            if self.check_for_game_over:
                self.app.game_over("win")
                self.app.hardness = self.app.hardness+1
                self.app.score = 0

    def acknowlegement(self, message="Pasused"):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Score reached", message)
        root.destroy()

    def decrypted(self):
        try:
            plain_text = self.enc_instance.decrypt()
            return plain_text
        except Exception as e:
            print("Decryption failed:", e)

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1
                self.blocks_count -= 10

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block
            self.blocks_counter += 1
            self.total_blocks -= 1

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_tetromino_landing(self):
        if self.blocks_counter > 100:
            self.speed_up = False
            with open("status.txt", "w") as file:
                file.write("active")
            self.app.ANIM_TIME_INTERVAL = 15000000

        else:
            current_tetrimino_name = self.app.tetris.tetromino.shape
            self.speed_up = True
            if self.new_block_generation:

                if current_tetrimino_name == "L" or current_tetrimino_name == "J":

                    self.tetromino.rotate()
                    self.tetromino.move(direction="left")
                if current_tetrimino_name == "O":
                    self.tetromino.rotate()
                    self.tetromino.move(direction="right")
                if current_tetrimino_name == "I":
                    self.tetromino.rotate()

                if current_tetrimino_name == "Z":
                    self.tetromino.move(direction="right")
                if current_tetrimino_name == "S":
                    self.tetromino.move(direction="left")

        self.blocks_counter += 1

        if self.tetromino.landing:

            if self.is_game_over():
                self.__init__(self.app, self.app.enc_instace)

            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(
                    self, current=False, level=self.app.hardness)
                self.new_block_generation = True
                self.check_for_game_over = True
                self.calculate_column_totals()

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger,
                   self.app.fast_anim_trigger][self.speed_up]
        down_key_pressed = pg.key.get_pressed()[pg.K_DOWN]

        # if trigger:
        if trigger or down_key_pressed:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()

        self.timer_duration -= 1 / FPS
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        # timer_text = f'Time Left: {int(self.timer_duration)}'
        timer_text = f' '
        self.timer_font.render_to(
            self.app.screen, self.timer_position, text=timer_text, fgcolor='white', size=20)
        self.sprite_group.draw(self.app.screen)
        for x, total in enumerate(self.column_totals):
            self.font.render_to(self.app.screen, (x * TILE_SIZE, 0),
                                text=str(total), fgcolor='white', size=20)

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
