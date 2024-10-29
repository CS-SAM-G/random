# Welcome to my VERY ambitious coding project
# This is a text based dungeon crawler
# This is made with 2 weeks of coding experience
# Good luck...
# Samuel Gould 2024-08-21
# *****************************************************
# NOTES / TODO:
#
# fix random room spawn
# more play testing and balancing
#
# *****************************************************

# import time
import os
import random
import ast
import Dungeon_Crawl_Fight_Test as dungeon_fight

print("Loading...")

player_name = "Player"
player_health = 10
player_max_health = 10
player_armour = 0
player_damage = 1
player_exp = 1
player_level = 1
player_luck = 1
player_carrying = {"Weapon": None, "Armour": None, "Shield": None}
player_hit_chance = 90
distance_traveled = 0
journey_length = 100
player_inventory = {"Gold": random.randint(1, 10)}
loot_list = ["Health Potion", "Health Potion", "Health Potion", "Health Potion", "Health Potion",
             "Gold", "Gold", "Gold", "Sword", "Shield", "Armour", "Bow", "Bomb", "Nothing! What a shame..."]
greater_loot_list = ["Grand Health Potion", "Grand Health Potion", "Heart Artifact", "Magic Sword",
                     "Tempered Shield", "Magic Armour", "Elvin Bow", "Luck Potion", "Greater Bomb"]
godlike_loot_list = ["Ancient Demonic Sword", "Unbreakable Shield", "True Shot Bow", "Demon Armour",
                     "True Heart Artifact"]
basic_monster_loot_list = ["Club", "Bone Bow", "Scaled Sword", "Exo-skeleton", "Slatemail"]
intermediate_monster_loot_list = ["Knife", "Studded Armour", "Hardened Exo-skeleton", "Gemstone", "Hounds Fang"]
expert_monster_loot_list = ["Tainted Sword", "Broken Magma Fang", "Obsidian Plate", "Corrupted Bow"]
boss_monster_loot_list = ["Blood-Soaked Axe", "Dragon-Scale Armour", "Beast Bow", "Starlight Bow", "Holy Blade"]

with open('two_path_room.txt', 'r') as open_file:
    line = open_file.readline()
    two_path_descriptions = []
    while line:
        line = line.replace('\n', '')
        two_path_descriptions.append(line)
        line = open_file.readline()

with open('three_path_room.txt', 'r') as open_file:
    line = open_file.readline()
    three_path_descriptions = []
    while line:
        line = line.replace('\n', '')
        three_path_descriptions.append(line)
        line = open_file.readline()

with open('continue_pathway.txt', 'r') as open_file:
    line = open_file.readline()
    continue_pathway_text = []
    while line:
        line = line.replace('\n', '')
        continue_pathway_text.append(line)
        line = open_file.readline()

with open('continue_on.txt', 'r') as open_file:
    line = open_file.readline()
    continue_on_text = []
    while line:
        line = line.replace('\n', '')
        continue_on_text.append(line)
        line = open_file.readline()

with open('enemy_approaching.txt', 'r') as open_file:
    line = open_file.readline()
    enemy_approaching_text = []
    while line:
        line = line.replace('\n', '')
        enemy_approaching_text.append(line)
        line = open_file.readline()

with open('random_events.txt', 'r') as open_file:
    line = open_file.readline()
    random_events_text = []
    while line:
        line = line.replace('\n', '')
        random_events_text.append(line)
        line = open_file.readline()

print("Loaded files.")


# Use this function to clear screen of all text
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Will pick between 2 and 3 directions for a path to split into
# Gets user input of direction they want to go, and return that input
def get_direction():
    global two_path_descriptions
    global three_path_descriptions
    description_of_path = ""
    # picks number of paths
    num_of_paths = random.randint(2, 3)
    if distance_traveled == 0:
        clear_screen()
        clear_screen()
        clear_screen()
        if num_of_paths == 2:
            description_of_path = ("           You begin your adventure stepping into a cave"
                                   "\n     Your torch casting flickering shadows on damp, uneven walls."
                                   "\nThe air is cool and musty, and the passages ahead disappears into darkness."
                                   "\n            With a mix of excitement and apprehension"
                                   "\n            You begin your adventure into the unknown."
                                   "\n"
                                   "\nThere are two paths in front of you. "
                                   "Which will you take to start your journey?")
        elif num_of_paths == 3:
            description_of_path = ("           You begin your adventure stepping into a cave"
                                   "\n     Your torch casting flickering shadows on damp, uneven walls."
                                   "\nThe air is cool and musty, and the passages ahead disappears into darkness."
                                   "\n            With a mix of excitement and apprehension"
                                   "\n            You begin your adventure into the unknown."
                                   "\n"
                                   "\nThere are thee paths in front of you. "
                                   "Which will you take to start your journey?")
    else:
        if num_of_paths == 2:
            description_of_path = random.choice(two_path_descriptions)
        elif num_of_paths == 3:
            description_of_path = random.choice(three_path_descriptions)

    # assigns a list with each option
    options = ['left', 'right', 'straight']

    # creates empty list to store random choices
    choices = []

    # fills empty list with random choices if they are not in list already
    for i in range(num_of_paths):
        while True:
            random_choice = random.choice(options)
            if random_choice not in choices:
                choices.append(random_choice)
                break

    # Writes different options depending on amount of choices
    if num_of_paths == 2:
        while True:
            print(description_of_path)
            direction = input(choices[0] + " or "
                              + choices[1] + "?: ").lower()

            # if input is valid, return choice. else, repeat
            if direction in choices:
                clear_screen()
                return direction
            else:
                clear_screen()
                print("Invalid option.")
    else:
        while True:
            print(description_of_path)
            direction = input(choices[0] + ", "
                              + choices[1] + " or "
                              + choices[2] + "?: ").lower()
            if direction in choices:
                clear_screen()
                return direction
            else:
                clear_screen()
                print("Invalid option.")


def dungeon_travel(direction):
    global distance_traveled, player_exp
    print("You continue " + direction + ".\n")
    length_of_path = random.randint(2, 10)
    walked_distance = 0
    while walked_distance < length_of_path + 1:
        if distance_traveled == 50 or distance_traveled == 100 or distance_traveled == 150\
                or distance_traveled == 200 or distance_traveled == 250\
                or distance_traveled == 300:
            spawn_boss_room()
        room_spawn(spawn_rate())
        player_action()
        walked_distance += 1
        distance_traveled += 1
        player_exp += 1


