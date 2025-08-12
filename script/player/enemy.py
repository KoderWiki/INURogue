import pygame as pg

class Enemy:
    def __init__(self, game):
        self.game = game
        self.pokemon = 0
        self.left = 3