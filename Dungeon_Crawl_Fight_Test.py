# Welcome to my VERY ambitious coding project PART 2!!!
# Time for the hard part lol
# Samuel Gould 2024-08-21
# *****************************************************
# NOTES / TODO:
#
# special moves
#
# BALANCING EVERYTHING / PLAY TESTING
# *****************************************************

import time
import os
import random
import math

print("Loading...")

player_name = "Fighter"
player_health = 5
player_max_health = 10
player_armour = 0
player_damage = 1
player_exp = 1
player_level = 1
player_carrying = {"Weapon": "Sword", "Armour": "Armour", "Shield": None}
player_hit_chance = 80
distance_traveled = 0
journey_length = 100
player_inventory = {"Gold": random.randint(1, 10), "Tempered Shield": 1, "Bomb":1,"Health Potion":2}
player_stats = {}
victory_loot = []  # item(s) [up to 3], gold, exp
exp_gain = 0
player_stuck = False
enemy_charge = [False, False, False, False, False]  #    Returns true is enemy_charge[position] is charging special
defence_raised = 0  # defend action will raise this for one turn
basic_monster_loot = ["Club", "Bone Bow", "Scaled Sword", "Exo-skeleton"]
intermediate_monster_loot = ["Knife", "Studded Armour", "Hardened Exo-skeleton", "Gemstone", "Hounds Fang"]
expert_monster_loot = ["Tainted Sword", "Broken Magma Fang", "Obsidian Plate", "Corrupted Bow"]
boss_monster_loot = ["Blood-Soaked Axe", "Dragon-Scale Armour", "Beast Bow", "Starlight Bow", "Holy Blade"]
monster_dict = {
    #   Beginner
    "Goblin": {"attack": [1, 3], "defence": 0, "hp": 4, "max hp": 4, "hit_chance": 55,
               "weapons": ["Club", "Broken Sword"], "special": None, "loot": "Club"},
    "Bat": {"attack": [1, 3], "defence": 0, "hp": 3, "max hp": 3, "hit_chance": 45,
            'weapons': ["Fangs", "Swarm"], "special": "Lesser Drain", "loot": None},
    "Skeleton": {"attack": [2, 3], "defence": 0, "hp": 4, "max hp": 4, "hit_chance": 65, "weapons": ["Bone Club", "Arrow"],
                 "special": None, "loot": "Bone Bow"},
    "Golem": {"attack": [2, 4], "defence": 1, "hp": 3, "max hp": 3, "hit_chance": 50,
              "weapons": ["Rock Fist"], "special": None, "loot": "Slatemail"},
    "Lizard-Man": {"attack": [2, 5], "defence": 0, "hp": 5, "max hp": 5, "hit_chance": 40,
                   "weapons": ["Scaled Sword", "Claws"], "special": None, "loot": "Scaled Sword"},
    "Giant Spider": {"attack": [2, 5], "defence": 0, "hp": 4, "max hp": 4, "hit_chance": 55,
                     "weapons": ["Fangs", "Web Shot"], "special": "Web Net", "loot": "Exo-skeleton"},
    #   Intermediate
    "Cultist": {"attack": [5, 9], "defence": 1, "hp": 14, "max hp": 14, "hit_chance": 65,
                "weapons": ["Knife", "Black Magic"], "special": "Lesser Heal", "loot": "Knife"},
    "Hobgoblin": {"attack": [5, 8], "defence": 2, "hp": 17, "max hp": 17, "hit_chance": 65,
                  "weapons": ["Large Club", "Battle Axe"], "special": None, "loot": "Studded Armour"},
    "Massive Beetle": {"attack": [4, 7], "defence": 4, "hp": 10, "max hp": 10, "hit_chance": 60,
                       "weapons": ["Fangs", "Pincers"], "special": None, "loot": "Hardened Exo-skeleton"},
    "Cave Troll": {"attack": [4, 9], "defence": 2, "hp": 16, "max hp": 16, "hit_chance": 65,
                   "weapons": ["Giant Club"], "special": None, "loot": None},
    "Crystal Drake": {"attack": [6, 8], "defence": 5, "hp": 17, "max hp": 17, "hit_chance": 60,
                      "weapons": ["Tail"], "special": None, "loot": "Gemstone"},
    "Gloom Hound": {"attack": [6, 9], "defence": 2, "hp": 12, "max hp": 12, "hit_chance": 70,
                     "weapons": ["Bite", "Claws"], "special": "Hound Backup", "loot": "Hounds Fang"},
    #   Expert
    "Tunnel Wraith": {"attack": [10,14], "defence": 0, "hp": 30, "max hp": 30, "hit_chance": 70,
                      "weapons": ["Claws", "Soul Sap"], "special": None, "loot": None},
    "Tainted Knight": {"attack":[10,16], "defence": 8, "hp": 24, "max hp": 24, "hit_chance": 60,
                       "weapons": ["Tainted Sword", "Tainted Axe"], "special": None, "loot": "Tainted Sword"},
    "Infernal Drake": {"attack": [12,15], "defence": 6, "hp": 26, "max hp": 26, "hit_chance": 75,
                       "weapons": ["Burning Claws", "Magma Fangs"], "special": None, "loot": "Broken Magma Fang"},
    "Obsidian Crawler": {"attack": [12,17], "defence": 10, "hp": 18, "max hp": 18, "hit_chance": 80,
                         "weapons": ["Hardened Limbs"], "special": None, "loot": "Obsidian Plate"},
    "Corrupted Archer": {"attack": [11,15], "defence": 2, "hp": 27, "max hp": 27, "hit_chance": 60,
                         "weapons": ["Corrupted Bow", "Throwing Knives"], "special": None, "loot": "Corrupted Bow"},
    #   Bosses
    "Aila the Severed": {"attack": [5,7], "defence": 2, "hp": 30, "max hp": 30, "hit_chance": 70,
                         "weapons": ["Blood-soaked Axe", "Infested Claws", "Poison Bite"],
                         "special": "Gnawing Screech", "loot": "Blood-Soaked Axe"},
    "Chained Dragon": {"attack": [17,23], "defence": 5, "hp": 70, "max hp": 70, "hit_chance": 80,
                         "weapons": ["Roar", "Broken Claws", "Deadly Fangs"],
                         "special": "Infernal Breath", "loot": "Dragon-Scale Armour"},
    "Oxyn the Beast": {"attack": [30,46], "defence": 4, "hp": 100, "max hp": 100, "hit_chance": 80,
                         "weapons": ["Charge", "Beast Claws", "Serrated Arrow"],
                         "special": "Grapple", "loot": "Beast Bow"},
    "Void Spawn": {"attack": [50, 62], "defence": 7, "hp": 140, "max hp": 140, "hit_chance": 75,
                         "weapons": ["Black Hole", "Fissure", "Rain of Stars"],
                         "special": "Infinity", "loot": "Starlight Bow"},
    "Fallen Angel": {"attack": [67,72], "defence": 4, "hp": 170, "max hp": 170, "hit_chance": 75,
                         "weapons": ["Holy Blade", "Wind Blast", "Corrupted Fangs"],
                         "special": "Requiem", "loot": "Holy Blade"},
    "Nyxara the Abyss": {"attack": [80, 100], "defence": 8, "hp": 250, "max hp": 250, "hit_chance": 85,
                         "weapons": ["Erase", "Finality", "Implode"],
                         "special": "Singularity", "loot": None},
}


