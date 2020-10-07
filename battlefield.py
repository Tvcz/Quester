from random import randint

class Battlefield:

    def __init__(self, dungeon=None):
        self.dungeon = dungeon

    def encounter_monsters(self, player, enemies, companion):
        self.battle_commands = {"h":self.battle_command_print, "st":player.print_status, "at":player.attack, "re":player.retreat, "ab":player.ability, "ce":""}
        player.damage_affector = 0
        player.defense_affector = 0
        self.enemies = enemies

        for monster in self.enemies:
            print("[{0}] You encountered a(n) {1}, {2} the {3}. He has {4} health.".format(monster.number, monster.species, monster.name, monster.character_class, monster.health))    
        if len(self.enemies) > 1:
            print("You have encountered multiple enemies! Use the 'ce' command to change the selected target.")
        self.current_enemy = self.enemies[0]
        while len(self.enemies) > 0 and player.health > 0:
            if self.current_enemy not in self.enemies:
                self.current_enemy = self.enemies[0]
            if len(self.enemies) > 0:
                print("SELECTED TARGET: {0} the {1} {2} ({3} health)".format(self.current_enemy.name, self.current_enemy.species, self.current_enemy.character_class, self.current_enemy.health))    

            command = player.quester.get_selected_option(("at", "ab", "re", "st", "h", "ce"), ">>>", "'{}' is either not a valid command or cannot be used in battle.")
            if command == "at":
                self.battle_commands[command](self.current_enemy)
            elif command == "re":
                if self.dungeon == None:
                    if self.battle_commands[command]():
                        break
                if self.dungeon != None:
                    if self.dungeon.retreat():
                        break
            elif command == "ce":
                for monster in self.enemies:
                    print("[{0}] {1}, {2} the {3}. {4} health. ".format(monster.number, monster.character_class, monster.name, monster.species, monster.health))
                current_enemy_number = int(player.quester.get_selected_option([str(n) for n in range(1, len(self.enemies) + 1)], "Select an enemy by entering their number.\n>>>", "Please enter a number between 1 and {}.".format(len(self.enemies))))
                for monster in self.enemies:
                    if monster.number == current_enemy_number:
                        self.current_enemy = monster
                        break
                continue
            else:
                self.battle_commands[command]()
                continue
            if companion != None and len(self.enemies) > 0:
                companion.attack(self.enemies[randint(0, len(self.enemies) - 1)])
            for monster in self.enemies:
                if companion != None and randint(0, 1):
                    monster.attack(companion)
                else:
                    monster.attack(player)
        return self.enemies

    def battle_command_print(self):
        battle_command_descriptions = {"h":"Displays all available battle commands.", "st":"Lists player stats and supplies.", "at":"Attacks the current enemy if in combat.", "re":"Attempts to escape the enemy currently fighting the player.", "ab":"Uses the player's class ability if they have at least 15 mana.", "ce":"Allows the player to select an enemy to target if in a multi-enemy battle."}
        
        for command in self.battle_commands:
            if command in battle_command_descriptions:
                print("{0} : {1}".format(command, battle_command_descriptions[command]))
            else:
                print(command)

