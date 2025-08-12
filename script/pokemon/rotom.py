import pygame as pg
from settings import *
from script.main.pokemon import *

class Rotom(Pokemon):
    def __init__(self, game, pokemon = 'rotom', path = 'asset/images/pokemon/rotom/0.png', scale = 4.0, animation_time = 250):
        super().__init__(game=game, path=path, scale=scale, animation_time = animation_time)
        self.game = game
        self.x, self.y = 20,4
        self.image_size = 34,34

        self.pokemon = pokemon

        self.path = 'asset/images/pokemon/{}'.format(self.pokemon)
        self.pokemon_images = self.get_images(self.path)

        self.idle_image = self.img_update(self.pokemon_images, 1.5)

        self.type = 'normal'

        self.level = 50
        self.hp = 125
        self.max = 125

        self.skill = ['thunder', "shadowpunch", 'thunderouskick']


    def draw(self):
        img = self.idle_image[0]
        self.game.screen.blit(img, ((self.x * TILESIZE ), (self.y * TILESIZE )))
        self.animate(self.idle_image)
    
    def update(self):
        self.check_animation_time()
        
