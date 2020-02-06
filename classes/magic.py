import random


class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_damage(self):
        if self.type == 'white':
            return self.dmg
        else:
            low = self.dmg * 0.8
            high = self.dmg * 1.4
            return random.randrange(low, high)