#   Clears screen when function called
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


#   Displays opening animation like Pokémon fight
def fight_sequence_opening():
    for x in range(35):
        if x < 25:
            print("****" * x)
        else:
            print("****" * 25)
        if x >= 1:
            a = x - 1
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        if x >= 2:
            a = x - 2
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        if x >= 3:
            a = x - 3
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        if x >= 4:
            a = x - 4
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        if x >= 5:
            a = x - 5
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        if x >= 6:
            a = x - 6
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        if x >= 7:
            a = x - 7
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        if x >= 8:
            a = x - 8
            if a < 25:
                print("****" * a)
            else:
                print("****" * 25)
        time.sleep(0.05)
        clear_screen()


#   gets all info needed from dungeon_crawl main and imports it here to global variables for ease of use
def player_fight_setup(plr_name, plr_health, plr_max_health, plr_armour,
                       plr_damage, plr_exp, plr_level, plr_carrying,
                       plr_hit_chance, dist_traveled, plr_inventory):
    global player_name, player_health, player_max_health, player_armour, \
        player_damage, player_exp, player_level, player_carrying, \
        player_hit_chance, distance_traveled, player_inventory
    player_name = plr_name
    player_health = plr_health
    player_max_health = plr_max_health
    player_armour = plr_armour
    player_damage = plr_damage
    player_exp = plr_exp
    player_level = plr_level
    player_carrying = plr_carrying
    player_hit_chance = plr_hit_chance
    distance_traveled = dist_traveled
    player_inventory = plr_inventory