# returns 1 in x chance for spawning either loot or encounter
def spawn_rate():
    if 30 >= distance_traveled:
        return 10
    elif 30 < distance_traveled < 75:
        return 7
    elif 75 <= distance_traveled < 150:
        return 6
    else:
        return 5

def go_back():
    global distance_traveled
    if distance_traveled < 50:
        distance_traveled = 0
    elif distance_traveled < 100:
        distance_traveled = 51
    elif distance_traveled < 150:
        distance_traveled = 101
    elif distance_traveled < 200:
        distance_traveled = 151
    elif distance_traveled < 250:
        distance_traveled = 201
    elif distance_traveled < 300:
        distance_traveled = 251

    clear_screen()
    print("You travel back to explore more!\n")
    input("Press enter to continue.")
    clear_screen()


def check_level_up():
    global player_health, player_max_health, player_armour, player_exp, player_level, player_damage
    if player_exp >= player_level * 50:
        clear_screen()
        health_bonus = random.randint(3, 5)
        damage_bonus = random.randint(0, 2)
        armour_bonus = random.randint(0, 2)
        print("You have leveled up!")
        print("Max Health +", health_bonus)
        if damage_bonus != 0:
            print("Base Damage +", damage_bonus)
        if armour_bonus != 0:
            print("Base Armour +", armour_bonus)
        player_level += 1
        player_armour += armour_bonus
        player_max_health += health_bonus
        player_health = player_max_health
        player_damage += damage_bonus
        player_exp = 0
        input("Press Enter to continue...")
        clear_screen()


# LOOT TO ADD
#  "Exo-skeleton" "Studded Armor" "Hardened Exo-skeleton", "Dragon-Scale Armour"

#
# How to add:
# Add in weapon category
# Add in respective shield or bow category if applicable
# Add in damage / armour
# add in damage /armour removal

