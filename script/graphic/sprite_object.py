import pygame as pg
from settings import *
import os
from collections import deque

BASE_IMG_PATH = 'asset/images/'

def load_image(path):
    img = pg.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

class AnimatedSpriteObject:
    def __init__(self, game, path = BASE_IMG_PATH + 'pokemon/polygon/0.png', pos = (10, 10), scale = 1.0, animation_time =300):
        self.game = game
        self.x, self.y = pos

        self.animation_time = animation_time
        self.image = pg.image.load(path).convert_alpha()
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images