def monster_setup():
    global player_level, distance_traveled, exp_gain
    #   checks how far you are first then should return boss type. then goes by level
    enemy_list = []
    exp_gain = 0
    if distance_traveled == 50:
        exp_gain += 50
        enemy_list.append(list(monster_dict.keys())[17])
        return enemy_list
    elif distance_traveled == 100:
        exp_gain += 100
        enemy_list.append(list(monster_dict.keys())[18])
        return enemy_list
    elif distance_traveled == 150:
        exp_gain += 150
        enemy_list.append(list(monster_dict.keys())[19])
        return enemy_list
    elif distance_traveled == 200:
        exp_gain += 200
        enemy_list.append(list(monster_dict.keys())[20])
        return enemy_list
    elif distance_traveled == 250:
        exp_gain += 300
        enemy_list.append(list(monster_dict.keys())[21])
        return enemy_list
    elif distance_traveled == 300:
        exp_gain += 400
        enemy_list.append(list(monster_dict.keys())[22])
        return enemy_list
    elif player_level == 1:
        #   1-2 Easy
        enemy_number = random.randint(1, 2)
        exp_gain += random.randint(3,8)
        for x in range(enemy_number):
            enemy_list.append(list(monster_dict.keys())[random.randint(0, 5)])
        return enemy_list
    elif player_level == 2:
        #   2-4 Easy
        enemy_number = random.randint(2, 4)
        exp_gain += enemy_number * random.randint(3,5)
        for x in range(enemy_number):
            enemy_list.append(list(monster_dict.keys())[random.randint(0, 5)])
        return enemy_list

    elif player_level == 3:
        #   1 Intermediate and 1-2 easy or 5 easy
        enemy_layout = random.randint(1, 3)
        if enemy_layout == 1:
            enemy_number = 5
            exp_gain += enemy_number * random.randint(3,5)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(0, 5)])
            return enemy_list
        else:
            enemy_number = 1
            exp_gain += enemy_number * random.randint(10,25)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(6, 11)])
            enemy_number = random.randint(1, 2)
            exp_gain += enemy_number * random.randint(3, 5)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(0, 5)])
            return enemy_list

    elif player_level == 4:
        #   2-3 Intermediate and 1 easy or 1 Intermediate and 3-4 easy
        enemy_layout = random.randint(1, 3)
        if enemy_layout == 1:
            enemy_number = random.randint(2, 3)
            exp_gain += enemy_number * random.randint(10, 25)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(6, 11)])
            enemy_number = 1
            exp_gain += enemy_number * random.randint(3, 5)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(0, 5)])
            return enemy_list
        else:
            enemy_number = 1
            exp_gain += enemy_number * random.randint(10, 25)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(6, 11)])
            enemy_number = random.randint(3, 4)
            exp_gain += enemy_number * random.randint(3, 5)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(0, 5)])
            return enemy_list

    elif player_level == 5:
        #   4-5 Intermediate or 1 hard
        enemy_layout = random.randint(1, 3)
        if enemy_layout == 1:
            enemy_number = enemy_number = random.randint(4, 5)
            exp_gain += enemy_number * random.randint(10, 20)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(6, 11)])
            return enemy_list
        else:
            enemy_number = 1
            exp_gain += enemy_number * random.randint(20, 35)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(12, 16)])
            return enemy_list

    elif player_level == 6:
        #   2-3 Hard and 1 Intermediate or 1 Hard and 3-4 Intermediate
        enemy_layout = random.randint(1, 3)
        if enemy_layout == 1:
            enemy_number = random.randint(2, 3)
            exp_gain += enemy_number * random.randint(20, 35)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(12, 16)])
            enemy_number = 1
            exp_gain += enemy_number * random.randint(10, 20)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(6, 11)])
            return enemy_list
        else:
            enemy_number = 1
            exp_gain += enemy_number * random.randint(20, 35)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(12, 16)])
            enemy_number = random.randint(3, 4)
            exp_gain += enemy_number * random.randint(10, 20)
            for x in range(enemy_number):
                enemy_list.append(list(monster_dict.keys())[random.randint(6, 11)])
            return enemy_list

    elif player_level == 7:
        #   5 Hard
        enemy_number = 5
        exp_gain += enemy_number * random.randint(20, 30)
        for x in range(enemy_number):
            enemy_list.append(list(monster_dict.keys())[random.randint(12, 16)])
        return enemy_list


#   Checks level, distance, and max attack and returns list of monsters you fight
def dungeon_fight_enemy_type(dungeon_monster_setup):
    # 0 - 5 = beginner
    # 6 -11 = intermediate
    # 12 - 16 = expert
    enemy_type = [None, None, None, None, None]
    for monster in range(len(dungeon_monster_setup)):
        enemy_type[monster] = dungeon_monster_setup[monster]
    return enemy_type  #   DEBUG *************************************************


def dungeon_fight_enemy_stats(current_enemy_list):
    enemy_stats = [{"attack": [], "defence": 0, "hp": 0, "max hp": 0, "hit_chance": 0,
                    "weapons": [], "special": None, "loot": None},
                   {"attack": [], "defence": 0, "hp": 0, "max hp": 0, "hit_chance": 0,
                    "weapons": [], "special": None, "loot": None},
                   {"attack": [], "defence": 0, "hp": 0, "max hp": 0, "hit_chance": 0,
                    "weapons": [], "special": None, "loot": None},
                   {"attack": [], "defence": 0, "hp": 0, "max hp": 0, "hit_chance": 0,
                    "weapons": [], "special": None, "loot": None},
                   {"attack": [], "defence": 0, "hp": 0, "max hp": 0, "hit_chance": 0,
                    "weapons": [], "special": None, "loot": None}]
    x = 0
    for name in current_enemy_list:
        if current_enemy_list[x] is not None:
            for stat in monster_dict[name]:
                enemy_stats[x].update({stat: monster_dict[name][stat]})
        x += 1
    return enemy_stats


# This will display any messages the player needs during combat
def display_message(msg=''):
    return msg