def item_equip(weapon_or_armour_or_shield):
    global player_carrying, player_armour, player_damage, player_inventory, player_hit_chance
    clear_screen()
    if (weapon_or_armour_or_shield == "Sword" or weapon_or_armour_or_shield == "Bow"
            or weapon_or_armour_or_shield == "Magic Sword"
            or weapon_or_armour_or_shield == "Elvin Bow"
            or weapon_or_armour_or_shield == "Ancient Demonic Sword"
            or weapon_or_armour_or_shield == "True Shot Bow"
            or weapon_or_armour_or_shield == "Club"
            or weapon_or_armour_or_shield == "Bone Bow"
            or weapon_or_armour_or_shield == "Scaled Sword"
            or weapon_or_armour_or_shield == "Knife"
            or weapon_or_armour_or_shield == "Hounds Fang"
            or weapon_or_armour_or_shield == "Tainted Sword"
            or weapon_or_armour_or_shield == "Broken Magma Fang"
            or weapon_or_armour_or_shield == "Corrupted Bow"
            or weapon_or_armour_or_shield == "Blood-Soaked Axe"
            or weapon_or_armour_or_shield == "Beast Bow"
            or weapon_or_armour_or_shield == "Starlight Bow"
            or weapon_or_armour_or_shield == "Holy Blade"):

        if player_carrying.get("Shield") is not None:
            if (weapon_or_armour_or_shield == "Bow"
                    or weapon_or_armour_or_shield == "Elvin Bow"
                    or weapon_or_armour_or_shield == "True Shot Bow"
                    or weapon_or_armour_or_shield == "Bone Bow"
                    or weapon_or_armour_or_shield == "Corrupted Bow"
                    or weapon_or_armour_or_shield == "Beast Bow"
                    or weapon_or_armour_or_shield == "Starlight Bow"):
                print("You cannot carry a bow and a shield at the same time.")
                print("Shield has been unequipped.")
                input("Press Enter to continue.")
                inventory_add(player_carrying.get("Shield"))
                if player_carrying.get("Shield") == "Shield":
                    player_armour -= 1
                elif player_carrying.get("Shield") == "Tempered Shield":
                    player_armour -= 4
                elif player_carrying.get("Shield") == "Unbreakable Shield":
                    player_armour -= 8
                elif player_carrying.get("Shield") == "Obsidian Plate":
                    player_armour -= 7
                player_carrying.update({"Shield": None})

        if player_carrying.get("Weapon") is not None:
            inventory_add(player_carrying.get("Weapon"))
            if player_carrying.get("Weapon") == "Sword":
                player_damage -= 3
            elif player_carrying.get("Weapon") == "Bow":
                player_damage -= 4
            elif player_carrying.get("Weapon") == "Magic Sword":
                player_damage -= 8
            elif player_carrying.get("Weapon") == "Elvin Bow":
                player_damage -= 9
            elif player_carrying.get("Weapon") == "Ancient Demonic Sword":
                player_damage -= 16
            elif player_carrying.get("Weapon") == "True Shot Bow":
                player_damage -= 18
            elif player_carrying.get("Weapon") == "Club":
                player_damage -= 2
            elif player_carrying.get("Weapon") == "Bone Bow":
                player_damage -= 3
            elif player_carrying.get("Weapon") == "Scaled Sword":
                player_damage -= 4
            elif player_carrying.get("Weapon") == "Knife":
                player_damage -= 6
            elif player_carrying.get("Weapon") == "Hounds Fang":
                player_damage -= 7
            elif player_carrying.get("Weapon") == "Tainted Sword":
                player_damage -= 8
            elif player_carrying.get("Weapon") == "Broken Magma Fang":
                player_damage -= 9
            elif player_carrying.get("Weapon") == "Corrupted Bow":
                player_damage -= 10
            elif player_carrying.get("Weapon") == "Blood-Soaked Axe":
                player_damage -= 10
            elif player_carrying.get("Weapon") == "Beast Bow":
                player_damage -= 13
            elif player_carrying.get("Weapon") == "Starlight Bow":
                player_damage -= 15
            elif player_carrying.get("Weapon") == "Holy Blade":
                player_damage -= 18

            player_carrying.update({"Weapon": weapon_or_armour_or_shield})
        else:
            player_carrying.update({"Weapon": weapon_or_armour_or_shield})

        if player_inventory.get(weapon_or_armour_or_shield) > 1:
            player_inventory[weapon_or_armour_or_shield] -= 1
        elif player_inventory.get(weapon_or_armour_or_shield) == 1:
            player_inventory.pop(weapon_or_armour_or_shield)

        if weapon_or_armour_or_shield == "Sword":
            player_damage += 3
            player_hit_chance = 80
        elif weapon_or_armour_or_shield == "Bow":
            player_damage += 4
            player_hit_chance = 70
        elif weapon_or_armour_or_shield == "Magic Sword":
            player_damage += 8
            player_hit_chance = 85
        elif weapon_or_armour_or_shield == "Elvin Bow":
            player_damage += 9
            player_hit_chance = 75
        elif weapon_or_armour_or_shield == "Ancient Demonic Sword":
            player_damage += 16
            player_hit_chance = 90
        elif weapon_or_armour_or_shield == "True Shot Bow":
            player_damage += 18
            player_hit_chance = 95
        elif player_carrying.get("Weapon") == "Club":
            player_damage += 2
            player_hit_chance = 70
        elif player_carrying.get("Weapon") == "Bone Bow":
            player_damage += 3
            player_hit_chance = 65
        elif player_carrying.get("Weapon") == "Scaled Sword":
            player_damage += 4
            player_hit_chance = 75
        elif player_carrying.get("Weapon") == "Knife":
            player_damage += 6
            player_hit_chance = 85
        elif player_carrying.get("Weapon") == "Hounds Fang":
            player_damage += 7
            player_hit_chance = 75
        elif player_carrying.get("Weapon") == "Tainted Sword":
            player_damage += 8
            player_hit_chance = 80
        elif player_carrying.get("Weapon") == "Broken Magma Fang":
            player_damage += 9
            player_hit_chance = 75
        elif player_carrying.get("Weapon") == "Corrupted Bow":
            player_damage += 10
            player_hit_chance = 70
        elif player_carrying.get("Weapon") == "Blood-Soaked Axe":
            player_damage += 10
            player_hit_chance = 75
        elif player_carrying.get("Weapon") == "Beast Bow":
            player_damage += 13
            player_hit_chance = 80
        elif player_carrying.get("Weapon") == "Starlight Bow":
            player_damage += 15
            player_hit_chance = 75
        elif player_carrying.get("Weapon") == "Holy Blade":
            player_damage += 18
            player_hit_chance = 75

        clear_screen()
        return True
    #  "Exo-skeleton" "Studded Armor" "Hardened Exo-skeleton", "Dragon-Scale Armour"
    elif (weapon_or_armour_or_shield == "Armour"
          or weapon_or_armour_or_shield == "Magic Armour"
          or weapon_or_armour_or_shield == "Demon Armour"
          or weapon_or_armour_or_shield == "Slatemail"
          or weapon_or_armour_or_shield == "Exo-skeleton"
          or weapon_or_armour_or_shield == "Studded Armour"
          or weapon_or_armour_or_shield == "Hardened Exo-skeleton"
          or weapon_or_armour_or_shield == "Dragon-Scale Armour"):

        if player_carrying.get("Armour") is not None:
            inventory_add(player_carrying.get("Armour"))
            if player_carrying.get("Armour") == "Armour":
                player_armour -= 2
            elif player_carrying.get("Armour") == "Magic Armour":
                player_armour -= 6
            elif player_carrying.get("Armour") == "Demon Armour":
                player_armour -= 15
            elif player_carrying.get("Armour") == "Slatemail":
                player_armour -= 1
            elif player_carrying.get("Armour") == "Exo-skeleton":
                player_armour -= 2
            elif player_carrying.get("Armour") == "Studded Armour":
                player_armour -= 3
            elif player_carrying.get("Armour") == "Hardened Exo-skeleton":
                player_armour -= 5
            elif player_carrying.get("Armour") == "Dragon-Scale Armour":
                player_armour -= 13
            player_carrying.update({"Armour": weapon_or_armour_or_shield})
        else:
            player_carrying.update({"Armour": weapon_or_armour_or_shield})

        if player_inventory.get(weapon_or_armour_or_shield) > 1:
            player_inventory[weapon_or_armour_or_shield] -= 1
        elif player_inventory.get(weapon_or_armour_or_shield) == 1:
            player_inventory.pop(weapon_or_armour_or_shield)

        if weapon_or_armour_or_shield == "Armour":
            player_armour += 2
        elif weapon_or_armour_or_shield == "Magic Armour":
            player_armour += 6
        elif weapon_or_armour_or_shield == "Demon Armour":
            player_armour += 15
        elif weapon_or_armour_or_shield == "Slatemail":
            player_armour += 1
        elif weapon_or_armour_or_shield  == "Exo-skeleton":
            player_armour += 2
        elif weapon_or_armour_or_shield  == "Studded Armour":
            player_armour += 3
        elif weapon_or_armour_or_shield  == "Hardened Exo-skeleton":
            player_armour += 5
        elif weapon_or_armour_or_shield == "Dragon-Scale Armour":
            player_armour += 13

        clear_screen()
        return True
    elif (weapon_or_armour_or_shield == "Shield"
          or weapon_or_armour_or_shield == "Tempered Shield"
          or weapon_or_armour_or_shield == "Unbreakable Shield"
          or weapon_or_armour_or_shield == "Obsidian Plate"):

        if (player_carrying.get("Weapon") == "Bow" #MISSING***********************************
                or player_carrying.get("Weapon") == "Elvin Bow"
                or player_carrying.get("Weapon") == "True Shot Bow"
                or player_carrying.get("Weapon") == "Bone Bow"
                or player_carrying.get("Weapon") == "Corrupted Bow"
                or player_carrying.get("Weapon") == "Beast Bow"
                or player_carrying.get("Weapon") == "Starlight Bow"):
            print("You cannot carry a bow and a shield at the same time.")
            print("Bow has been unequipped.")
            input("Press Enter to continue.")
            inventory_add(player_carrying.get("Weapon"))
            if player_carrying.get("Weapon") == "Bow":
                player_damage -= 4
            elif player_carrying.get("Weapon") == "Elvin Bow":
                player_damage -= 9
            elif player_carrying.get("Weapon") == "True Shot Bow":
                player_damage -= 18
            elif player_carrying.get("Weapon") == "Bone Bow":
                player_damage -= 3
            elif player_carrying.get("Weapon") == "Corrupted Bow":
                player_damage -= 10
            elif player_carrying.get("Weapon") == "Beast Bow":
                player_damage -= 13
            elif player_carrying.get("Weapon") == "Starlight Bow":
                player_damage -= 15
            player_carrying.update({"Weapon": None})

        if player_carrying.get("Shield") is not None:
            inventory_add(player_carrying.get("Shield"))
            if player_carrying.get("Shield") == "Shield":
                player_armour -= 1
            elif player_carrying.get("Shield") == "Tempered Shield":
                player_armour -= 4
            elif player_carrying.get("Shield") == "Unbreakable Shield":
                player_armour -= 8
            elif player_carrying.get("Shield") == "Obsidian Plate":
                player_armour -= 7
            player_carrying.update({"Shield": weapon_or_armour_or_shield})
        else:
            player_carrying.update({"Shield": weapon_or_armour_or_shield})

        if player_inventory.get(weapon_or_armour_or_shield) > 1:
            player_inventory[weapon_or_armour_or_shield] -= 1
        elif player_inventory.get(weapon_or_armour_or_shield) == 1:
            player_inventory.pop(weapon_or_armour_or_shield)

        if weapon_or_armour_or_shield == "Shield":
            player_armour += 1
        elif weapon_or_armour_or_shield == "Tempered Shield":
            player_armour += 4
        elif weapon_or_armour_or_shield == "Unbreakable Shield":
            player_armour += 8
        elif weapon_or_armour_or_shield == "Obsidian Plate":
            player_armour += 7
        clear_screen()
        return True
    else:
        clear_screen()
        return False


