import random
from .magic import Spell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ['Attack', 'Magic', 'Items']

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_actions(self):
        i = 1
        print('\n' + '    ' + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD +
              '    Actions:' + bcolors.ENDC)
        for item in self.actions:
            print('    ' + str(i) + ':', item)
            i += 1

    def choose_magic(self):
        i = 1
        print('\n' + bcolors.OKBLUE + bcolors.BOLD + '    Magic:' + bcolors.ENDC)
        for spell in self.magic:
            if spell.type == 'black':
                text = 'damage'
            else:
                text = 'heals'

            print('    ' + str(i) + ':', spell.name, '(cost:',
                  str(spell.cost) + ', ' + text + ': ' + str(spell.dmg) + ')')
            i += 1
        print('    0: Back')

    def choose_item(self):
        i = 1
        print('\n' + bcolors.OKBLUE + bcolors.BOLD + '    ITEMS:' + bcolors.ENDC)
        for item in self.items:
            print('    ' + str(i) + ':', item['item'].name, '-',
                  item['item'].description + ' (x' + str(item['quantity']) + ')')
            i += 1
        print('    0: Back')

    def get_enemy_stats(self):
        hp_bar = ''
        bar_fill = self.hp / self.maxhp * 50

        while bar_fill > 0:
            hp_bar += '█'
            bar_fill -= 1

        while len(hp_bar) < 50:
            hp_bar += ' '

        hp_fill = len(str(self.maxhp)) - len(str(self.hp))
        hp_spacing = ''

        while hp_fill > 0:
            hp_spacing += ' '
            hp_fill -= 1

        print('                     __________________________________________________')
        print('' + bcolors.BOLD + self.name + ': ' + hp_spacing + str(self.hp) + '/' + str(self.maxhp) + ' |' + bcolors.FAIL + hp_bar +
              bcolors.ENDC + '|')

    def get_stats(self):
        hp_bar = ''
        bar_fill = self.hp / self.maxhp * 25

        while bar_fill > 0:
            hp_bar += '█'
            bar_fill -= 1

        while len(hp_bar) < 25:
            hp_bar += ' '

        mp_bar = ''
        bar_fill = self.mp / self.maxmp * 10

        while bar_fill > 0:
            mp_bar += '█'
            bar_fill -= 1

        while len(mp_bar) < 10:
            mp_bar += ' '

        hp_fill = len(str(self.maxhp)) - len(str(self.hp))
        hp_spacing = ''

        while hp_fill > 0:
            hp_spacing += ' '
            hp_fill -= 1

        mp_fill = len(str(self.maxmp)) - len(str(self.mp))
        mp_spacing = ''

        while mp_fill > 0:
            mp_spacing += ' '
            mp_fill -= 1

        top_space = ''
        str_len = len(str(self.mp) + '/' + str(self.maxmp))-5
        str_len += 7 - len(str(self.mp) + '/' + str(self.maxmp))
        while str_len > 0:
            top_space += ' '
            str_len -= 1

        mid_space = ''
        mid_len = 7 - len(str(self.mp) + '/' + str(self.maxmp))
        while mid_len > 0:
            mid_space += ' '
            mid_len -= 1

        print('                    _________________________       ' +
              top_space + '     __________')
        print('' + bcolors.BOLD + self.name + ':   ' + hp_spacing + str(self.hp) + '/' + str(self.maxhp) + ' |' + bcolors.OKGREEN + hp_bar +
              bcolors.ENDC + bcolors.BOLD + '|   ' + mp_spacing + str(self.mp) + '/' + str(self.maxmp) + mid_space + '  |' + bcolors.OKBLUE + mp_bar + bcolors.ENDC + '|')