#   will display players options based off of current game state
def display_options(enemy_list, enemy_stats, loot_list, state=''):
    global player_armour, defence_raised, player_name, player_max_health
    global player_health, player_inventory, player_carrying, player_hit_chance
    global player_exp
    if state == '':

        print("                         [1:  Attack  ]" + " " * 15 + "[2: Defend]")
        print("                         [3: Inventory]" + " " * 15 + "[4:  Run  ]")
        return ''

    elif state == 'attack':
        back_distance = 0
        print("        ", end='')
        for length in range(len(enemy_list)):
            if enemy_list[length] is not None:
                back_distance += 1
                if length == 3:
                    print("\n        ", end='')
                print("[" + str(length + 1) + ": " + enemy_list[length] + " " * (
                        16 - len(enemy_list[length])) + "]        ", end='')
        if back_distance < 4:
            print("\n" + " " * 66 + "[6: Back" + " " * 12 + "]")
        elif back_distance == 4:
            print(" " * 29 + "[6: Back" + " " * 12 + "]")
        elif back_distance == 5:
            print("[6: Back" + " " * 12 + "]")
        return 'attack'

    elif (state == 'enemyattack_0' or state == 'enemyattack_1'
          or state == 'enemyattack_2' or state == 'enemyattack_3'
          or state == 'enemyattack_4'):
        attacked_enemy = int(state.split('_')[1])

        if enemy_list[attacked_enemy] == "Dead":
            return 'enemy_dead'

        # IMPLEMENT DAMAGE AND WHATNOT
        hit_check = random.randint(1, 100)
        if hit_check < player_hit_chance:  #   Success!

            if random.randint(1, 10) == 1:
                if player_damage * 2 > enemy_stats[attacked_enemy]['defence']:
                    enemy_stats[attacked_enemy]['hp'] = (enemy_stats[attacked_enemy]['hp']
                                                         - (player_damage * 2 - enemy_stats[attacked_enemy]['defence']))
                    if enemy_stats[attacked_enemy]['hp'] <= 0:
                        enemy_stats[attacked_enemy]['hp'] = 0
                        enemy_stats[attacked_enemy]['max hp'] = 0
                        enemy_list[attacked_enemy] = "Dead"
                    return 'crit'
            else:
                if player_damage > enemy_stats[attacked_enemy]['defence']:
                    enemy_stats[attacked_enemy]['hp'] = (enemy_stats[attacked_enemy]['hp']
                                                         - (player_damage - enemy_stats[attacked_enemy]['defence']))
                if enemy_stats[attacked_enemy]['hp'] <= 0:
                    enemy_stats[attacked_enemy]['hp'] = 0
                    enemy_stats[attacked_enemy]['max hp'] = 0
                    enemy_list[attacked_enemy] = "Dead"
                return 'hit'
        else:
            return 'miss'

    elif state == "hit":
        print("                                         [ Your attack hit! ]\n")
        return 'enemy'

    elif state == "bomb":
        print("                                         [ Your Bomb hit! ]\n")
        return 'enemy'

    elif state == "greater bomb":
        print("                                      [ Your Greater Bomb hit! ]\n")
        return 'enemy'

    elif state == "crit":
        print("                                        [ Your attack crit! ]\n")
        return 'enemy'

    elif state == "miss":
        print("                                       [ Your attack missed! ]\n")
        return 'enemy'

    elif state == 'defend':
        print("                                 [ " + player_name + "\'s defences are boosted! ]\n")
        if player_armour > 0:
            defence_raised += math.ceil(player_armour / 2)
        else:
            defence_raised = 1
        player_armour += defence_raised
        player_name = player_name + " *Defending*"
        return 'defend'

    elif state == 'inventory':
        while True:
            clear_screen()
            print("In bag:")
            for items in player_inventory:
                print(items + ":", player_inventory[items])
            print("\nCarrying:")
            for items in player_carrying:
                if (player_carrying.get(items) is not None and items != "Gold"
                        and items != "Luck Potion"
                        and items != "Gemstone"):
                    print(player_carrying.get(items))
            equip_action = input("\nPress enter to go back or type 'Item Name' to equip / use: ")
            if equip_action == "Health Potion":
                if player_inventory.get("Health Potion") is None:
                    clear_screen()
                    print("You have no Health Potions!")
                    input("\nPress enter to continue.")
                    clear_screen()
                else:
                    clear_screen()
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
                    break
            elif equip_action == "Grand Health Potion":
                if player_inventory.get("Grand Health Potion") is None:
                    print("You have no Grand Health Potions!")
                    input("\nPress enter to continue.")
                    clear_screen()
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
                    break

            elif equip_action == "Bomb":
                if player_inventory.get("Bomb") is None:
                    print("You have no Bombs!")
                    input("\nPress enter to continue.")
                    clear_screen()
                else:
                    if (player_inventory.get("Bomb") > 1
                            and player_inventory.get("Bomb") is not None):
                        player_inventory["Bomb"] -= 1
                    elif (player_inventory.get("Bomb") == 1
                          and player_inventory.get("Bomb") is not None):
                        player_inventory.pop("Bomb")

                    for enemies in range(len(enemy_list)):
                        if enemy_list[enemies-1] is not None:
                            enemy_stats[enemies-1]['hp'] -= random.randint(3,8)
                            if enemy_stats[enemies-1]['hp'] <= 0:
                                enemy_stats[enemies-1]['hp'] = 0
                                enemy_stats[enemies-1]['max hp'] = 0
                                enemy_list[enemies-1] = "Dead"
                    clear_screen()
                    return 'bomb'

            elif equip_action == "Greater Bomb":
                if player_inventory.get("Greater Bomb") is None:
                    print("You have no Greater Bombs!")
                    input("\nPress enter to continue.")
                    clear_screen()
                else:
                    if (player_inventory.get("Greater Bomb") > 1
                            and player_inventory.get("Greater Bomb") is not None):
                        player_inventory["Greater Bomb"] -= 1
                    elif (player_inventory.get("Greater Bomb") == 1
                          and player_inventory.get("Greater Bomb") is not None):
                        player_inventory.pop("Greater Bomb")

                    for enemies in range(len(enemy_list)):
                        if enemy_list[enemies-1] is not None:
                            enemy_stats[enemies - 1]['hp'] -= random.randint(10, 15)
                            if enemy_stats[enemies - 1]['hp'] <= 0:
                                enemy_stats[enemies - 1]['hp'] = 0
                                enemy_stats[enemies - 1]['max hp'] = 0
                                enemy_list[enemies - 1] = "Dead"
                    clear_screen()
                    return 'greater bomb'

            elif equip_action in player_inventory:
                if item_equip(equip_action):
                    print("You equipped: " + equip_action + ".")
                    input("Press Enter to continue.")
                    clear_screen()
                    break
                else:
                    print("You can only equip a Weapon, Shield, or Armour.")
            elif equip_action == "":
                clear_screen()
                return 'back'
            else:
                clear_screen()
                print("Invalid action.")

        return 'inventory'

    elif state == 'run':
        print("                                       [ Attempting to run. ]")
        return 'run'

    elif state == 'run_attempt':
        if player_level == 1:
            run_attempt = 80
        elif player_level == 2:
            run_attempt = 70
        elif player_level == 3:
            run_attempt = 65
        elif player_level == 4:
            run_attempt = 60
        elif player_level == 5:
            run_attempt = 55
        elif player_level == 6:
            run_attempt = 50
        else:
            run_attempt = 40

        run_check = random.randint(1, 100)
        if run_check < run_attempt:
            global distance_traveled
            #   success!
            print("                                          [ You got away! ]")
            input("Press enter to continue...")
            clear_screen()
            if player_inventory["Gold"] > 3:
                gold_lost = random.randint(1, int(player_inventory["Gold"] / 3))
                player_inventory["Gold"] -= gold_lost
                if distance_traveled > 15: #    *********** FIX SO YOU CANT GO BACK THROUGH BOSS BATTLES ******************************************
                    distance_traveled -= random.randint(10,15)
                print("\n                                         [ You lost " + str(gold_lost) + " gold! ]\n")
            else:
                print("\n                                        [ You got away safely! ]\n")
            return 'end'
        else:
            print("                                        [ Failed to escape! ]\n")
            return 'run_attempt'

    elif state == 'enemy':
        print("                                          [ Enemy's turn! ]\n")
        return 'enemy_attack_sequence_1'

    elif state == 'enemy_attack_sequence_1':
        attacking_enemy = int(state.split('_')[3]) - 1
        #   this shouldn't happen but still
        if enemy_list[attacking_enemy] is None:
            return 'player_win'
        #   if enemy one is there and isn't dead, attack
        elif enemy_list[attacking_enemy] != 'Dead':
            # enemy attack sequence / crit check
            hit_check = random.randint(1, 100)
            if hit_check < enemy_stats[attacking_enemy]['hit_chance']:  # Success!

                if random.randint(1, 10) == 1:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 > player_armour:
                        player_health = (player_health - (random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 - player_armour))
                        if player_health <= 0:
                            player_health = 0
                    return 'enemy_crit_1'
                else:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) > player_armour:
                        player_health = (player_health - (
                                random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) - player_armour))
                        if player_health <= 0:
                            player_health = 0
                return 'enemy_hit_1'
            else:
                return 'enemy_miss_1'
        else:
            #   if next enemy exists, and isn't dead, continue onto their turn
            if enemy_list[attacking_enemy + 1] is not None or enemy_list[attacking_enemy] != 'dead':
                return 'enemy_dead_1'
            #   if monster one is dead, and there is no second monster, you win
            if enemy_list[attacking_enemy + 1] is None:
                return 'enemy_turn_purge'

    elif state == 'enemy_attack_sequence_2':
        attacking_enemy = int(state.split('_')[3]) - 1
        if enemy_list[attacking_enemy] != 'Dead':
            # enemy attack sequence / crit check
            hit_check = random.randint(1, 100)
            if hit_check < enemy_stats[attacking_enemy]['hit_chance']:  # Success!

                if random.randint(1, 10) == 1:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 > player_armour:
                        player_health = (player_health - (random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 - player_armour))
                        if player_health <= 0:
                            player_health = 0
                    return 'enemy_crit_2'
                else:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) > player_armour:
                        player_health = (player_health - (
                                random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) - player_armour))
                        if player_health <= 0:
                            player_health = 0
                return 'enemy_hit_2'
            else:
                return 'enemy_miss_2'
        else:
            #   if next enemy exists, and isn't dead, continue onto their turn
            if enemy_list[attacking_enemy + 1] is not None or enemy_list[attacking_enemy] != 'dead':
                return 'enemy_dead_2'
            #   if monster one is dead, and there is no second monster, you win
            if enemy_list[attacking_enemy + 1] is None:
                return 'enemy_turn_purge'

    elif state == 'enemy_attack_sequence_3':
        attacking_enemy = int(state.split('_')[3]) - 1
        if enemy_list[attacking_enemy] != 'Dead':
            # enemy attack sequence / crit check
            hit_check = random.randint(1, 100)
            if hit_check < enemy_stats[attacking_enemy]['hit_chance']:  # Success!

                if random.randint(1, 10) == 1:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 > player_armour:
                        player_health = (player_health - (random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 - player_armour))
                        if player_health <= 0:
                            player_health = 0
                    return 'enemy_crit_3'
                else:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) > player_armour:
                        player_health = (player_health - (
                                random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) - player_armour))
                        if player_health <= 0:
                            player_health = 0
                return 'enemy_hit_3'
            else:
                return 'enemy_miss_3'
        else:
            #   if next enemy exists, and isn't dead, continue onto their turn
            if enemy_list[attacking_enemy + 1] is not None or enemy_list[attacking_enemy] != 'dead':
                return 'enemy_dead_3'
            #   if monster one is dead, and there is no second monster, you win
            if enemy_list[attacking_enemy + 1] is None:
                return 'enemy_turn_purge'

    elif state == 'enemy_attack_sequence_4':
        attacking_enemy = int(state.split('_')[3]) - 1
        if enemy_list[attacking_enemy] != 'Dead':
            # enemy attack sequence / crit check
            hit_check = random.randint(1, 100)
            if hit_check < enemy_stats[attacking_enemy]['hit_chance']:  # Success!

                if random.randint(1, 10) == 1:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 > player_armour:
                        player_health = (player_health - (random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 - player_armour))
                        if player_health <= 0:
                            player_health = 0
                    return 'enemy_crit_4'
                else:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) > player_armour:
                        player_health = (player_health - (
                                random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) - player_armour))
                        if player_health <= 0:
                            player_health = 0
                return 'enemy_hit_4'
            else:
                return 'enemy_miss_4'
        else:
            #   if next enemy exists, and isn't dead, continue onto their turn
            if enemy_list[attacking_enemy + 1] is not None or enemy_list[attacking_enemy] != 'dead':
                return 'enemy_dead_4'
            #   if monster one is dead, and there is no second monster, you win
            if enemy_list[attacking_enemy + 1] is None:
                return 'enemy_turn_purge'

    elif state == 'enemy_attack_sequence_5':
        attacking_enemy = int(state.split('_')[3]) - 1
        if enemy_list[attacking_enemy] != 'Dead':
            # enemy attack sequence / crit check
            hit_check = random.randint(1, 100)
            if hit_check < enemy_stats[attacking_enemy]['hit_chance']:  # Success!

                if random.randint(1, 10) == 1:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 > player_armour:
                        player_health = (player_health - (random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) * 2 - player_armour))
                        if player_health <= 0:
                            player_health = 0
                    return 'enemy_crit_5'
                else:
                    if random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) > player_armour:
                        player_health = (player_health - (
                                random.randint(enemy_stats[attacking_enemy]['attack'][0],enemy_stats[attacking_enemy]['attack'][1]) - player_armour))
                        if player_health <= 0:
                            player_health = 0
                return 'enemy_hit_5'
            else:
                return 'enemy_miss_5'
        else:
            return 'enemy_dead_5'

    elif state == "enemy_dead_1":
        attacking_enemy = int(state.split('_')[2])
        print("                                     [ Monster " + str(attacking_enemy) + " is dead! ]\n")
        if enemy_list[attacking_enemy] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_2'

    elif state == "enemy_dead_2":
        attacking_enemy = int(state.split('_')[2])
        print("                                     [ Monster " + str(attacking_enemy) + " is dead! ]\n")
        if enemy_list[attacking_enemy] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_3'

    elif state == "enemy_dead_3":
        attacking_enemy = int(state.split('_')[2])
        print("                                     [ Monster " + str(attacking_enemy) + " is dead! ]\n")
        if enemy_list[attacking_enemy] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_4'

    elif state == "enemy_dead_4":
        attacking_enemy = int(state.split('_')[2])
        print("                                     [ Monster " + str(attacking_enemy) + " is dead! ]\n")
        if enemy_list[attacking_enemy] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_5'

    elif state == "enemy_dead_5":
        attacking_enemy = int(state.split('_')[2])
        print("                                     [ Monster " + str(attacking_enemy) + " is dead! ]\n")
        return 'enemy_turn_purge'

    elif state == "enemy_hit_1":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " hit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_2'

    elif state == "enemy_crit_1":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " crit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_2'

    elif state == "enemy_miss_1":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " missed! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_2'

    elif state == "enemy_hit_2":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " hit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_3'

    elif state == "enemy_crit_2":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " crit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_3'

    elif state == "enemy_miss_2":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " missed! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_3'

    elif state == "enemy_hit_3":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " hit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_4'

    elif state == "enemy_crit_3":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " crit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_4'

    elif state == "enemy_miss_3":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " missed! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_4'

    elif state == "enemy_hit_4":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " hit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_5'

    elif state == "enemy_crit_4":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " crit! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_5'

    elif state == "enemy_miss_4":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " missed! ]\n")
        if enemy_list[attacking_enemy + 1] is None:
            return 'enemy_turn_purge'
        else:
            return 'enemy_attack_sequence_5'

    elif state == "enemy_hit_5":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " hit! ]\n")
        return 'enemy_turn_purge'

    elif state == "enemy_crit_5":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " crit! ]\n")
        return 'enemy_turn_purge'

    elif state == "enemy_miss_5":
        attacking_enemy = int(state.split('_')[2]) - 1
        print("                                         [ " + enemy_list[attacking_enemy] + "\'s "
              + random.choice(enemy_stats[attacking_enemy]['weapons']) + " missed! ]\n")
        return 'enemy_turn_purge'

    elif state == 'player_turn':
        #   resets the raised armour at start of next player turn
        player_armour -= defence_raised
        if defence_raised > 0:
            player_name = player_name.split(" *")[0]
        defence_raised = 0

        print("                                      [ Your turn! ]\n")
        return 'player_turn'

    elif state == 'enemy_turn_purge':
        return 'player_turn'

    elif state == 'player_win':
        clear_screen()
        print("\n                                      [ You won! ]")
        print("                                        ~*Rewards*~")
        print("Gold: " + str(loot_list[0]))
        player_inventory['Gold'] += loot_list[0]
        if len(loot_list) > 1:
            for loot_length in range(len(loot_list) - 1):
                if loot_length != 0:
                    print(loot_list[loot_length] + ": 1")
                    #   ADD TO INVENTORY
                    if loot_list[loot_length] == "Heart Artifact":
                        player_max_health += 5
                        player_health = player_max_health
                    elif loot_list[loot_length] == "True Heart Artifact":
                        player_max_health += 10
                        player_health = player_max_health
                    elif player_inventory.get(loot_list[loot_length]) is None and loot_list[loot_length] != "Gold":
                        player_inventory.update({loot_list[loot_length]: 1})
                    else:
                        player_inventory[loot_list[loot_length]] += 1
        print("Exp: " + str(exp_gain))
        player_exp += exp_gain
        print()
        return 'end'

    elif state == 'end':
        clear_screen()
        return 'end'