def player_action(option=""):
    global player_health, player_max_health, player_armour, player_exp, player_luck, player_level, player_damage
    action = ""
    while True:
        if option == "":
            action = input("What would you like to do? (Enter to continue): ").lower()
            clear_screen()
        elif (option in loot_list or option in greater_loot_list
              or option in godlike_loot_list or option in basic_monster_loot_list
              or option in intermediate_monster_loot_list or option in expert_monster_loot_list
              or option in boss_monster_loot_list):
            if option != "Nothing! What a shame...":
                inventory_add(option)
                input("Successfully added to inventory.")
            else:
                input("Press Enter to continue.")
            clear_screen()
            break

        if action == "help":
            print("\nAction list: \n"
                  "stats - Shows current player stats.\n"
                  "inventory - Shows current player inventory.\n"
                  "heal - Uses health potion.\n"
                  "grand heal - Uses grand health potion.\n"
                  "luck - Uses luck potion.\n"
                  'go back - Backtrack til just after last boss'
                  "save - Saves your game.\n"
                  "quit - Quits game.\n")

        elif action == "stats":
            print("******** Stats ********")

            print("Level: " + str(player_level) + " | HP:", player_health, "/", player_max_health, )
            print("Damage Rating: " + str(player_damage) + " | Armour Rating:", player_armour)
            if player_level * 50 - player_exp > 0:
                print("EXP: " + str(player_exp) + " | EXP til next level: ", player_level * 50 - player_exp)
            else:
                print("EXP: " + str(player_exp) + " | EXP til next level: 0")
                print("You will level shortly...")
            print("Distance Traveled: " + str(distance_traveled)+ " | ", end='')
            if player_luck == 2:
                print("You\'re feelin\' lucky!")
            elif player_luck == 1:
                print("You have normal luck.")
            elif player_luck == 0:
                print("You have bad luck!")
            input("\nPress enter to continue.")
            clear_screen()

        elif action == "inventory":
            while True:
                print("In bag:")
                for items in player_inventory:
                    print(items + ":", player_inventory[items])
                print("\nCarrying:")
                for items in player_carrying:
                    if player_carrying.get(items) is not None:
                        print(player_carrying.get(items))
                equip_action = input("\nPress enter to continue or type 'Item Name' to equip: ")
                if equip_action in player_inventory:
                    if item_equip(equip_action):
                        print("You equipped: " + equip_action + ".")
                        input("Press Enter to continue.")
                        clear_screen()
                    else:
                        print("You can only equip a Weapon, Shield, or Armor.")
                elif equip_action == "":
                    clear_screen()
                    break
                else:
                    clear_screen()
                    print("Invalid action.")

        elif action == "heal":
            if player_inventory.get("Health Potion") is None:
                print("You have no Health Potions.")
            else:
                if player_inventory.get("Health Potion") > 1:
                    player_inventory["Health Potion"] -= 1
                    if player_health >= player_max_health - 10:
                        player_health = player_max_health
                        print("Healed 10 HP!")
                    else:
                        player_health += 10
                        print("Healed 10 HP!")
                elif player_inventory.get("Health Potion") == 1:
                    player_inventory.pop("Health Potion")
                    if player_health >= player_max_health - 10:
                        player_health = player_max_health
                        print("Healed 10 HP!")
                    else:
                        player_health += 10
                        print("Healed 10 HP!")
            input("\nPress enter to continue.")
            clear_screen()

        elif action == "grand heal":
            if player_inventory.get("Grand Health Potion") is None:
                print("You have no Grand Health Potions.")
            else:
                if (player_inventory.get("Grand Health Potion") > 1
                        and player_inventory.get("Grand Health Potion") is not None):
                    player_inventory["Grand Health Potion"] -= 1
                    player_health = player_max_health
                    print("Fully healed!")
                elif (player_inventory.get("Grand Health Potion") == 1
                      and player_inventory.get("Grand Health Potion") is not None):
                    player_inventory.pop("Grand Health Potion")
                    player_health = player_max_health
                    print("Fully healed!")
            input("\nPress enter to continue.")
            clear_screen()

        elif action == "luck":
            if player_inventory.get("Luck Potion") is None:
                print("You have no Luck Potions.")
            else:
                if player_inventory.get("Luck Potion") > 1 and player_inventory.get("Luck Potion") is not None:
                    player_inventory["Luck Potion"] -= 1
                    player_luck = 2
                    print("You begin feeling lucky!")
                elif player_inventory.get("Luck Potion") == 1 and player_inventory.get("Luck Potion") is not None:
                    player_inventory.pop("Luck Potion")
                    player_luck = 2
                    print("You begin feeling lucky!")
            input("\nPress enter to continue.")
            clear_screen()

        elif action == 'go back':
            go_back()

        elif action == "save":
            save_game()
            input("Game saved successfully.")
            clear_screen()

        elif action == "quit":
            clear_screen()
            print("You may want to save first!")
            possible_quit = input("Are you sure you want to quit? (y/n): ")
            if possible_quit.lower() == "y":
                clear_screen()
                input("Thank you for playing!\nPress enter to quit.")
                clear_screen()
                exit()
            clear_screen()

        elif action == "":
            break


