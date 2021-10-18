from random import randint
from monster import Monster
from battlefield import Battlefield
from math import ceil

class Dungeon:

    def __init__(self, quester):
        self.battlefield = Battlefield(self)
        self.quester = quester
        self.quester.player = quester.player
        self.quester.player.dungeon_location = [0, 0]
        self.room_count = 0
        dungeon_objects = ["M", "M", "M", "M", "B", "g", "l", "m", "f"]
        self.dungeon_grid = []
        rows = randint(3, 5)
        rooms = randint(3, 12)
        for iterator in range(rows):
            self.dungeon_grid.append([])
        for row in self.dungeon_grid:
            for iterator in range(rooms):
                self.dungeon_grid[self.dungeon_grid.index(row)].append([])
        for row in self.dungeon_grid:
            for room in row:
                self.room_count += 1
                dungeon_object = dungeon_objects[randint(0, len(dungeon_objects) - 1)]
                    
                self.dungeon_grid[self.dungeon_grid.index(row)][row.index(room)].append(dungeon_object)
                
                if dungeon_object in ("g", "l", "m", "f"):
                    self.dungeon_grid[self.dungeon_grid.index(row)][row.index(room)].append(randint(30, 60))
                
                if dungeon_object == ("M"):
                    monster_count = randint(1, 3)
                    enemies = []
                    for monster_number in range(monster_count):
                        monster             = Monster(quester)
                        monster.health      = round(monster.health / monster_count)
                        monster.max_health  = monster.health
                        monster.strength    = round(monster.strength / monster_count)
                        monster.number      = monster_number + 1
                        enemies.append(monster)
                    self.dungeon_grid[self.dungeon_grid.index(row)][row.index(room)].append(enemies)

                if dungeon_object == "B":
                    dungeon_objects.remove(dungeon_object)
                    boss                    = Monster(quester)
                    boss.health             *= randint(2, 3)
                    boss.max_health         = boss.health
                    boss.strength           *= randint(2, 3)
                    boss.character_class    = "Boss" 
                    boss.number             = 1
                    self.dungeon_grid[self.dungeon_grid.index(row)][row.index(room)].append([boss])

        self.dungeon_grid[0][0].append(self.quester.player)
        self.dungeon_grid[0][0].append("visited")


    def enter(self):
        print("You entered a dungeon. It has {} rooms.".format(self.room_count))
        self.in_dungeon = True
        self.enter_room()
        while self.in_dungeon:
            self.get_command()

    def retreat(self):
        if randint(0, 1):
            print("You successfully retreated from the room.")
            return True
        else:
            print("You failed to retreat from the room.")
            return False

    def move(self):
        self.print_dungeon()
        self.dungeon_grid[self.quester.player.dungeon_location[1]][self.quester.player.dungeon_location[0]].remove(self.quester.player)
        while True:
            direction = self.quester.get_selected_option(("n", "s", "e", "w"), "Select a direction to move towards. (n/s/e/w)\n>>> ", "Please use 'n', 's', 'e', or 'w'.")
            if direction == "n" and self.quester.player.dungeon_location[1] < len(self.dungeon_grid) - 1:
                self.quester.player.dungeon_location[1] += 1
            elif direction == "s" and self.quester.player.dungeon_location[1] > 0:
                self.quester.player.dungeon_location[1] -= 1
            elif direction == "e" and self.quester.player.dungeon_location[0] < len(self.dungeon_grid[self.quester.player.dungeon_location[1]]) - 1:
                self.quester.player.dungeon_location[0] += 1
            elif direction == "w" and self.quester.player.dungeon_location[0] > 0:
                self.quester.player.dungeon_location[0] -= 1
            else:
                print("You cannot travel past the dungeon boundaries!")
                continue
            break
        self.dungeon_grid[self.quester.player.dungeon_location[1]][self.quester.player.dungeon_location[0]].append(self.quester.player)
        self.dungeon_grid[self.quester.player.dungeon_location[1]][self.quester.player.dungeon_location[0]].append("visited")
        if self.quester.player.food == 0:
            print("Warning: You have no food left. You must get some or you will starve to death.")

    def get_command(self):
        self.print_dungeon()
        self.commands = {"rs":self.quester.player.rest, "mp":self.print_dungeon, "h":self.print_commands, "leave":self.exit_dungeon, "st":self.quester.player.print_status}
        command = self.quester.get_selected_option(("rs", "mv", "mp", "h", "leave", "st"), ">>> ", "'{}' is not a valid command.")
        if command == "mv":
            self.move()
            self.enter_room()
        else:
            self.commands[command]()

    def print_commands(self):
        self.command_descriptions = {"rs":"The player rests and consumes 20 food, which restores 10 health points and some mana.", "mv":"Moves the player in the specified direction.","mp":"Prints the dungeon map, which shows player location and visited rooms.","h":"Displays the commands and their respective descriptions.","leave":"Exits the player from the dungeon.", "st":"Lists player stats and supplies."}
        for command in self.command_descriptions:
            print("{0} : {1}".format(command, self.command_descriptions[command]))

    def exit_dungeon(self):
        leave = input("Are you sure you want to exit the dungeon? (y/n)\n>>> ").lower()
        if leave == "y":
            self.in_dungeon = False

    def print_dungeon(self):
        for row in reversed(self.dungeon_grid):
            length = len(row)
            print("-" + ("----" * length))
            print("|" + ("   |" * length))
            row_view = "|"
            for room in row:
                if self.quester.player in room:
                    room_view = "*P*|".format(room[0])
                elif "visited" in room:
                    if room[1] == 0 or room[1] == []:
                        room_view = " {}X|".format(room[0])
                    else:
                        room_view = " {} |".format(room[0])
                else:
                    room_view = "   |"
                row_view += room_view
            print(row_view)
            print("|" + ("   |" * length))
        print("-" + ("----" * length))

    def enter_room(self):
        room_identifier = self.dungeon_grid[self.quester.player.dungeon_location[1]][self.quester.player.dungeon_location[0]][0]
        room_object  = self.dungeon_grid[self.quester.player.dungeon_location[1]][self.quester.player.dungeon_location[0]][1]
        
        if room_object == 0 or room_object == []:
            print("This room has already been entered and is now empty.")
        else:
            if room_identifier in ("M", "B"):
                self.dungeon_grid[self.quester.player.dungeon_location[1]][self.quester.player.dungeon_location[0]][1] = self.battlefield.encounter_monsters(self.quester.player, room_object, self.quester.companion)

            if room_identifier in ("g", "l", "m", "f"):
                if room_identifier == "g":
                    print("You found {} gold!".format(room_object))
                    self.quester.player.gold += room_object
                if room_identifier == "l":
                    self.quester.player.loot += room_object 
                    print("You found {} loot!".format(room_object))
                if room_identifier == "m":
                    self.quester.player.mana += room_object
                    print("You found {} mana!".format(room_object))
                if room_identifier == "f":
                    self.quester.player.food += room_object
                    print("You found {} food!".format(room_object))
                self.dungeon_grid[self.quester.player.dungeon_location[1]][self.quester.player.dungeon_location[0]][1] = 0
        if self.quester.player.food == 0:
            print("\nYou lost! You died of starvation.")
            exit()
        self.quester.player.food -= (self.quester.player.max_health + self.quester.player.strength) // 20
        if self.quester.player.food < 0:
            self.quester.player.food = 0
        self.quester.player.health += ceil(self.quester.player.max_health / 50)
        if self.quester.player.health > self.quester.player.max_health:
            self.quester.player.health = self.quester.player.max_health
        self.quester.player.mana += self.quester.player.mana_growth
        if self.quester.player.mana > self.quester.player.max_mana:
            self.quester.player.mana = self.quester.player.max_mana
        if self.quester.companion != None:
            self.quester.companion.health += self.quester.companion.max_mana // 10
            if self.quester.companion.health > self.quester.companion.max_health:
                self.quester.companion.health = self.quester.companion.max_health
            self.quester.companion.lifetime -= 1
            if self.quester.companion.lifetime == 0:
                print("{0} the {1} {2} has left your company.".format(self.quester.companion.name, self.quester.companion.species, self.quester.companion.character_class))
                self.quester.companion = None