# If it is players turn, it will allow player to pick options
def get_player_input(is_player_turn, game_state):
    if is_player_turn is True:
        if game_state == "" or game_state == "attack":
            return input("What do you do?: ").lower()
        elif (game_state == 'hit' or game_state == 'miss' or game_state == 'crit' or game_state == 'enemy_dead'\
                or game_state == 'inventory' or game_state == 'bomb' or game_state == 'greater bomb' or
              game_state == 'back'):
            return ''
        else:
            return input("Press Enter to Continue...")
    else:  # ENEMY TURN
        if (game_state == 'enemy_hit_1' or game_state == 'enemy_crit_1' or game_state == 'enemy_miss_1'
                or game_state == 'enemy_hit_2' or game_state == 'enemy_crit_2' or game_state == 'enemy_miss_2'
                or game_state == 'enemy_hit_3' or game_state == 'enemy_crit_3' or game_state == 'enemy_miss_3'
                or game_state == 'enemy_hit_4' or game_state == 'enemy_crit_4' or game_state == 'enemy_miss_4'
                or game_state == 'enemy_hit_5' or game_state == 'enemy_crit_5' or game_state == 'enemy_miss_5'
                or game_state == 'enemy_dead_1' or game_state == 'enemy_dead_2' or game_state == 'enemy_dead_3'
                or game_state == 'enemy_dead_4' or game_state == 'enemy_dead_5' or game_state == 'end'):
            return ''
        else:
            return input("Press Enter to Continue...")


