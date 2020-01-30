from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

import random as rand
# Instantiate spell with name, cost, dmg, type
# Black magic
thunder = Spell('Thunder', 10, 1500, 'black')
fire = Spell('Fire', 14, 2000, 'black')
blizzard = Spell('Blizzard', 19, 2500, 'black')
meteor = Spell('Meteor', 25, 3000, 'black')
quake = Spell('Quake', 32, 3500, 'black')

# White magic
cure = Spell('Cure', 12, 1200, 'white')
heal = Spell('Heal', 22, 2000, 'white')

# Instantiate item with name, type, description, prop
potion = Item('Potion', 'potion', 'Heals 75 HP', 50)
big = Item('Big Potion', 'potion', 'Heals 150 HP', 50)
pint = Item('Pint of Potion', 'potion', 'Heals 350 HP', 50)
elixir = Item('Elexir', 'potion', 'Fully restores hp and mp', 50)
megaElixir = Item('MegaElexir', 'potion',
                  'Fully restores parties hp and mp', 50)

grenade = Item('Grenade', 'attack', 'Deals 500 damage', 500)

# poison = Item('Poison', 'poison', 'Deals 25 damage per turn', 25)

player_spells = [thunder, fire, blizzard, meteor, quake, cure, heal]
player_items = [{'item': potion, 'quantity': 5},
                {'item': big, 'quantity': 4},
                {'item': pint, 'quantity': 3},
                {'item': elixir, 'quantity': 2},
                {'item': megaElixir, 'quantity': 1},
                {'item': grenade, 'quantity': 2},
                # {'item': poison, 'quantity': 4}
                ]

# Instantiate person with hp, mp, atk, df, magic
player1 = Person('Valos', 1000, 265, 1000, 35, player_spells, player_items)
player2 = Person('Tom  ', 2460, 65, 50, 35, player_spells, player_items)
player3 = Person('Mick ', 1460, 65, 50, 35, player_spells, player_items)

enemy2 = Person('Orc   ', 2500, 165, 550, 125, [], [])
enemy1 = Person('Demon ', 10000, 701, 600, 50, [], [])
enemy3 = Person('Goblin', 2500, 165, 550, 125, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True

print(bcolors.FAIL + bcolors.BOLD + 'An enemy attacks' + bcolors.ENDC)
# poison = 0

while running:
    print('===============================')
    print('\n')
    for player in players:
        player.get_stats()

    print('\n')

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        if player.get_hp() > 0:
            player.choose_actions()
            choice = input('    Choose action: ')
            index = int(choice) - 1

            # Handle Regular Attack
            if index == 0:
                dmg = player.generate_damage()
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(dmg)
                print('You attacked ' + enemies[enemy].name.strip() + ' for ' + bcolors.OKGREEN + str(dmg) +
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

                    print(bcolors.OKBLUE + '\n' + spell.name + ' deals',
                          str(magic_dmg), 'points of damage to ' + enemies[enemy].name.strip() + bcolors.ENDC)

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

                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name.strip() + ' has died.')
                        del enemies[enemy]

                # elif item.type == 'poison':
                #     poison += item.prop
                #     print(item.name + bcolors.OKGREEN +
                #           ' poisons' + bcolors.ENDC + ' the enemy for', str(item.prop), 'points.')
        else:
            break

    for enemy in enemies:
        enemy_choice = 1
        target = rand.randrange(0, 3)
        enemy_dmg = enemies[0].generate_damage()

        players[target].take_damage(enemy_dmg)

        # if poison > 0:
        #     enemy.take_damage(poison)
        #     print('Enemy attacks for ', bcolors.FAIL + enemy_dmg + ' points ' + bcolors.ENDC + 'of damage. The enemy also took ' + bcolors.ENDC +
        #           bcolors.OKGREEN + str(poison) + ' poison' + bcolors.ENDC + ' damage.')

        print('Enemy attacks ' + players[target].get_name().strip() + ' for ' + bcolors.FAIL + str(enemy_dmg) +
            ' points ' + bcolors.ENDC + 'of damage.')

    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_players == 3:
        print(bcolors.FAIL + 'Your party has died!' + bcolors.ENDC)
        running = False

    if enemy[0].get_hp() == 0:
        print(bcolors.OKGREEN + 'You win!' + bcolors.ENDC)
        running = False
