import pygame as pg
from settings import *
from script.handler.skill_hander import *
from script.player.trainer import *
from script.main.softmax import *

def set_image(path, w, h):
    img = pg.image.load(path).convert_alpha()
    p_w,p_h = img.get_size()
    image = pg.transform.scale(img, (p_w * w, p_h * h))
    return image

class Battle:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.skill_handler = SkillHandler(self.game)
        self.trainer = Trainer(self.game)

        self.pressed = False
        self.s_pressed = False

        self.battle = False
        self.run = False

        self.first_select = True
        self.first_select_number = 1 

        self.second_select = False
        self.skill = 1

        self.fight = False
        self.dealt = False

        self.e_dealt = False
        self.select = False
        self.e_skill = ''
        self.result = []
        self.e_result = []

        self.weak = False
        self.strong = False

        self.player = self.game.player_pokemon
        self.enemy = self.game.pokemon

        self.player_name = self.player.pokemon.pokemon
        self.enemy_name = self.enemy.pokemon.pokemon

        self.cursor = set_image('asset/images/ui/cursor.png', 3, 3)
        self.cursor_x, self.cursor_y = 670, 650

        self.p_hp = set_image('asset/images/ui/hp.png', 4.1, 3.7)
        self.e_hp = set_image('asset/images/ui/hp.png', 4.1, 5)

        self.player_ui = set_image('asset/images/ui/player.png', 3, 3)
        self.enemy_ui = set_image('asset/images/ui/enemy.png', 3, 5)

        self.background_img = pg.image.load('asset/images/bg/bg1.png').convert_alpha()
        self.background = pg.transform.scale(self.background_img, (WIDTH, HEIGHT))
        
        self.ground_img = pg.image.load('asset/images/bg/bg2.png').convert_alpha()
        w,h = self.ground_img.get_size()
        self.ground = pg.transform.scale(self.ground_img, (w * 3.0, h * 3.0))
        self.ground2 = pg.transform.scale(self.ground_img, (w *4.0, h * 5.0))
        
        self.ui = set_image('asset/images/ui/ui.png', 70, 7)

        self.skill_ui = set_image('asset/images/ui/ui.png', 15, 7)

        self.font_path = "asset/font/normal.ttf"
        self.font = pg.font.Font(self.font_path, 48)
        self.middle_font = pg.font.Font(self.font_path, 40)

        self.select_text = "{}은 무엇을 할까?".format(self.player_name)
        self.s_text = self.font.render(self.select_text, True, (255,255,255))

        self.select2_text = "싸운다"
        self.select3_text = "도망간다"
        self.select4_text = "등의 상처는 검사의 수치다"
        self.s2_text = self.font.render(self.select2_text, True, (255,255,255))
        self.s3_text = self.font.render(self.select3_text, True, (255,255,255))
        self.s4_text = self.font.render(self.select4_text, True, (255,255,255))

        self.skill_1 = self.player.pokemon.skill[0]
        self.skill_2 = self.player.pokemon.skill[1]
        self.skill_3 = self.player.pokemon.skill[2]
        self.skill_4 = self.player.pokemon.skill[3]
        self.skill_1_text = self.font.render(self.skill_1, True, (255,255,255))
        self.skill_2_text = self.font.render(self.skill_2, True, (255,255,255))
        self.skill_3_text = self.font.render(self.skill_3, True, (255,255,255))
        self.skill_4_text = self.font.render(self.skill_4, True, (255,255,255))

        self.fight_text = "효과가 굉장했다"
        self.fight_1_text = "효과가 별로였다"
        self.prompt1 = True
        self.prompt2 = False
        self.prompt3 = False
        self.prompt4 = False

        self.c_prompt1 = True
        self.c_prompt2 = False
        self.c_prompt3 = False
        self.c_prompt4 = False

        self.ec_prompt1 = True
        self.ec_prompt2 = False
        self.ec_prompt3 = False
        self.ec_prompt4 = False

        self.p_live = True
        self.e_live = True

        self.die = False

        self.tick = True
        self.e_tick = True

        self.next_pokemon = ''

        self.e_skill = self.skill_handler.skill_list[0]
        self.p_skill = self.skill_handler.skill_list[0]


    def select_logic(self):
        keys = pg.key.get_pressed()
            

        if self.first_select:
            if keys[pg.K_j] and not self.s_pressed and self.run == False:
                self.s_pressed = True

                if self.first_select_number == 2:
                    self.run = True

                if self.first_select_number == 1:
                    self.first_select = False
                    self.second_select = True
                    self.cursor_x, self.cursor_y = 20, 655

            if not keys[pg.K_j]:
                self.s_pressed = False

            if not self.run:
                self.ui_1_draw()

            if self.run:
                self.screen.blit(self.s4_text, (50, 650))
                self.cursor_x, self.cursor_y = 20, 650

                if keys[pg.K_j] and not self.s_pressed:
                    self.s_pressed = True
                    self.run = False
                    self.cursor_x, self.cursor_y = 670, 650
                    self.first_select_number = 1

            if not keys[pg.K_j]:
                self.s_pressed = False

        if self.second_select:
            if keys[pg.K_j] and not self.s_pressed:
                self.s_pressed = True
                self.second_select = False
                self.fight = True
            else:
                self.second_select = True

            if not keys[pg.K_j]:
                self.s_pressed = False

            if not self.fight:
                self.ui_2_draw()

        if self.fight:
            self.fight_draw()

        if self.player.pokemon.hp < 0 and not self.fight:
            self.p_live = False
            if self.tick:
                if self.game.player.left > 0:
                    
                    self.game.player.left -= 1
                self.tick = False
            self.second_select = False
        elif self.enemy.pokemon.hp < 0 and not self.fight:
            self.e_live = False
            if self.e_tick:
                if self.game.enemy.left > 0:
                    self.game.enemy.left -= 1
                self.e_tick = False
            self.second_select = False

        if not self.p_live:
            self.player_change()
        
        if not self.e_live:
            self.enemy_change()

        self.draw_cursor()

    def intro(self):
        keys = pg.key.get_pressed()

        self.trainer.draw(20,3)
        self.intro_text1 = "{} 가 승부를 걸어왔다".format(self.trainer.name)
        self.intro_text1 = self.font.render(self.intro_text1, True, (255,255,255))
        self.screen.blit(self.intro_text1, (50, 650))
        self.draw_cursor()

        if keys[pg.K_j] and not self.s_pressed:
            self.s_pressed = True
            self.cursor_x, self.cursor_y = 670, 650
            self.intro = False
        

    def pokemon_draw(self):
        if self.p_live:
            self.player.draw()
        if self.e_live:
            self.enemy.draw()

    def battle_logic(self):
        if self.battle:
            self.back_draw()

            if self.intro:
                self.base_ui_draw()
                self.intro()
                
            else:
                self.pokemon_draw()
                self.status_draw()
                self.base_ui_draw()
                self.draw_hp()

                self.select_logic()

            

    def back_draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.ground, (100,100))
        self.screen.blit(self.ground2, (-500,250))

    def base_ui_draw(self):
        self.screen.blit(self.ui, (-300, 620))

    def ui_1_draw(self):
        self.screen.blit(self.skill_ui, (600, 620))
        self.screen.blit(self.s_text, (50, 650))
        self.screen.blit(self.s2_text, (700, 650))
        self.screen.blit(self.s3_text, (700, 710))

    def ui_2_draw(self):
        self.s_type = set_image('asset/images/ui/type/skill/{}.png'.format(self.skill_handler.skill_list[skill_dict[self.player.pokemon.skill[self.skill-1]]].type), 3, 3)
        self.skill_text = self.player.pokemon.skill[self.skill-1]
        self.skill_text = self.font.render(self.skill_text, True, (255,255,255))
        self.damage_text = "위력 : {}".format(self.skill_handler.skill_list[skill_dict[self.player.pokemon.skill[self.skill-1]]].damage)
        self.damage_text = self.font.render(self.damage_text, True, (255,255,255))

        self.screen.blit(self.skill_ui, (600, 620))
        self.screen.blit(self.s_type, (800, 650))
        self.screen.blit(self.skill_text, (660, 650))
        self.screen.blit(self.damage_text, (660, 700))

        self.screen.blit(self.skill_1_text, (50, 650))
        self.screen.blit(self.skill_2_text, (300, 650))
        self.screen.blit(self.skill_3_text, (50, 700))
        self.screen.blit(self.skill_4_text, (300, 700))

    def ui_3_draw(self):
        self.screen.blit(self.skill_ui, (600, 620))
        

    def fight_draw(self):
        if self.p_live and self.e_live:
            keys = pg.key.get_pressed()

            self.player_skill = "{}은(는) {}을 사용했다.".format(self.player_name, self.player.pokemon.skill[self.skill - 1])
            self.player_skill_text = self.font.render(self.player_skill, True, (255,255,255))

            player_skill = skill_dict[self.player.pokemon.skill[self.skill - 1]]
            self.p_skill = self.skill_handler.skill_list[player_skill]

            if not self.p_skill.end and self.prompt1:
                self.p_skill.draw(17, 1)
            else:
                if not self.dealt:
                    result = cal_damage(self.p_skill, self.p_skill.type, self.player.pokemon.type)
                    self.enemy.pokemon.hp -= result[0]

                    self.dealt = True

                    if result[1] == 'weak':
                        self.weak = True
                    if result[1] == 'strong':
                        self.strong = True

            if self.prompt1:
                self.screen.blit(self.player_skill_text, (50, 650))
                self.weak = False
                self.strong = False

            if keys[pg.K_j] and not self.s_pressed and self.prompt1:
                self.s_pressed = True
                self.prompt1 = False
                if self.weak or self.strong:
                    self.prompt2 = True
                else:
                    self.prompt3 = True

            if not keys[pg.K_j]:
                self.s_pressed = False

            if self.prompt2:
                if self.weak:
                    skill_weak = self.font.render(self.fight_1_text, True, (255,255,255))
                    self.screen.blit(skill_weak, (50, 650))
                if self.strong:
                    skill_strong = self.font.render(self.fight_text, True, (255,255,255))
                    self.screen.blit(skill_strong, (50, 650))

            if keys[pg.K_j] and not self.s_pressed and self.prompt2:
                self.s_pressed = True
                self.prompt2 = False
                self.prompt3 = True

            if self.prompt3:
                if not self.select:
                    self.e_result = self.enemy.skill_algorithm()
                    enemy_skill = self.e_result[0]
                    enemy_skill = skill_dict[enemy_skill]
                    self.e_skill = self.skill_handler.skill_list[enemy_skill]
                    self.enemy_skill_text = "{}은(는) {}을 사용했다.".format(self.enemy_name, self.e_result[0])
                    self.enemy_skill_text = self.font.render(self.enemy_skill_text, True, (255,255,255))
                    self.select = True
                else:
                    self.screen.blit(self.enemy_skill_text, (50, 650))
                    if not self.e_skill.end:
                        self.e_skill.draw(5, 9)
                    else:
                        if not self.e_dealt:
                            self.player.pokemon.hp -= self.e_result[1][0]
                            if self.player.pokemon.hp <= 0:
                                self.fight = False
                                self.init()
                                self.second_select = True

                            if self.e_result[1][1] == 'weak':
                                self.weak = True
                            if self.e_result[1][1] == 'strong':
                                self.strong = True

                            self.e_dealt = True

            if keys[pg.K_j] and not self.s_pressed and self.prompt3 and self.e_dealt:
                self.s_pressed = True
                self.prompt3 = False
                if self.weak or self.strong:
                    self.prompt4 = True
                else:
                    self.fight = False
                    self.init()
                    self.second_select = True

            if self.prompt4:
                if self.weak:
                    skill_weak = self.font.render(self.fight_1_text, True, (255,255,255))
                    self.screen.blit(skill_weak, (50, 650))
                if self.strong:
                    skill_strong = self.font.render(self.fight_text, True, (255,255,255))
                    self.screen.blit(skill_strong, (50, 650))

            if keys[pg.K_j] and not self.s_pressed and self.prompt4:
                self.s_pressed = True
                self.prompt4 = False
                self.fight = False
                self.init()
                self.second_select = True

            if self.enemy.pokemon.hp <= 0:
                self.e_live = False
                self.prompt3 = False
                self.prompt4 = True

        else:
            self.s_pressed = False
            self.fight = False
            self.init()
                

    def init(self):
        self.prompt1 = True
        self.prompt2 = False
        self.prompt3 = False
        self.prompt4 = False
        self.weak = False
        self.strong = False
        self.fight = False
        self.dealt = False
        self.e_dealt = False
        self.select = False
        self.skill = 1
        
        self.e_skill.end = False
        self.p_skill.end = False
        self.p_skill.frame_counter = 0
        self.e_skill.frame_counter = 0

    def c_init(self):
        self.c_prompt1 = True
        self.c_prompt2 = False
        self.c_prompt3 = False
        self.c_prompt4 = False
        self.select = False

        self.p_live = True

        self.tick = True

    def ec_init(self):
        self.ec_prompt1 = True
        self.ec_prompt2 = False
        self.ec_prompt3 = False
        self.ec_prompt4 = False

        self.e_live = True

        self.e_tick = True


    def player_change(self):
        if not self.p_live:
            keys = pg.key.get_pressed()

            self.player_die_text = "{}은(는) 쓰러졌다.".format(self.player_name)
            self.player_die_text = self.font.render(self.player_die_text, True, (255,255,255))
            

            if self.c_prompt1:
                self.screen.blit(self.player_die_text, (50, 650))

            self.player2 = self.font.render(self.game.player_pokemon.pokemon_list[1].pokemon, True, (255,255,255))
            self.player3 = self.font.render(self.game.player_pokemon.pokemon_list[2].pokemon, True, (255,255,255))
            
            if self.game.player.left == 0:
                if keys[pg.K_j] and not self.s_pressed and self.c_prompt1:
                    self.s_pressed = True
                    self.c_prompt1 = False
                    self.die = True

                if not keys[pg.K_j]:
                    self.s_pressed = False

                if self.die:
                    self.battle = False

            if keys[pg.K_j] and not self.s_pressed and self.c_prompt1:
                self.s_pressed = True
                self.c_prompt1 = False
                self.c_prompt2 = True
            
            if not keys[pg.K_j]:
                self.s_pressed = False

            if self.c_prompt2:
                if self.game.player.left == 2:
                    self.screen.blit(self.player2, (50, 650))
                    self.screen.blit(self.player3, (300, 650))
                else:
                    if self.player_name == self.game.player_pokemon.pokemon_list[1].pokemon:
                        self.screen.blit(self.player3, (50, 650))
                    else:
                        self.screen.blit(self.player2, (300, 650))

            if keys[pg.K_j] and not self.s_pressed and self.c_prompt2:
                self.s_pressed = True
                self.c_prompt3 = True
                self.c_prompt2 = False
                

            if not keys[pg.K_j]:
                self.s_pressed = False
            
            if self.c_prompt3:
                self.game.player_pokemon.pokemon = self.next_pokemon
                self.player = self.game.player_pokemon
                self.player_name = self.player.pokemon.pokemon 
                self.skill_1 = self.player.pokemon.skill[0]
                self.skill_2 = self.player.pokemon.skill[1]
                self.skill_3 = self.player.pokemon.skill[2]
                self.skill_4 = self.player.pokemon.skill[3]
                self.skill_1_text = self.font.render(self.skill_1, True, (255,255,255))
                self.skill_2_text = self.font.render(self.skill_2, True, (255,255,255))
                self.skill_3_text = self.font.render(self.skill_3, True, (255,255,255))
                self.skill_4_text = self.font.render(self.skill_4, True, (255,255,255))
                self.c_prompt4 = True
                self.c_prompt3 = False

            if self.c_prompt4:
                self.player_change_text = self.font.render("나는 {}을(를) 내보냈다.".format(self.player_name), True, (255,255,255))
                self.screen.blit(self.player_change_text, (50, 650))

            if keys[pg.K_j] and not self.s_pressed and self.c_prompt4:
                self.s_pressed = True
                self.second_select = True
                self.c_init()

    def enemy_change(self):
        if not self.e_live:
            keys = pg.key.get_pressed()
            self.enemy_die_text = "{}은(는) 쓰러졌다.".format(self.enemy_name)
            self.enemy_die_text = self.font.render(self.enemy_die_text, True, (255,255,255))
                    
            if self.ec_prompt1:
                self.screen.blit(self.enemy_die_text, (50, 650))

            if self.game.enemy.left == 0:
                if keys[pg.K_j] and not self.s_pressed and self.ec_prompt1:
                    self.s_pressed = True
                    self.ec_prompt1 = False
                    self.die = True

                if not keys[pg.K_j]:
                    self.s_pressed = False

                if self.die:
                    self.battle = False

            if keys[pg.K_j] and not self.s_pressed and self.ec_prompt1:
                self.s_pressed = True
                self.ec_prompt1 = False
                self.game.enemy.pokemon += 1
                self.ec_prompt2 = True

            if not keys[pg.K_j]:
                self.s_pressed = False

            

            if self.ec_prompt2:   
                self.game.pokemon.pokemon = self.game.pokemon.pokemon_list[self.game.enemy.pokemon]
                self.enemy = self.game.pokemon
                self.enemy_name = self.enemy.pokemon.pokemon 
                self.e_skill = self.skill_handler.skill_list[0]

            if keys[pg.K_j] and not self.s_pressed and self.ec_prompt2:
                self.s_pressed = True
                self.ec_prompt3 = True
                self.ec_prompt2 = False
            
            if not keys[pg.K_j]:
                self.s_pressed = False

            if self.ec_prompt3:
                self.enemy_change_text = self.font.render("{}가 {}을(를) 내보냈다.".format(self.trainer.name, self.enemy_name), True, (255,255,255))
                self.screen.blit(self.enemy_change_text, (50, 650))

            if keys[pg.K_j] and not self.s_pressed and self.ec_prompt3:
                self.s_pressed = True
                self.second_select = True
                self.ec_init()


    def status_draw(self):
        self.p_type = set_image('asset/images/ui/type/{}.png'.format(self.player.pokemon.type), 4, 4.5)
        self.e_type = set_image('asset/images/ui/type/{}.png'.format(self.enemy.pokemon.type), 4, 5)

        self.player_lv = "lv {}".format(self.player.pokemon.level)
        self.enemy_lv = "lv {}".format(self.enemy.pokemon.level)
        p_hp = (lambda x: max(0, x))(self.player.pokemon.hp)
        e_hp = (lambda x: max(0, x))(self.enemy.pokemon.hp)
        self.player_hp = "{} / {}".format(p_hp, self.player.pokemon.max)
        self.enemy_hp = "{} / {}".format(e_hp, self.enemy.pokemon.max)

        self.p_name_text = self.font.render(self.player_name, True, (255,255,255))
        self.e_name_text = self.font.render(self.enemy_name, True, (255,255,255))
        self.p_lv_text = self.middle_font.render(self.player_lv, True, (255,255,255))
        self.e_lv_text = self.middle_font.render(self.enemy_lv, True, (255,255,255))
        self.p_hp_text = self.middle_font.render(self.player_hp, True, (255,255,255))
        self.e_hp_text = self.middle_font.render(self.enemy_hp, True, (255,255,255))

        self.screen.blit(self.p_type, (530, 480))
        self.screen.blit(self.e_type, (490, 140))

        self.screen.blit(self.player_ui, (570, 470))
        self.screen.blit(self.enemy_ui, (150, 130))
        

        self.screen.blit(self.p_name_text, (630,485))
        self.screen.blit(self.e_name_text, (180,150))

        self.screen.blit(self.p_lv_text, (820, 490))
        self.screen.blit(self.e_lv_text, (370, 155))

        self.screen.blit(self.p_hp_text, (800, 550))
        self.screen.blit(self.e_hp_text, (370, 185))

        

    def draw_hp(self):
        if  self.player.pokemon.hp > 0:
            hp_ratio = self.player.pokemon.hp / self.player.pokemon.max
            width = int(self.p_hp.get_width() * hp_ratio)

            if width > 0:
                hp = self.p_hp.subsurface((0, 0, width, self.p_hp.get_height()))
                self.screen.blit(hp, (777, 530))
        
        if  self.enemy.pokemon.hp > 0:
            e_hp_ratio = self.enemy.pokemon.hp / self.enemy.pokemon.max
            e_width = int(self.e_hp.get_width() * e_hp_ratio)

            if e_width > 0:
                e_hp = self.e_hp.subsurface((0, 0, e_width, self.e_hp.get_height()))
                self.screen.blit(e_hp, (327, 229))




    def draw_cursor(self):
        keys = pg.key.get_pressed()

        if self.intro:
            self.cursor_x = 20
            self.cursor_y = 655


        if self.first_select:
            if keys[pg.K_w] :
                self.cursor_x, self.cursor_y = 670, 650
                self.first_select_number = 1
            if keys[pg.K_s] :
                self.cursor_x, self.cursor_y = 670, 710
                self.first_select_number = 2
            

        if self.second_select:
            if keys[pg.K_w] :
                if not self.pressed:
                    if self.cursor_x == 20 and self.cursor_y == 655:
                        
                        self.cursor_x, self.cursor_y = 270, 655
                        self.skill = 2
                    
                    elif self.cursor_x == 270 and self.cursor_y == 655:
                        self.cursor_x, self.cursor_y = 20, 705
                        self.skill = 3
                    
                    elif self.cursor_x == 20 and self.cursor_y == 705:
                        self.cursor_x, self.cursor_y = 270, 705
                        self.skill = 4
                    
                    elif self.cursor_x == 270 and self.cursor_y == 705:
                        self.cursor_x, self.cursor_y = 20, 655
                        self.skill = 1
                self.pressed = True
            else:
                self.pressed = False
        
        if self.fight:
            self.cursor_x = 20
            self.cursor_y = 655
        
        if not self.p_live:
            if self.c_prompt1:
                self.cursor_x = 20
                self.cursor_y = 655
                if self.game.player.left == 1:
                    if self.player_name == self.game.player_pokemon.pokemon_list[1].pokemon:
                        self.next_pokemon = self.game.player_pokemon.pokemon_list[2]
                    else:
                        self.next_pokemon = self.game.player_pokemon.pokemon_list[1]
                else:
                    self.next_pokemon = self.game.player_pokemon.pokemon_list[1]

            if self.c_prompt2 and self.game.player.left == 2:              
                if keys[pg.K_w]:
                    if not self.pressed:
                        if self.cursor_x == 20 and self.cursor_y == 655:
                            self.cursor_x, self.cursor_y = 270, 655
                            self.next_pokemon = self.game.player_pokemon.pokemon_list[2]
                
                        elif self.cursor_x == 270 and self.cursor_y == 655:
                            self.cursor_x, self.cursor_y = 20, 655
                            self.next_pokemon = self.game.player_pokemon.pokemon_list[1]
                            

                    self.pressed = True
                else:
                    self.pressed = False

        if not self.e_live:
            self.cursor_x = 20
            self.cursor_y = 655


        self.screen.blit(self.cursor, (self.cursor_x, self.cursor_y))
            

        


    def update(self):
        self.battle_logic()

    