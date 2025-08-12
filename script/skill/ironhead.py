import pygame as pg
from settings import *
from script.main.skill import *

class Ironhead(Skill):
    def __init__(self, game, skill = 'ironhead', path = 'asset/images/skill/ironhead/0.png', scale = 7.0, animation_time = 150):
        super().__init__(game=game, path=path, scale=scale, animation_time = animation_time)
        self.game = game
        self.image_size = 34,34
        
        self.skill = skill

        self.path = 'asset/images/skill/{}'.format(self.skill)
        self.skill_images = self.get_images(self.path)

        self.idle_image = self.img_update(self.skill_images, 1.5)

        self.type = 'steel'
        self.damage = 40

    def draw(self, x, y):
        img = self.idle_image[0]
        self.game.screen.blit(img, ((x * TILESIZE ), (y * TILESIZE )))
        self.animate(self.idle_image)
        self.check_animation_time()
        