def get_enemy_amount(enemy_list):
    enemy_amount = 0
    print("        ", end='')
    for length in range(len(enemy_list)):
        if enemy_list[length] is not None:
            enemy_amount += 1
    return enemy_amount


#   prints the fight screen with current information
def fight_screen_display(enemy_list, enemy_stats, player_turn, loot_list, game_state='', error_code=''):
    if game_state != "inventory":
        print("****" * 25)
        print("   ", end='')
        for length in range(len(enemy_list)):
            if enemy_list[length] is not None:
                print(str(length + 1) + "." + " " * 18, end='')
        print("\n    ", end='')
        for length in range(len(enemy_list)):
            if enemy_list[length] is not None:
                print(enemy_list[length] + " " * (20 - len(enemy_list[length])), end='')
        print("\n    ", end='')
        for length in range(len(enemy_list)):
            if enemy_list[length] is not None:
                print(str(enemy_stats[length].get('hp')) + "/" + str(enemy_stats[length].get('max hp'))
                      + " " * (17 - len(str(enemy_stats[length].get('hp')))
                               + len(str(enemy_stats[length].get('max hp')))), end='')
        print("\n\n\n")
        print(" " * (97 - (len(str(player_health)) + len(str(player_max_health)) + len(player_name)))
              + player_name + ": " + str(player_health) + "/" + str(
            player_max_health))
        print(" " * (85 - (len(str(player_damage))) + len(str(player_armour)))
              + "ATK: " + str(player_damage) + " | DEF: " + str(player_armour))
        print("****" * 25)
        #   Print if error code is returned
        print(display_message(error_code))
        #   Print options, using game_state and enemy list for attacks
        game_state = display_options(enemy_list, enemy_stats, loot_list, game_state)
        #   Return the input to fight sequence
    # Enter inventory function
    else:
        game_state = display_options(enemy_list, enemy_stats, loot_list, game_state)
    return get_player_input(player_turn, game_state), game_state


