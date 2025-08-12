from script.skill.shadowball import *
from script.skill.shadowpunch import *
from script.skill.crossthunder import *
from script.skill.thunder import *
from script.skill.thunderouskick import *
from script.skill.ironhead import *
from script.skill.airslash import *
from script.skill.earth import *
from script.skill.dragoncraw import *
from script.skill.darkness import *

skill_dict = {
    'thunder': 0,
    'thunderouskick': 1,
    'airslash': 2,
    'shadowball': 3,
    'shadowpunch': 4,
    'earth': 5,
    'dragoncraw': 6,
    'darkness': 7,
    'crossthunder': 8,
    'ironhead': 9
}

def get_skill_index(skill_name):
    return skill_dict.get(skill_name, -1)

def cal_damage(skill, type1, type2):
    damage = skill.damage
    add = 'none'

    if type1 == 'ghost' :
        if type2 =='normal':
            damage= 0.5 * damage
            add = 'weak'
        else:
            add = 'none'

    if type1 == 'eletric':
        if type2 == 'air':
            damage= 2.0 * damage
            add = 'strong'

    if type1 == 'steel':
        if type2 == 'eletric':
            damage= 0.5 * damage
            add = 'weak'
        else:
            add = 'none'

    if type1 == 'ground':
        if type2 == 'eletric':
            damage= 2.0 * damage
            add = 'strong'
        else:
            add = 'none'

    return damage, add

class SkillHandler:
    def __init__(self, game):
        self.game = game
        self.skill_list = [Thunder(game), Thunderouskick(game), Airslash(game), Shadowball(game), Shadowpunch(game), Earth(game), Dragoncraw(game), Darkness(game), Crossthunder(game), Ironhead(game)]