def save_game():
    global player_name, player_health, player_max_health, player_armour, player_damage, player_exp
    global player_level, player_luck, player_carrying, player_hit_chance
    global distance_traveled, journey_length, player_inventory
    save_list = [player_name, player_health, player_max_health, player_armour, player_damage, player_exp,
                 player_level, player_luck, player_carrying, player_hit_chance,
                 distance_traveled, journey_length, player_inventory]
    open_save_file = open('dungeon_crawler_save_file.txt', 'w')
    for ids in save_list:
        open_save_file.write(str(ids) + "\n")
    open_save_file.close()


def inventory_add(item):
    global player_max_health
    global player_health
    if item == "Nothing! What a shame...":
        print()
    elif item == "Heart Artifact":
        player_max_health += 5
        player_health = player_max_health
    elif item == "True Heart Artifact":
        player_max_health += 10
        player_health = player_max_health
    elif player_inventory.get(item) is None and item != "Gold":
        player_inventory.update({item: 1})
    elif player_inventory.get(item) is None and item == "Gold":
        player_inventory.update({item: 5})
    elif item == "Gold":
        player_inventory[item] += 5
    else:
        player_inventory[item] += 1


def spawn_loot_room():
    print("You come across a room with 3 chests!")
    loot = random_loot()
    print("Chest 1 contains: " + loot)
    player_action(loot)
    loot = random_loot()
    print("Chest 2 contains: " + loot)
    player_action(loot)
    loot = random_loot()
    print("Chest 3 contains: " + loot)
    player_action(loot)


# picks a random number, if it is outside of list, picks an item from a better loot pool
def random_loot():
    random_pick = random.randint(0, len(loot_list))
    if random_pick == len(loot_list):
        random_pick = random.randint(0, len(greater_loot_list))
        if random_pick == len(greater_loot_list):
            return godlike_loot_list[random.randint(0, len(godlike_loot_list) - 1)]
        else:
            return greater_loot_list[random_pick]
    else:
        return loot_list[random_pick]


def spawn_enemy_room():
    global player_health, player_max_health, player_armour, player_damage, player_exp, \
        player_level, player_carrying, player_hit_chance, distance_traveled, player_inventory
    print(random.choice(enemy_approaching_text))
    print("There is danger ahead!")
    input("Press enter to fight!")
    clear_screen()
    dungeon_fight.player_fight_setup(player_name, player_health, player_max_health, player_armour,
                                     player_damage, player_exp, player_level, player_carrying,
                                     player_hit_chance, distance_traveled, player_inventory)

    (player_health, player_max_health, player_armour, player_damage, player_exp,
     player_level, player_carrying, player_hit_chance,
     distance_traveled, player_inventory) = dungeon_fight.dungeon_fight_sequence()


def spawn_boss_room():
    global player_health, player_max_health, player_armour, player_damage, player_exp, \
        player_level, player_carrying, player_hit_chance, distance_traveled, player_inventory
    if distance_traveled == 50:
        print("You step into a cavernous chamber, the air grows cold and thick with an unsettling silence...\n"
              "        In the center stands a grotesque figure, both mesmerizing and horrifying...\n"
              "A body split down the center, twisting and turning as the cleaved sides join at the waist...\n"
              "                 And a head, that floats detached from her body...\n"
              "Her sunken, dead eyes quickly lock onto you, sending a shiver down your spine...\n")
    elif distance_traveled == 100:
        print("")
    elif distance_traveled == 150:
        print("")
    elif distance_traveled == 200:
        print("")
    elif distance_traveled == 250:
        print("")
    elif distance_traveled == 300:
        print("")

    print("I hope you're ready for this...")
    input("Press enter to fight!")
    clear_screen()
    dungeon_fight.player_fight_setup(player_name, player_health, player_max_health, player_armour,
                                     player_damage, player_exp, player_level, player_carrying,
                                     player_hit_chance, distance_traveled, player_inventory)

    (player_health, player_max_health, player_armour, player_damage, player_exp,
     player_level, player_carrying, player_hit_chance,
     distance_traveled, player_inventory) = dungeon_fight.dungeon_fight_sequence()