def get_loot(enemy_list):
    given_loot = [random.randint(int(player_level / 2), player_level * 5)]

    for enemy in enemy_list:
        if enemy is not None:
            if monster_dict[enemy]['loot'] is not None:
                if player_level <= 4:
                    if random.randint(1, 2 * player_level) == 1:
                        given_loot.append(monster_dict[enemy]['loot'])
                else:
                    if random.randint(1, 10) == 1:
                        given_loot.append(monster_dict[enemy]['loot'])
                if player_level <= 4:
                    if random.randint(1, 4) == 1:
                        given_loot.append("Health Potion")
                    if random.randint(1, 6) == 1:
                        given_loot.append("Bomb")
                else:
                    if random.randint(1, 4) == 1:
                        given_loot.append("Health Potion")
                    if random.randint(1, 10) == 1:
                        given_loot.append("Grand Health Potion")
                    if random.randint(1, 6) == 1:
                        given_loot.append("Bomb")
                    if random.randint(1, 13) == 1:
                        given_loot.append("Greater Bomb")
    if random.randint(1, 10) == 1:
        given_loot.append("Luck Potion")
    return given_loot


#   runs all sequences in order
def dungeon_fight_sequence():
    fight_sequence_opening()
    enemies_list = dungeon_fight_enemy_type(monster_setup())
    enemy_stats = dungeon_fight_enemy_stats(enemies_list)
    loot_drop = get_loot(enemies_list)
    game_state = ''
    error_code = ''
    #   Player Turn
    while True:
        while True:
            if game_state == 'enemy' or game_state == 'end':
                clear_screen()
                break
            player_input, game_state = fight_screen_display(enemies_list, enemy_stats, True, loot_drop, game_state,
                                                            error_code)
            game_state, error_code = main_operator(player_input, game_state, enemies_list)
            clear_screen()

        if game_state != 'end' and game_state != 'player_win':
            #   Check if a win!
            x = 0
            for check_dead in enemies_list:
                if check_dead is not None and check_dead != 'Dead':
                    x += 1
            if x == 0:
                game_state = 'player_win'
                player_input, game_state = fight_screen_display(enemies_list, enemy_stats, True, loot_drop, game_state,
                                                                error_code)
                game_state, error_code = main_operator(player_input, game_state, enemies_list)
                clear_screen()
        else:
            break

        #   Enemy Turn
        while True:
            if game_state != 'player_win' and game_state != 'end':
                player_input, game_state = fight_screen_display(enemies_list, enemy_stats, False, loot_drop, game_state,
                                                                error_code)
                game_state, error_code = main_operator(player_input, game_state, enemies_list)
                if game_state == 'player_turn':
                    clear_screen()
                    break
                clear_screen()
            else:
                break
        if game_state == 'end':
            clear_screen()
            break

    return player_health, player_max_health, player_armour, player_damage, player_exp, player_level, \
        player_carrying, player_hit_chance, distance_traveled, player_inventory


