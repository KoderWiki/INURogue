from script.player.charizard import *
from script.player.machamp import *
from script.player.phantom import *


class PlayerHandler:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.pokemon_list = [Charizard(game), Machamp(game), Phantom(game)]

        self.pokemon = self.pokemon_list[self.player.pokemon]

    def draw(self):
        self.pokemon.draw()

    def update(self):
        self.pokemon.update()