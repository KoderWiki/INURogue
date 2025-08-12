import pygame as pg
from settings import *

def set_image(path, w, h):
    img = pg.image.load(path).convert_alpha()
    p_w,p_h = img.get_size()
    image = pg.transform.scale(img, (p_w * w, p_h * h))
    return image

class Ending:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.ending = False
        self.font_path = "asset/font/normal.ttf"
        self.font = pg.font.Font(self.font_path, 48)
        self.bigfont = pg.font.Font(self.font_path, 60)
        self.ending1 = "The End"
        self.ending2 = "한학기 수업 고생 많으셨습니다!"
        self.ending1_text = self.bigfont.render(self.ending1, True, (255,255,255))
        self.ending2_text = self.font.render(self.ending2, True, (255,255,255))
        self.cursor = set_image('asset/images/ui/cursor.png', 3, 3)
        self.prompt0 = True
        self.prompt1 = False
        self.prompt2 = False
        self.press = False
        self.end = False

    def ending_prompt(self):
        keys = pg.key.get_pressed()

        if self.prompt0:
            self.screen.fill((0, 0, 0))

        if keys[pg.K_j] and not self.press and self.prompt0:
            self.press = True
            self.prompt0 = False
            self.screen.fill((0, 0, 0))
            self.prompt1 = True
            
        if self.prompt1:
            self.screen.blit(self.ending1_text, (HALF_WIDTH - 100, HALF_HEIGHT - 50))
            
        if keys[pg.K_j] and not self.press and self.prompt1:
            self.press = True
            self.prompt1 = False
            self.screen.fill((0, 0, 0))
            self.prompt2 = True

        if not keys[pg.K_j]:
            self.press = False
        
        if self.prompt2:
            self.screen.blit(self.ending2_text, (HALF_WIDTH - 200, HALF_HEIGHT - 40))

        if self.prompt1:
            self.screen.blit(self.cursor, (HALF_WIDTH - 120, HALF_HEIGHT - 40))
        else:
            self.screen.blit(self.cursor, (HALF_WIDTH-230, HALF_HEIGHT - 40))

        if keys[pg.K_j] and not self.press and self.prompt2:
            self.press = True
            self.end = True
        
        if self.end:
            pg.quit()

    def update(self):
        self.ending_prompt()

            