def spawn_random_event():
    global player_luck, player_exp, player_health, player_max_health, distance_traveled, player_damage
    event_choice = random.randint(1, 10)
    if event_choice == 1:
        random_text = random.randint(0, 4)
        print(random_events_text[random_text])
        while True:
            choice_answer = input("Do you touch it? (y/n):").lower()
            clear_screen()
            if choice_answer == "y":
                clear_screen()
                if random.randint(player_luck, 3) == 3:
                    exp_gain = int(player_level * 50 / 3)
                    print(f"You gained otherworldly knowledge!\nExp + " + str(exp_gain) + "!")
                    player_exp += exp_gain
                    if player_luck == 2:
                        print("Your luck saved you!")
                        player_luck = 1
                    else:
                        print("You\'re feeling lucky!")
                        player_luck = 2
                    input("Press enter to continue.")
                    clear_screen()
                    break
                else:
                    print("It was a trap!\nYou've been cursed with bad luck!")
                    player_luck = 0
                input("Press enter to continue.")
                clear_screen()
                break
            elif choice_answer == "n":
                print("Perhaps it\'s better left alone...")
                input("Press enter to continue.")
                clear_screen()
                break
            else:
                print("Invalid input.")
                input("Press enter to continue.")
                clear_screen()

    elif event_choice == 2:
        random_text = random.randint(5, 9)
        print(random_events_text[random_text])
        input("Press enter to continue...")
        clear_screen()
        if random.randint(player_luck, 3) == 3:
            print("You slowly awaken and find that something had gone through your gear\n"
                  "It seems they didn\'t find what they were looking for!")
            if player_luck == 2:
                print("Your luck saved you!")
                player_luck = 1
            else:
                print("You\'re feeling lucky!")
                player_luck = 2
        else:
            print("You slowly awaken and find that something had gone through your gear.")
            item_lost_list = []
            for lost_items in player_inventory:
                if lost_items != "Gold":
                    item_lost_list.append(lost_items)
            if not item_lost_list:
                print("You didn\'t have much... So they took your gold!")
                player_inventory["Gold"] = 0
            else:
                item_lost = random.choice(item_lost_list)
                print("You lost: " + item_lost)
                if player_inventory.get(item_lost) > 1:
                    player_inventory[item_lost] -= 1
                else:
                    player_inventory.pop(item_lost)
            if player_luck == 0:
                print("Your bad luck has ended!")
                player_luck = 1

        input("Press enter to continue.")
        clear_screen()

    elif event_choice == 3:
        random_text = random.randint(10, 14)
        print(random_events_text[random_text])
        input("Press enter to continue...")
        clear_screen()
        if random.randint(player_luck, 3) == 3:
            gold_reward = random.randint(5, 15)
            print("You found", gold_reward, "gold!")
            player_inventory["Gold"] += gold_reward
            if player_luck == 2:
                print("Your luck saved you!")
                player_luck = 1
            else:
                print("You\'re feeling lucky!")
                player_luck = 2
        else:
            if random.randint(1, 2) == 1:
                print("You find nothing but rocks and dirt...")
            else:
                print("A scorpion bites your hand as you reach in!")
                print("-1 HP!")
                player_health -= 1
            if player_luck == 0:
                print("Your bad luck has ended!")
                player_luck = 1
        input("Press enter to continue.")
        if player_health <= 0:
            game_over()
        clear_screen()

    elif event_choice == 4:
        random_text = random.randint(15, 19)
        print(random_events_text[random_text])
        input("Press enter to continue...")
        clear_screen()
        if random.randint(player_luck, 3) == 3:
            print("You find yourself slowly drifting off, and you enjoy a nice nap.")
            print("You fully recovered your HP!")
            player_health = player_max_health
            if player_luck == 2:
                print("Your luck saved you!")
                player_luck = 1
            else:
                print("You\'re feeling lucky!")
                player_luck = 2
        else:
            print("After a brief moment, a sudden noise sends shivers down your spine!")
            print("You are unable to rest, and continue on...")
            print("You\'ve got bad luck!")
            player_luck = 0
        input("Press enter to continue.")
        clear_screen()

    elif event_choice == 5:
        random_text = random.randint(20, 24)
        print(random_events_text[random_text])
        input("Press enter to continue...")
        clear_screen()
        if random.randint(player_luck, 3) == 3:
            print("You manage to jump to safety at the last second!")
            # PLAYER REWARD
            if player_luck == 2:
                print("Your luck saved you!")
                player_luck = 1
            else:
                print("You\'re feeling lucky!")
                player_luck = 2
        else:
            print("You don\'t manage to escape in time!")
            damage_from_trap = random.randint(1, player_health + 1)
            print("You take " + str(damage_from_trap) + " damage!")
            player_health -= damage_from_trap
            if player_luck == 0:
                print("Your bad luck has ended!")
                player_luck = 1
        input("Press enter to continue.")
        if player_health <= 0:
            game_over()
        clear_screen()

    elif event_choice == 6:
        random_text = random.randint(25, 29)
        print(random_events_text[random_text])
        input("Press enter to continue...")
        clear_screen()
        if random.randint(player_luck, 3) == 3:
            print("You manage to find your way, and you feel a bit smarter too!")
            exp_gain = int(player_level * 50 / 6)
            print("You gained " + str(exp_gain) + " Exp!")
            player_exp += exp_gain
            if player_luck == 2:
                print("Your luck saved you!")
                player_luck = 1
            else:
                print("You\'re feeling lucky!")
                player_luck = 2
        else:
            print("You\'re lost!")
            distance_lost = random.randint(1, int(distance_traveled / 4))
            print("By the time you realize, you've gone back " + str(distance_lost) + " steps!")
            distance_traveled -= distance_lost
            if player_luck == 0:
                print("Your bad luck has ended!")
                player_luck = 1
        input("Press enter to continue.")
        clear_screen()

    elif event_choice == 7:
        random_text = random.randint(30, 34)
        print(random_events_text[random_text])
        while True:
            choice_answer = input("Do you touch it? (y/n):").lower()
            clear_screen()
            if choice_answer == "y":
                if random.randint(player_luck, 4) == 3:
                    print("You feel a warm feeling rush over your body as you touch the artifact!")
                    artifact_reward = random.randint(1, 3)
                    player_max_health += artifact_reward
                    player_health = player_max_health
                    print("Your max health has been increased by " + str(artifact_reward) + "!")
                    artifact_reward = random.randint(5, 15)
                    player_inventory["Gold"] += artifact_reward
                    print("You gained " + str(artifact_reward) + " Gold!")
                    print("\nThe artifact slowly fades away...\n")
                    if player_luck == 2:
                        print("Your luck saved you!")
                        player_luck = 1
                    else:
                        print("You\'re feeling lucky!")
                        player_luck = 2
                else:
                    print("You\'r vision goes blurry as you feel energy being sapped away from you!")
                    artifact_reward = random.randint(2, 5)
                    player_max_health -= artifact_reward
                    if player_health > player_max_health:
                        player_health = player_max_health
                    print("Your max health has been decreased by " + str(artifact_reward) + "!")
                    artifact_reward = random.randint(5, 15)
                    player_inventory["Gold"] -= artifact_reward
                    if player_inventory["Gold"] < 0:
                        player_inventory["Gold"] = 0
                    print("You lost " + str(artifact_reward) + " Gold!")
                    print("\nThe cursed object slowly fades away with a black cloud of smoke...\n")
                    if player_luck == 0:
                        print("Your bad luck has ended!")
                        player_luck = 1
                input("Press enter to continue.")
                if player_health <= 0:
                    game_over()
                clear_screen()
                break
            elif choice_answer == "n":
                print("Perhaps it\'s better left alone...")
                input("Press enter to continue.")
                clear_screen()
                break
            else:
                print("Invalid input.")
                input("Press enter to continue.")
                clear_screen()

    elif event_choice == 8:

        random_text = random.randint(35, 39)
        print(random_events_text[random_text])
        if 50 < distance_traveled >= 25:
            distance_traveled = 50
        elif 100 < distance_traveled >= 75:
            distance_traveled = 100
        elif 150 < distance_traveled >= 125:
            distance_traveled = 150
        elif 200 < distance_traveled >= 175:
            distance_traveled = 200
        elif 250 < distance_traveled >= 225:
            distance_traveled = 250
        elif 300 < distance_traveled >= 275:
            distance_traveled = 300
        else:
            distance_advance = random.randint(5, 25)
            distance_traveled += distance_advance
        print("You find that you\'ve advanced significantly in the cave!")
        input("Press enter to continue.")
        clear_screen()

    elif event_choice == 9:
        random_text = random.randint(40, 44)
        print(random_events_text[random_text])
        while True:
            choice_answer = input("Do you read it? (y/n):").lower()
            clear_screen()
            if choice_answer == "y":
                if random.randint(player_luck, 3) == 3:
                    print("The contents of the journal rejuvenate you and teach you new ways to fight!")
                    player_damage += 1
                    player_health += int(player_max_health / 2)
                    if player_health > player_max_health:
                        player_health = player_max_health
                    print("You gained +1 base damage and healed " + str(int(player_max_health / 2)) + " HP!")
                    if player_luck == 2:
                        print("Your luck saved you!")
                        player_luck = 1
                    else:
                        print("You\'re feeling lucky!")
                        player_luck = 2
                    input("Press enter to continue.")
                    clear_screen()
                    break
                else:
                    print("The contents of the journal depress you and you lose the will to fight...")
                    if player_damage > 1:
                        player_damage -= 1
                    player_health -= int(player_health / 2)
                    print("You lost 1 base damage and lost " + str(int(player_health / 2)) + " HP!")
                    if player_luck == 0:
                        print("Your bad luck has ended!")
                        player_luck = 1
                input("Press enter to continue.")
                if player_health <= 0:
                    game_over()
                clear_screen()
                break
            elif choice_answer == "n":
                print("Perhaps it\'s better left alone...")
                input("Press enter to continue.")
                clear_screen()
                break
            else:
                print("Invalid input.")
                input("Press enter to continue.")
                clear_screen()

    elif event_choice == 10:
        random_text = random.randint(45, 49)
        print(random_events_text[random_text])
        input("Press enter to continue...")
        clear_screen()
        if random.randint(player_luck, 3) == 3:
            print("It seems to have taken a liking to you!")
            loot = random_loot()
            print("They lead you to a small crack in the wall,\n"
                  "You find: " + loot + "!")
            player_action(loot)
            if player_luck == 2:
                print("Your luck saved you!")
                player_luck = 1
            else:
                print("You\'re feeling lucky!")
                player_luck = 2
        else:
            print("It charges at you!")
            distance_lost = random.randint(1, int(distance_traveled / 4))
            print("When you finally stop running to check if it is still following you,\n"
                  "You realize you\'ve run " + str(distance_lost) + " steps backwards!")
            distance_traveled -= distance_lost
            item_lost_list = []
            for lost_items in player_inventory:
                if lost_items != "Gold":
                    item_lost_list.append(lost_items)
            if not item_lost_list:
                print("After catching your breath, you realize you also dropped all your Gold!")
                player_inventory["Gold"] = 0
            else:
                item_lost = random.choice(item_lost_list)
                print("After catching your breath, you realize you also dropped your " + item_lost)
                if player_inventory.get(item_lost) > 1:
                    player_inventory[item_lost] -= 1
                else:
                    player_inventory.pop(item_lost)
            print("Talk about bad luck!")
            if player_luck == 0:
                print("Your bad luck has ended!")
                player_luck = 1
        input("Press enter to continue.")
        clear_screen()


