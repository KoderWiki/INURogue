import pygame as pg
import sys, os
from settings import *
from script.graphic.sprite_object import *
from script.handler.pokemon_handler import *
from script.handler.player_handler import *
from script.player.player import *
from script.player.enemy import *
from script.main.battle import *
from script.main.logic import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        icon = pg.image.load("asset/images/icon.png")
        pg.display.set_icon(icon)
        self.new_game()

    def new_game(self):
        self.player = Player(self)
        self.enemy = Enemy(self)
        
        self.player_pokemon = PlayerHandler(self)
        self.pokemon = PokemonHandler(self)
        
        self.logic = Logic(self)


    def update(self):
        self.pokemon.update()
        self.player_pokemon.update()
        self.logic.update()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption("INURoGue")
        

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()

if __name__ == '__main__':
    game = Game()
    game.run()