# takes input and CURRENT game state,
# decides what to do and returns what game-state to turn it to next, or send error code
def main_operator(player_input, game_state, enemy_list):
    if game_state == '':
        if player_input == '1' or player_input == 'attack':
            return "attack", ''
        elif player_input == '2' or player_input == 'defend':
            return "defend", ''
        elif player_input == '3' or player_input == 'inventory':
            return "inventory", ''
        elif player_input == '4' or player_input == 'run':
            return "run", ''
        elif player_input == '':
            return '', ''
        else:
            return '', "Invalid Move [Enter number, or type action]"

    if game_state == 'attack':
        attack_options = get_enemy_amount(enemy_list)
        if player_input == '6' or player_input == 'back':
            return '', ''
        try:
            if 0 < int(player_input) < 6:
                for x in range(attack_options):
                    if int(player_input) == x + 1:
                        return "enemyattack_" + str(x), ''
                return 'attack', 'Invalid Move [Enter one of the options!]'
        except ValueError:
            return 'attack', 'Invalid Move [Enter numbers only!]'

    if game_state == 'back':
        return '',''

    if game_state == 'hit':
        return 'hit', ''

    if game_state == 'bomb':
        return 'bomb', ''

    if game_state == 'greater bomb':
        return 'greater bomb', ''

    if game_state == 'crit':
        return 'crit', ''

    if game_state == 'miss':
        return 'miss', ''

    if game_state == 'enemy_dead':
        return 'attack', 'It\'s already dead!'

    if game_state == 'enemy':
        return 'enemy', ''

    if game_state == 'inventory':
        return 'enemy', ''

    if game_state == 'run':
        return 'run_attempt', ''

    if game_state == 'defend' or game_state == 'run_attempt':
        return "enemy", ''

    if game_state == 'player_turn':
        return '', ''

    if game_state == 'enemy_turn_purge':
        if player_health <= 0:
            game_over()
        return 'player_turn', ''

    if game_state == 'player_win':
        return 'end', ''

    if game_state == 'end':
        return 'end', ''

    if game_state == 'enemy_hit_1':
        return 'enemy_hit_1', ''
    if game_state == 'enemy_crit_1':
        return 'enemy_crit_1', ''
    if game_state == 'enemy_miss_1':
        return 'enemy_miss_1', ''

    if game_state == 'enemy_hit_2':
        return 'enemy_hit_2', ''
    if game_state == 'enemy_crit_2':
        return 'enemy_crit_2', ''
    if game_state == 'enemy_miss_2':
        return 'enemy_miss_2', ''

    if game_state == 'enemy_hit_3':
        return 'enemy_hit_3', ''
    if game_state == 'enemy_crit_3':
        return 'enemy_crit_3', ''
    if game_state == 'enemy_miss_3':
        return 'enemy_miss_3', ''

    if game_state == 'enemy_hit_4':
        return 'enemy_hit_4', ''
    if game_state == 'enemy_crit_4':
        return 'enemy_crit_4', ''
    if game_state == 'enemy_miss_4':
        return 'enemy_miss_4', ''

    if game_state == 'enemy_hit_5':
        return 'enemy_hit_5', ''
    if game_state == 'enemy_crit_5':
        return 'enemy_crit_5', ''
    if game_state == 'enemy_miss_5':
        return 'enemy_miss_5', ''

    if game_state == 'enemy_attack_sequence_1':
        if player_health <= 0:
            game_over()
        return 'enemy_attack_sequence_1', ''
    if game_state == 'enemy_attack_sequence_2':
        if player_health <= 0:
            game_over()
        return 'enemy_attack_sequence_2', ''
    if game_state == 'enemy_attack_sequence_3':
        if player_health <= 0:
            game_over()
        return 'enemy_attack_sequence_3', ''
    if game_state == 'enemy_attack_sequence_4':
        if player_health <= 0:
            game_over()
        return 'enemy_attack_sequence_4', ''
    if game_state == 'enemy_attack_sequence_5':
        if player_health <= 0:
            game_over()
        return 'enemy_attack_sequence_5', ''

    if game_state == 'enemy_dead_1':
        return 'enemy_dead_1', ''
    if game_state == 'enemy_dead_2':
        return 'enemy_dead_2', ''
    if game_state == 'enemy_dead_3':
        return 'enemy_dead_3', ''
    if game_state == 'enemy_dead_4':
        return 'enemy_dead_4', ''
    if game_state == 'enemy_dead_5':
        return 'enemy_dead_5', ''


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


def main():
    dungeon_fight_sequence()


if __name__ == "__main__":
    main()
