from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Instantiate spell with name, cost, dmg, type
# Black magic
thunder = Spell('Thunder', 10, 150, 'black')
fire = Spell('Fire', 14, 200, 'black')
blizzard = Spell('Blizzard', 19, 250, 'black')
meteor = Spell('Meteor', 25, 300, 'black')
quake = Spell('Quake', 32, 350, 'black')

# White magic
cure = Spell('Cure', 12, 120, 'white')
heal = Spell('Heal', 22, 200, 'white')

# Instantiate item with name, type, description, prop
potion = Item('Potion', 'potion', 'Heals 75 HP', 50)
big = Item('Big Potion', 'potion', 'Heals 150 HP', 50)
pint = Item('Pint of Potion', 'potion', 'Heals 350 HP', 50)
elixir = Item('Elexir', 'potion', 'Fully restores hp and mp', 50)

grenade = Item('Grenade', 'attack', 'Deals 500 damage', 500)
poison = Item('Poison', 'poison', 'Deals 25 damage per turn', 25)

# Instantiate person with hp, mp, atk, df, magic
player = Person(460, 65, 50, 35, [
                thunder, fire, blizzard, meteor, quake, cure, heal])
enemy = Person(1000, 65, 45, 25, [])

running = True

print(bcolors.FAIL + bcolors.BOLD + 'An enemy attacks' + bcolors.ENDC)

while running:
    print('===============================')
    player.choose_actions()
    choice = input('Choose action: ')
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print('You attacked for', dmg,
              'points of damage.')
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input('Choose magic: ')) - 1

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
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + '\n' + spell.name + ' deals',
                  str(magic_dmg), 'points of damage' + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print('Enemy attacks for', enemy_dmg, 'points of damage.')

    print('Enemy HP:', bcolors.FAIL + str(enemy.get_hp()) +
          '/' + str(enemy.get_max_hp()) + bcolors.ENDC)

    print('Your HP:', bcolors.OKGREEN + str(player.get_hp()) +
          '/' + str(player.get_max_hp()) + bcolors.ENDC)

    print('Your MP:', bcolors.OKGREEN + str(player.get_mp()) +
          '/' + str(player.get_max_mp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + 'You win!' + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + 'You have died!' + bcolors.ENDC)
        running = False
