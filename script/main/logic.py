import pygame as pg
from script.main.battle import *
from script.handler.pokemon_handler import *
from script.handler.player_handler import *
from script.main.ending import *
from script.main.intro import *

class Logic:
    def __init__(self, game):
        self.game = game
        self.intro = Intro(game)
        self.battle = Battle(game)
        self.pokemon = self.game.pokemon
        self.player_pokemon = self.game.player.pokemon
        self.ending = Ending(game)
        self.started_battle = False
        self.ending_start = False

    def update(self):
        if self.intro.intro:
            self.intro.update()

        elif not self.started_battle:
            self.battle.battle = True
            self.started_battle = True

        if self.battle.battle:
            self.battle.update()
        
        elif self.started_battle and not self.ending_start:
            self.ending.ending = True
            self.ending_start = False

        if self.ending.ending:
            self.ending.update()
