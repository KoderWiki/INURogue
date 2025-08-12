import pygame as pg
from settings import *
from script.main.pokemon import *

class Machamp(Pokemon):
    def __init__(self, game, pokemon = 'machamp', path = 'asset/images/player/machamp/0.png', scale = 7.0, animation_time = 150):
        super().__init__(game=game, path=path, scale=scale, animation_time = animation_time)
        self.game = game
        self.x, self.y = 6,11
        self.image_size = 34,34

        self.pokemon = pokemon

        self.path = 'asset/images/player/{}'.format(self.pokemon)
        self.pokemon_images = self.get_images(self.path)

        self.idle_image = self.img_update(self.pokemon_images, 1.5)

        self.type = 'fight'
        self.death = False

        self.level = 50
        self.max = 175
        self.hp = 175

        self.skill = ['earth', "thunderouskick", 'ironhead', 'shadowpunch']

    def draw(self):
        img = self.idle_image[0]
        self.game.screen.blit(img, ((self.x * TILESIZE ), (self.y * TILESIZE )))
        self.animate(self.idle_image)
    
    def update(self):
        self.check_animation_time()
        
