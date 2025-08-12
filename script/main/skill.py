import pygame as pg
from settings import *
from script.graphic.sprite_object import *

class Skill(AnimatedSpriteObject):
    def __init__(self, game, skill = 'airslash', path = 'asset/images/skill/airslash/0.png', scale = 2.0, animation_time = 250):
        super().__init__(game=game, path=path, scale=scale, animation_time = animation_time)
        self.game = game
        self.x, self.y = 10,10
        self.scale = scale
        self.size = 34,34
        
        self.skill = skill
        self.frame_counter = 0
        self.scale = scale
        self.end = False
        
    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def animate(self, images):
        num_images = len(images)

        if self.animation_trigger and self.frame_counter < num_images:
            images.rotate(-1)
            self.image = images[0]
            self.frame_counter += 1

            if self.frame_counter >= num_images:
                self.end = True
    
    def img_update(self, images, size):
        images = deque(
            [pg.transform.smoothscale(img, (self.image_size[0] * self.scale * size, self.image_size[1]* self.scale * size))
            for img in images])
        return images
    

    def update(self): 
        self.check_animation_time()
        self.animate()