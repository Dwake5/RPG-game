from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

import math
import random as random

# Instantiate spell with name, cost, dmg, type
# Black magic
thunder = Spell('Thunder', 20, 300, 'black')
fire = Spell('Fire', 28, 450, 'black')
blizzard = Spell('Blizzard', 42, 600, 'black')
meteor = Spell('Meteor', 70, 800, 'black')
quake = Spell('Quake', 90, 1200, 'black')

# White magic
cure = Spell('Cure', 20, 500, 'white')
heal = Spell('Heal', 40, 800, 'white')
recover = Spell('Recover', 50, 2000, 'white')

# Instantiate item with name, type, description, prop
potion = Item('Potion', 'potion', 'Heals 200 HP', 200)
big = Item('Big Potion', 'potion', 'Heals 500 HP', 500)
pint = Item('Pint of Potion', 'potion', 'Heals 1200 HP', 1200)
elixir = Item('Elexir', 'potion', 'Fully restores hp and mp', 5000)
megaElixir = Item('MegaElexir', 'potion',
                  'Fully restores parties hp and mp', 5000)
grenade = Item('Grenade', 'attack', 'Deals 2000 damage', 2000)

player_spells = [thunder, fire, blizzard, meteor, quake, cure, heal]
player_items = [{'item': potion, 'quantity': 5},
                {'item': big, 'quantity': 4},
                {'item': pint, 'quantity': 3},
                {'item': elixir, 'quantity': 2},
                {'item': megaElixir, 'quantity': 1},
                {'item': grenade, 'quantity': 2},
                ]

# Instantiate person with hp, mp, atk, df, magic, items
player1 = Person('Valos', 1200, 260, 120, 40, player_spells, player_items)
player2 = Person('Tom  ', 2400, 150, 250, 90, player_spells, player_items)
player3 = Person('Mick ', 1600, 120, 375, 140, player_spells, player_items)

enemy1 = Person('Orc   ', 2500, 165, 250, 125, [thunder, fire], [])
enemy2 = Person('Demon ', 10000, 200, 300, 150, [blizzard, meteor, quake], [])
enemy3 = Person('Goblin', 2500, 165, 250, 125, [thunder, fire], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True

print(bcolors.FAIL + bcolors.BOLD +
      'Enemies attack, defeat the Demon to win!' + bcolors.ENDC)

while running:
    print('===============================')
    print('\n')
    for player in players:
        player.get_stats()

    print('\n')

    for enemy in enemies:
        enemy.get_enemy_stats()

    # Check if all have died
    defeated_players = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_players == 3:
        print(bcolors.FAIL + 'Your party has died!' + bcolors.ENDC)
        running = False

    for player in players:

        if player.get_hp() > 0:
            player.choose_actions()
            choice = input('    Choose action: ')
            index = int(choice) - 1

            # Handle Regular Attack
            if index == 0:
                dmg = player.generate_damage()
                enemy = player.choose_target(enemies)

                reduction = enemies[enemy].roll_defence()
                print(reduction)
                dmg = max(dmg-reduction, 0)

                enemies[enemy].take_damage(dmg)
                print(player.name.strip() + ' attacked ' + enemies[enemy].name.strip() + ' for ' + bcolors.OKGREEN + str(dmg) +
                      ' points ' + bcolors.ENDC + 'of damage.')

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.strip() + ' has died.')
                    del enemies[enemy]

            # Handle Magic Attack
            elif index == 1:
                player.choose_magic()
                magic_choice = int(input('    Choose magic: ')) - 1

                if magic_choice == -1:
                    continue

                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()

                current_mp = player.get_mp()

                if spell.cost > current_mp:
                    print(bcolors.FAIL + '\nNot enough MP\n' + bcolors.ENDC)
                    continue

                player.reduce_mp(spell.cost)

                if spell.type == 'white':
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE + spell.name + ' restores',
                          str(magic_dmg), 'hp' + bcolors.ENDC)

                elif spell.type == 'black':

                    enemy = player.choose_target(enemies)

                    enemies[enemy].take_damage(magic_dmg)

                    print(bcolors.OKBLUE + '\n' + spell.name + bcolors.ENDC + ' deals' + bcolors.FAIL +
                          str(magic_dmg) + bcolors.ENDC + 'points of damage to ' + enemies[enemy].name.strip() + bcolors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name.strip() + ' has died.')
                        del enemies[enemy]

            # Handle Item Usage
            elif index == 2:
                player.choose_item()
                item_choice = int(input('    Choose item: ')) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]['item']

                if player_items[item_choice]['quantity'] == 0:
                    print(bcolors.FAIL + '\n' + 'None left...' + bcolors.ENDC)
                    continue

                player_items[item_choice]['quantity'] -= 1

                if item.type == 'potion':
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + '\n' + item.name +
                          ' heals for', str(item.prop), 'HP' + bcolors.ENDC)

                elif item.type == 'elixir':
                    if item.name == 'MegaElixer':
                        for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                        print(bcolors.OKGREEN + '\n' + item.name +
                              'fully restores your parties HP and MP' + bcolors.ENDC)
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                        print(bcolors.OKGREEN + '\n' + item.name +
                              'fully restores your HP and MP' + bcolors.ENDC)

                elif item.type == 'attack':
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.OKGREEN + '\n' + item.name +
                          ' damages ' + enemies[enemy].name.strip() + ' for ', str(item.prop), 'HP' + bcolors.ENDC)

                # Declare and then remove an enemy if it dies
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.strip() + ' has died.')
                    del enemies[enemy]

        else:
            break

    print('\n' + 'Enemies Turn:')
    # Check if you have won (only need to defeat the 'boss')
    if enemies[1].get_hp() == 0:
        print(bcolors.OKGREEN + 'The demon has been slain. You win!' + bcolors.ENDC)
        running = False

    # Enemy attacks
    for enemy in enemies:
        enemy_choice = random.randrange(0, 10)

        # 60% chance of attacking
        if enemy_choice < 6:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.strip() + ' attacks ' + players[target].name.strip() + ' for ' + bcolors.FAIL + str(enemy_dmg) +
                  ' points ' + bcolors.ENDC + 'of damage.')

        # 40% chance of magic
        elif enemy_choice < 10:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            target = random.randrange(0, 3)
            players[target].take_damage(magic_dmg)

            print(enemy.name.strip() + "'s " + bcolors.OKBLUE + spell.name + bcolors.ENDC + ' deals ' +
                  str(magic_dmg) + ' points ' + bcolors.ENDC + 'of damage to ' + players[target].name.strip() + '.')

            if players[target].get_hp() == 0:
                print(players[target].name.strip() + ' has died.')
                del players[target]