def spawn_shop_room():
    print("You found a shop room!")
    options = {}
    while True:
        current_item = random_loot()
        if current_item != "Gold" and current_item != "Nothing! What a shame...":
            if current_item not in options.keys():
                if current_item in loot_list:
                    options.update({current_item: random.randint(5, 10)})
                elif current_item in greater_loot_list:
                    options.update({current_item: random.randint(20, 40)})
                else:
                    options.update({current_item: random.randint(60, 80)})
        if len(options) == 5:
            break

    sell_list = {}
    for list_item in loot_list:
        sell_list[list_item] = random.randint(3, 8)
    for list_item in greater_loot_list:
        sell_list[list_item] = random.randint(10, 30)
    for list_item in godlike_loot_list:
        sell_list[list_item] = random.randint(30, 50)
    for list_item in basic_monster_loot_list:
        sell_list[list_item] = random.randint(5, 13)
    for list_item in intermediate_monster_loot_list:
        sell_list[list_item] = random.randint(10, 25)
    for list_item in expert_monster_loot_list:
        sell_list[list_item] = random.randint(25, 40)
    for list_item in boss_monster_loot_list:
        sell_list[list_item] = random.randint(50, 80)

    while True:
        choice = input("Buy, sell or leave?: ").lower()
        clear_screen()
        if choice == "buy":
            if player_inventory.get("Gold") == 0:
                print("You don't have any gold!")
            else:
                while True:
                    print("Current Gold: " + str(player_inventory.get("Gold")))
                    print("What would you like to buy?: ")
                    x = 1
                    for option in options:
                        if option != "Nothing! What a shame..." and option != 'Gold':
                            print(x, ": " + option + ":", options.get(option))
                            x += 1
                    purchase_option = input("Pick by name, or type done: ")
                    clear_screen()
                    if purchase_option == "done":
                        break
                    elif (options.get(purchase_option) is not None
                          and player_inventory.get("Gold") >= options.get(purchase_option)):
                        player_action(purchase_option)
                        player_inventory["Gold"] -= options.get(purchase_option)
                        options.pop(purchase_option)
                    elif options.get(purchase_option) is None:
                        print("Invalid option.")
                    else:
                        print("Not enough Gold!")
                        input("Press enter to continue.")
                        clear_screen()
        elif choice == "sell":
            if len(player_inventory) == 1:
                print("Your inventory is empty!")
                input("Press enter to continue.")
                clear_screen()
            else:
                while True:
                    print("What would you like to sell?: ")
                    for sell_options in player_inventory:
                        if sell_options != "Gold":
                            print(sell_options + ":", player_inventory.get(sell_options),
                                  "| Value: ", sell_list.get(sell_options))
                    sell_option = input("Sell by name, or type done: ")
                    clear_screen()
                    if sell_option == "done":
                        break
                    elif player_inventory.get(sell_option) is not None:
                        player_inventory["Gold"] += sell_list.get(sell_option)
                        player_inventory[sell_option] -= 1
                        print("Sold!")
                        if player_inventory.get(sell_option) == 0:
                            player_inventory.pop(sell_option)
                        input("Press enter to continue.")
                        clear_screen()
                    else:
                        print("Invalid option.")
        elif choice == "leave":
            print("Thanks for stopping by!")
            input("Press enter to continue.")
            clear_screen()
            break
        else:
            print("Invalid option.")
            input("Press enter to continue.")
            clear_screen()


