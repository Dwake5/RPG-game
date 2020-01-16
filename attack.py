from classes.enemy import Enemy

enemy = Enemy(200, 50)
print(enemy.get_hp())

# class Enemy:
#     hp = 200

#     def __init__(self, atkl, atkh):
#         self.atkl = atkl
#         self.atkh = atkh

#     def getAtk(self):
#         print('Atk is', self.atkl)

#     def getHp(self):
#         print('Hp is', self.hp)


# enemy1 = Enemy(40, 50)
# enemy1.getAtk()
# enemy1.getHp()

# enemy2 = Enemy(50, 90)
# enemy2.getAtk()


# playerhp = 300
# enemyatklow = 30
# enermyatkhigh = 50

# while playerhp > 0:
#     dmg = random.randrange(enemyatklow, enermyatkhigh)
#     playerhp -= dmg

#     if playerhp <= 0:
#         playerhp = 0

#     print("Enemy strikes for", dmg, "points of damage. Current HP is", playerhp)

#     if playerhp > 51:
#         continue

#     print("You have low health. You've been teleported to the nearest inn.")
#     break
