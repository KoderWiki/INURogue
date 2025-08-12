import pygame as pg
from settings import *

def set_image(path, w, h):
    img = pg.image.load(path).convert_alpha()
    p_w,p_h = img.get_size()
    image = pg.transform.scale(img, (p_w * w, p_h * h))
    return image

class Intro:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font_path = "asset/font/normal.ttf"
        self.font = pg.font.Font(self.font_path, 48)
        self.bigfont = pg.font.Font(self.font_path, 60)

        self.background_img = pg.image.load('asset/images/bg/intro.png').convert_alpha()
        self.background = pg.transform.scale(self.background_img, (WIDTH, HEIGHT))

        self.ui = set_image('asset/images/ui/ui.png', 10, 10)
        self.cursor = set_image('asset/images/ui/cursor.png', 3, 3)

        self.select_text = "Start"
        self.quit_text = "Quit"
        self.intro_text1 = "Computer Algorithm Final"
        self.intro_text2 = "Presend By 고건우"

        self.start1_text = self.font.render(self.select_text, True, (255,255,255))
        self.start2_text = self.font.render(self.quit_text, True, (255,255,255))
        self.start3_text = self.bigfont.render(self.intro_text1, True, (255,255,255))
        self.start4_text = self.bigfont.render(self.intro_text2, True, (255,255,255))

        self.intro = True

        self.prompt1 = True
        self.prompt2 = False
        self.prompt3 = False
        self.prompt4 = False

        self.cursor_x, self.cursor_y = 410, 535
        self.select = 1

    def prompt(self):
        keys = pg.key.get_pressed()

        if self.prompt1:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.ui, (HALF_WIDTH - 110, HALF_HEIGHT + 70))
            self.screen.blit(self.start1_text, (440, 530))
            self.screen.blit(self.start2_text, (450, 600))

        if keys[pg.K_j] and not self.press and self.prompt1:
            self.press = True
            self.prompt1 = False
            self.screen.fill((0, 0, 0))

            if self.select == 1:
                self.prompt2 = True
            else:
                pg.quit()

        if not keys[pg.K_j]:
            self.press = False

        if self.prompt2:
            self.screen.blit(self.start3_text, (HALF_WIDTH - 230, HALF_HEIGHT - 40))

        if keys[pg.K_j] and not self.press and self.prompt2:
            self.press = True
            self.prompt2 = False
            self.screen.fill((0, 0, 0))
            self.prompt3 = True

        if not keys[pg.K_j]:
            self.press = False

        if self.prompt3:
            self.screen.blit(self.start4_text, (HALF_WIDTH - 230, HALF_HEIGHT - 40))

        if keys[pg.K_j] and not self.press and self.prompt3:
            self.press = True
            self.prompt3 = False

        if not keys[pg.K_j] and not self.prompt3 and not self.prompt1 and not self.prompt2:
            self.intro = False
            self.press = False
            

    def draw_cursor(self):
        keys = pg.key.get_pressed()

        if self.prompt1:
            if keys[pg.K_w] :
                self.cursor_x, self.cursor_y = 410, 535
                self.select = 1
            if keys[pg.K_s] :
                self.cursor_x, self.cursor_y = 410, 605
                self.select = 2

        if self.prompt2:
            self.cursor_x, self.cursor_y = HALF_WIDTH -280, HALF_HEIGHT - 35
        
        self.screen.blit(self.cursor, (self.cursor_x, self.cursor_y))

    def update(self):
        self.prompt()
        self.draw_cursor()




            