# Checks spawn rate to see if dungeon travel spawns in a unique room
def room_spawn(spawner_rate):
    global continue_pathway_text
    spawner_chance = random.randint(1, 11)
    if random.randint(1, spawner_rate) == 1:
        if (spawner_chance == 1 or spawner_chance == 2 or spawner_chance == 3
                or spawner_chance == 4 or spawner_chance == 5):
            spawn_enemy_room()
        elif spawner_chance == 6 or spawner_chance == 7:
            spawn_loot_room()
        elif spawner_chance == 8:
            spawn_shop_room()
        else:
            spawn_random_event()
    else:
        print(random.choice(continue_pathway_text))
        print(random.choice(continue_on_text))


def main_menu():
    global player_name, player_health, player_max_health, player_armour, player_damage, player_exp
    global player_level, player_luck, player_carrying, player_hit_chance
    global distance_traveled, journey_length, player_inventory
    while True:
        print("***************************************************")
        print("                 D U N G E O N")
        print("                   C R A W L")
        print("***************************************************")
        print("                                           New Game")
        print("                                          Load Save")
        print("                                               Help")
        print("                                               Quit\n")
        print("               Enter your choice:")
        main_choice = input("                     ").lower()
        clear_screen()
        if main_choice == "new game":
            while True:
                print("***************************************************")
                print("                 D U N G E O N")
                print("                   C R A W L")
                print("***************************************************")
                print("Beginner's Bliss: The Entryway Expedition     (Easy)")
                print("Challenger's Depths: The Midway Gauntlet    (Medium)")
                print("Nightmare's Descent: The Abyssal Trial        (Hard)\n")
                difficulty = input("          Select Difficulty: ").lower()
                if difficulty == "easy":
                    journey_length = 100
                    clear_screen()
                    break
                elif difficulty == "medium":
                    journey_length = 200
                    clear_screen()
                    break
                elif difficulty == "hard":
                    journey_length = 300
                    clear_screen()
                    break
                else:
                    clear_screen()
                    print("        Invalid option (Easy, Medium or Hard)")
            print("***************************************************")
            print("                 D U N G E O N")
            print("                   C R A W L")
            print("***************************************************\n\n")
            player_name = str(input("             Enter your name: "))
            clear_screen()
            print("***************************************************")
            print("                 D U N G E O N")
            print("                   C R A W L")
            print("***************************************************\n\n")
            input("           Press enter to begin, " + player_name + "!")
            break
        elif main_choice == "load save":
            with open('dungeon_crawler_save_file.txt', 'r') as open_save_file:
                save_line = open_save_file.readline()
                save_data = []
                while save_line:
                    save_line = save_line.replace('\n', '')
                    save_data.append(save_line)
                    save_line = open_save_file.readline()
            print("***************************************************")
            print("                 D U N G E O N")
            print("                   C R A W L")
            print("***************************************************\n\n")
            load_save_choice = input("         Load in [" + save_data[0] + "\'s] save? (y/n): ").lower()
            if load_save_choice == "y":
                player_name = str(save_data[0])
                player_health = int(save_data[1])
                player_max_health = int(save_data[2])
                player_armour = int(save_data[3])
                player_damage = int(save_data[4])
                player_exp = int(save_data[5])
                player_level = int(save_data[6])
                player_luck = int(save_data[7])
                player_carrying = (ast.literal_eval((save_data[8])))
                player_hit_chance = int(save_data[9])
                distance_traveled = int(save_data[10])
                journey_length = int(save_data[11])
                player_inventory = (ast.literal_eval((save_data[12])))
                print("        " + player_name + "\'s save loaded successfully!")
                input("          Press enter to begin, " + player_name + "!")
                break
            clear_screen()
        elif main_choice == "help":
            print("***************************************************************")
            print("                           H E L P")
            print("***************************************************************")
            print("Explore a diverse cave system using your keyboard to guide you!")
            print("      Follow the prompts to continue through the story")
            print("             Use the enter key to advance")
            print(" You must match spelling, and in some cases CaPiTaLs as well")
            print("       Type in help when available get in-game help!\n")
            input("                         Good luck!")
            clear_screen()
        elif main_choice == "quit":
            print("Bye!")
            exit()
        else:
            print("                Invalid Option")


def main_dungeon_script():
    clear_screen()
    clear_screen()
    main_menu()
    clear_screen()
    while distance_traveled < journey_length + 1:
        dungeon_travel(get_direction())
        check_level_up()
    print("You win! Make something cooler here...")
    input("Press enter to continue.")


def game_over():
    clear_screen()
    print("       You died!")
    print("******** Stats ********")
    print(player_name)
    print("Distance traveled: " + str(distance_traveled))
    print("Gold: " + str(player_inventory.get("Gold")))
    print("Level: " + str(player_level))
    print("\nThank you for playing!")
    input("Press enter to end your run...")
    exit()


def main():
    clear_screen()
    print("Loading...")
    clear_screen()
    main_dungeon_script()
    clear_screen()
    print("This should be a new screen!")


if __name__ == '__main__':
    main()
