import pygame as pg
from settings import *
from script.graphic.sprite_object import *

class Trainer(AnimatedSpriteObject):
    def __init__(self, game, name = '김동훈 교수', path = 'asset/images/trainer/0.png', scale = 1.0, animation_time = 200):
        super().__init__(game=game, path=path, scale=scale, animation_time = animation_time)
        self.game = game
        self.x, self.y = 10,10
        self.scale = scale
        self.image_size = 34,34

        self.path = 'asset/images/trainer'
        self.images = self.get_images(self.path)

        self.idle_image = self.img_update(self.images, 7.0)
        
        self.name = name
        self.frame_counter = 0
        self.scale = scale
    
    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def animate(self, images):
        num_images = len(images)

        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]
            self.frame_counter += 1
            if self.frame_counter == num_images:
                self.frame_counter = 0

    def img_update(self, images, size):
        images = deque(
            [pg.transform.smoothscale(img, (self.image_size[0] * self.scale * size, self.image_size[1]* self.scale * size))
            for img in images])
        return images
    
    def draw(self, x, y):
        img = self.idle_image[0]
        self.game.screen.blit(img, ((x * TILESIZE ), (y * TILESIZE )))
        self.animate(self.idle_image)
        self.check_animation_time()
    
    def update(self): 
        self.check_animation_time()
        self.animate()
    
    @property
    def map_pos(self):
        return int(self.x) , int(self.y) 