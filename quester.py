#!/usr/bin/python3
#add more random events, bosses, shields, weapons, and armor

from dungeon import Dungeon
from battlefield import Battlefield
from player import Player
from monster import Monster
from math import ceil, floor
from random import randint


class Quester:

    def __init__(self):
        self.player         = Player(self)
        self.battlefield    = Battlefield()
        self.companion      = None
        self.in_dungeon     = False

    def startup(self):
        self.location_names1 = ("Ab","Bret","Pha","Lem","Ra","The","Tra","Vem","Ple","Cro","Ad","Ne")
        self.location_names2 = ("seph","tro","zem","ma","nem","lo","hi","sa","de","yo","thra","pal")
        self.location_names3 = ("la","me","se","et","kra","men","wa","tire","du","od","le")
        self.next_locations  = []
        self.steps_since_town = 0

        for iterator in range(5):
            self.next_locations.append(self.location_names1[randint(0, len(self.location_names1) - 1)] + self.location_names2[randint(0, len(self.location_names2) - 1)] + self.location_names3[randint(0, len(self.location_names3) - 1)])

        print("================================================================================")
        print(" _______    _       _    ________    _______    _________    ________    _____  \n|  ___  |  | |     | |  |  ______|  |  _____|  |___   ___|  |  ______|  |  _  |\n| |   | |  | |     | |  | |______   | |_____       | |      | |______   | |_| |\n| |   | |  | |     | |  |  ______|  |_____  |      | |      |  ______|  |    _|\n| |  \\\\ |  | |     | |  | |               | |      | |      | |         | |\\ \\\n| |___\\\\|  | |_____| |  | |______    _____| |      | |      | |______   | | \\ \\\n|______\\\\  |_________|  |________|  |_______|      |_|      |________|  |_|  \\_\\")
        print("\n================================================================================\n")

        character_creation = self.get_selected_option(("1", "2"), "Would you like to\n1)Load a player save\n2)Create a new player\n>>>", "Please select either '1' or '2'.")

        create_new = character_creation == "2"

        while True:
            if self.player.init(create_new):
                break

        print("Enter 'h' to view commands.")

    def get_command(self):
        self.commands = {"h":self.print_commands, "ld":self.player.load, "a":self.advance, "s":self.player.save, "exit":self.exit_game, "mp":self.town_map, "rs":self.player.rest, "dev":self.player.set_unbeatable}

        self.player.print_status()
        command = self.get_selected_option(self.commands, ">>>", "'{}' is not a valid command.").lower()
        self.commands[command]()


    def encounter_multiple_monsters(self):
        monster_count = randint(2, 4)
        enemies = []
        for monster_number in range(monster_count):
            monster             = Monster(self)
            monster.health      = round(monster.health / monster_count)
            monster.max_health  = monster.health
            monster.strength    = round(monster.strength / monster_count)
            monster.number      = monster_number + 1
            enemies.append(monster)
        self.battlefield.encounter_monsters(self.player, enemies, self.companion)

    def encounter_monster(self):
        monster = Monster(self)
        self.battlefield.encounter_monsters(self.player, [monster], self.companion)

    def print_commands(self):
        command_descriptions = {"h":"Displays all available commands.", "ld":"Allows the player to load a previous save file.", "a":"Advances the player to the next event, encounter, or location.", "s":"Allows the player to save their current character to a file.", "mp": "Shows the player a map with the locations of the next 5 towns.", "rs":"The player rests and consumes 20 food, which restores 10 health points and some mana.", "exit":"Exits the game. Make sure you save first!", "dev":"Gives the player infinite supplies, allowing them to test features."}
        
        for command in self.commands:
            if command in command_descriptions:
                print("{0} : {1}".format(command, command_descriptions[command]))
            else:
                print(command)

    def refresh_map(self):
        self.current_map = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        for line in range(14):
            for iterator in range(80):
                self.current_map[line].append(" ")

        self.player_location = randint(1,6)
        self.current_map[randint(3, 10)][self.player_location : self.player_location + 5] = "O-You"
        horizontal = 0

        for town in self.next_locations:
            town = "X-" + town
            horizontal = horizontal + randint(10, 14)
            self.current_map[randint(1, 13)][horizontal : horizontal + len(town)] = list(town)

        for line in range(14):
            self.current_map[line] = "".join(self.current_map[line])
        self.current_map = "\n".join(self.current_map)

    def town_map(self):
        print(self.current_map)

    def advance(self):
        occurrences = (self.encounter_monster, self.encounter_monster, self.encounter_monster, self.encounter_monster, self.encounter_location, self.encounter_traveler, self.encounter_multiple_monsters, self.encounter_monster, self.encounter_monster, self.encounter_monster, self.encounter_monster, self.encounter_location, self.encounter_traveler, self.encounter_multiple_monsters, self.encounter_companion, self.encounter_dungeon)
        self.steps_since_town += 1
        WEIGHTED_TOWN_DISTANCE = 6
        if self.player.food == 0:
            print("Warning: You have no food left. You must get some or you will starve to death.")
        if self.steps_since_town == WEIGHTED_TOWN_DISTANCE:
            self.location_weight = 8
        if self.steps_since_town > WEIGHTED_TOWN_DISTANCE:
            self.location_weight -= 1
            if randint(0, self.location_weight) == self.location_weight:
                self.encounter_location()
            else:
                occurrences[randint(0, len(occurrences) - 1)]()
        else:
            occurrences[randint(0, len(occurrences) - 1)]()
        if self.player.food == 0:
            print("\nYou lost! You died of starvation.")
            exit()
        self.player.food -= (self.player.max_health + self.player.strength) // 20
        if self.player.food < 0:
            self.player.food = 0
        self.player.health += ceil(self.player.max_health / 50)
        if self.player.health > self.player.max_health:
            self.player.health = self.player.max_health
        self.player.mana += self.player.mana_growth
        if self.player.mana > self.player.max_mana:
            self.player.mana = self.player.max_mana
        if self.companion != None:
            self.companion.health += self.companion.max_health // 10
            if self.companion.health > self.companion.max_health:
                self.companion.health = self.companion.max_health
            self.companion.lifetime -= 1
            if self.companion.lifetime == 0:
                print("{0} the {1} {2} has left your company.".format(self.companion.name, self.companion.species, self.companion.character_class))
                self.companion = None

    def encounter_location(self):
        self.steps_since_town = 0
        town_name = self.next_locations[0]
        self.deals = randint(50, 200) / 100
        print("You arrived at the town of {}.".format(town_name))
        self.player.visited_cities.append(town_name)
        while True:
            self.player.print_status()
            enter = self.get_selected_option(("1", "2", "3"), "What would you like to do\n1)Enter the marketplace\n2)Enter the wizard's hut\n3)Leave the town\n>>>","Please select an option '1' through '3'")
            if enter == "1":
                while self.encounter_location_marketplace():
                    continue
            if enter == "2":
                while self.encounter_location_wizards_hut():
                    continue
            if enter == "3":
                leave = input("Are you sure you want to leave the town of {}? (y/n)\n>>>".format(town_name)).lower()
                if leave == "y":
                    print("You left {}.".format(town_name))
                    del self.next_locations[0]
                    self.next_locations.append(self.location_names1[randint(0, len(self.location_names1) - 1)] + self.location_names2[randint(0, len(self.location_names2) - 1)] + self.location_names3[randint(0, len(self.location_names3) - 1)])
                    self.refresh_map()
                    return None

    def encounter_location_marketplace(self):
        gold_price = .7 * self.deals
        food_price = .3 * self.deals
        
        self.player.print_status()
        print("You entered the marketplace.")
        purchase = self.get_selected_option(("1", "2", "3"), "What would you like to buy?\n1)Gold - {0} loot for one piece\n2)Food - {1} gold for one piece\n3)Exit\n>>>".format(round(gold_price, 2), round(food_price, 2)), "Please select an option '1' through '3'")
        
        if purchase == "1":
            try:
                amount = input("How much gold would you like to buy?\n>>>")
                if amount == "max":
                    amount = round(self.player.loot / gold_price)
                else:
                    amount = int(amount)
            except ValueError:
                pass
            else:
                cost = floor(amount * gold_price)
                if cost == 0 and amount > 0:
                    cost = 1
                confirm = input("That will cost {} loot. Are you sure you want to make the purchase? (y/n)\n>>>".format(cost)).lower()
                if confirm == "y":
                    if self.player.loot >= cost:
                        self.player.loot -= cost
                        self.player.gold += amount
                        print("You now have {} gold.".format(self.player.gold))
                    else:
                        print("Not enough loot!")

        elif purchase == "2":
            try:
                amount = input("How much food would you like to buy?\n>>>")
                if amount == "max":
                    amount = round(self.player.gold / food_price)
                else:
                    amount = int(amount)
            except ValueError:
                pass
            else:
                cost = floor(amount * food_price)
                if cost == 0 and amount > 0:
                    cost = 1
                confirm = input("That will cost {} gold. Are you sure you want to make the purchase? (y/n)\n>>>".format(cost)).lower()
                if confirm == "y":
                    if self.player.gold >= cost:
                        self.player.gold -= cost
                        self.player.food += amount
                        print("You now have {} food.".format(self.player.food))
                    else:
                        print("Not enough gold!")
        else:
            return False

        return True

    def encounter_location_wizards_hut(self):
        heal_price = ((self.player.strength + self.player.max_health) / 11) * self.deals
        mana_price = (self.player.max_mana / 3) * self.deals
        max_mana_price = 15 * self.deals
        mana_growth_price = 25 * self.deals
        strength_price = 20 * self.deals
        health_price = 20 * self.deals
        price_list = (heal_price, mana_price, strength_price, health_price, max_mana_price, mana_growth_price)
          
        self.player.print_status()
        print("You entered the wizard's hut.")
        purchase = self.get_selected_option(("1","2","3","4","5","6","7"), "Wizard: How can I help you today?\n1)Heal - restore full health for {0} gold\n2)Mana potion - restore to full mana for {1} gold\n3)Strength potion - increase Strength by 1 point for {2} gold\n4)Health potion - increase max health by 1 point for {3} gold\n5)Max mana upgrade - increade max mana by 1 point for {4} gold\n6)Mana increase upgrade - increase mana growth by 1 point for {5} gold\n7)Exit\n>>>".format(round(heal_price, 2), round(mana_price, 2), round(strength_price, 2), round(health_price, 2), round(max_mana_price, 2), round(mana_growth_price, 2)), "Please select an option '1' through '7'.")

        if purchase != "7":
            cost = round(price_list[int(purchase) - 1]) 
            if self.player.gold < cost:
                print("Not enough gold!")
                return False
            self.player.gold -= cost

        if purchase == "1":
            self.player.health = self.player.max_health
            print("You were healed to max health.")
        elif purchase == "2":
            self.player.mana = self.player.max_mana
            print("You now have {} mana.".format(self.player.mana))
        elif purchase == "3":
            self.player.strength += 1
            print("You now have {} strength.".format(self.player.strength))
        elif purchase == "4":
            self.player.max_health += 1
            print("Your max health is now {}.".format(self.player.max_health))
        elif purchase == "5":
            self.player.max_mana += 1
            print("Your max mana is now {}.".format(self.player.max_mana))
        elif purchase == "6":
            self.player.mana_growth += 1
            print("Your mana growth rate is now {}.".format(self.player.mana_growth))
        else:
            return False

        return True

    def encounter_traveler(self):
        tradeables_list = ("gold", "loot", "mana", "food")
        tradeables_reference = {"gold":self.player.gold, "loot":self.player.loot, "mana":self.player.mana, "food":self.player.food}
        tradeable = tradeables_list[randint(0, len(tradeables_list) - 1)]
        while True:
            payment = tradeables_list[randint(0, len(tradeables_list) - 1)]
            if payment != tradeable:
                break
        tradeable_amount = randint(1, 20)
        payment_amount = randint(1, 20)

        if len(self.player.visited_cities) > 0: 
            destination = self.player.visited_cities[-1]
        if len(self.player.visited_cities) == 0:
            destination = self.location_names1[randint(0, len(self.location_names1) - 1)] + self.location_names2[randint(0, len(self.location_names2) - 1)] + self.location_names3[randint(0, len(self.location_names3) - 1)]
        print("You meet a traveler on the road, passing you on his way to {}.".format(destination))
        
        if tradeables_reference[payment] < payment_amount:
            print("The traveler offers to give you {0} {1} in exchange for {2} {3}.\nUnfortunately, you do not have enough {3}.\nYou and the traveler continue on your seperate ways.".format(tradeable_amount, tradeable, payment_amount, payment))
            return None
        
        trade = self.get_selected_option(("y", "n"), "The traveler offers to give you {0} {1} in exchange for {2} {3}. Do you accept? (y/n)\n>>>".format(tradeable_amount, tradeable, payment_amount, payment), "Please use 'y' or 'n'.").lower()
        if trade == "y":
            print("You and the traveler exchange items.")
            tradeables_reference[payment] -= payment_amount
            tradeables_reference[tradeable] += tradeable_amount
            self.player.gold = tradeables_reference["gold"]
            self.player.loot = tradeables_reference["loot"]
            self.player.mana = tradeables_reference["mana"]
            self.player.food = tradeables_reference["food"]
            print("You now have {0} {1} and {2} {3}.".format(tradeables_reference[payment], payment, tradeables_reference[tradeable], tradeable))
            if self.player.mana > self.player.max_mana:
                self.player.mana = self.player.max_mana
            return None
        else:
            print("You and the traveler continue on your seperate ways.")
            return None

    def encounter_companion(self):
        companion = Player(self)
        companion.init_companion()

        print("You come across a(n) {0}, {1} the {2}, who offers to join you on your adventure. He has {3} health and {4} strength.".format(companion.character_class, companion.name, companion.species, companion.health, companion.strength))
        accept_companion = self.get_selected_option(("y", "n"), "Do you accept the companion? He will replace any current companion. (y/n)\n>>>", "Please use 'y' or 'n'.")
        if accept_companion == "y":
            self.companion = companion
            print("{} is now your companion.".format(self.companion.name))
        if accept_companion == "n":
            print("You decline the {}'s offer and go on your way.".format(companion.name))
            
    def encounter_dungeon(self):
        enter_dungeon = self.get_selected_option(("y", "n"), "You encountered a dungeon. Would you like to enter? (y/n)\n>>>", "Please use 'y' or 'n'.")
        if enter_dungeon == "y":
            self.in_dungeon = True
            self.dungeon = Dungeon(self)
            self.dungeon.enter()
            self.in_dungeon = False

    def exit_game(self):
        leave_game = input("Are you sure you want to exit the game? (y/n)\n>>>").lower()
        if leave_game == "y":
            exit()
        else:
            return None

    def get_selected_option(self, choices, question, error_message):
        while True:
            choice = input(question).lower()
            if choice in choices:
                return choice
            else:
                error_message = error_message.format(choice) if "{}" in error_message else error_message
                print(error_message)

        



quester = Quester()
quester.startup()
while True:
    quester.get_command()

