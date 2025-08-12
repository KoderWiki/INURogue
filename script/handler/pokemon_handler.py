from script.pokemon.polygon import *
from script.pokemon.rotom import *
from script.pokemon.pikachu import *
import numpy as np
from script.main.softmax import *
from script.handler.skill_hander import *


class PokemonHandler:
    def __init__(self, game):
        self.game = game
        self.enemy = self.game.enemy
        self.player = self.game.player_pokemon
        self.pokemon_list = [Polygon(game), Rotom(game), Pikachu(game)]
        self.skill_handler = SkillHandler(self.game)

        self.pokemon = self.pokemon_list[self.enemy.pokemon]

    def draw(self):
        self.pokemon.draw()

    def update(self):
        self.pokemon = self.pokemon_list[self.enemy.pokemon]
        self.pokemon.update()


    def get_state(self):
        return np.array([
            self.pokemon.hp / self.pokemon.max,
            self.player.pokemon.hp / self.player.pokemon.max,
            1.0  
        ])
    
    def skill_algorithm(self):
        state = self.get_state()

        enemy_skill_idx, probs = choose_skill(state)

        enemy_skill_name = self.pokemon.skill[enemy_skill_idx]
        enemy_skill_key = skill_dict[enemy_skill_name]
        enemy_skill = self.skill_handler.skill_list[enemy_skill_key]

        result = cal_damage(enemy_skill, enemy_skill.type, self.player.pokemon.type)

        reward = result[0]

        update_weights(state, enemy_skill_idx, reward, probs)

        self.dealt = True

        return enemy_skill_name, result
