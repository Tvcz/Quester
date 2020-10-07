from random import randint
from creature import Creature

character_classes = ((25, 65), (65, 25), (40, 50), (55, 35), (15, 75))
class_list = ("Archer", "Assassin", "Berserker", "Mage", "Warrior")
attack_bonus = {"Archer":"Mage", "Mage":"Assassin", "Assassin":"Berserker", "Warrior":"Archer", "Berserker":"Warrior", "Boss":"Boss"}
defense_bonus = {"Archer":"Assassin", "Mage":"Berserker", "Assassin":"Warrior", "Warrior":"Mage", "Berserker":"Archer", "Boss":"Boss"}
ally_species = ["Human", "Elf", "Dwarf", "Wolf", "Dragon"]
companion_names1 = ["Gala", "Rek", "Ter", "Lot", "Ang", "Andri", "Thran", "Rum", "Dur", "Kil", "Fer", "Nok"]
companion_names2 = ["et", "al", "riel", "lan", "nei", "ras", "duil", "eli", "rion", "dain", "es", "fari"]

class Player(Creature):

    def __init__(self, quester):
        self.quester            = quester
        self.gold               = 0
        self.loot               = 0
        self.mana               = 0
        self.mana_growth        = 1
        self.max_mana           = 25
        self.food               = 50
        self.enemies_defeated   = 0
        self.bosses_defeated    = 0
        self.visited_cities     = []
        self.damage_affector    = 0
        self.defense_affector   = 0
    def init(self, create_new):
        if not create_new:
            return self.load()

        name = input("Enter a name for your character:\n>>>")
        character_class = input("Select a character class:\n1)Archer\n2)Assassin\n3)Berserker\n4)Mage\n5)Warrior\n>>>")
        if not character_class in ("1", "2", "3", "4", "5"):
            print("Please enter a number 1 through 5.")
            return False

        self.name               = name
        self.character_class    = class_list[int(character_class) - 1]
        self.strength           = character_classes[int(character_class) - 1][0]
        self.health             = character_classes[int(character_class) - 1][1]
        self.max_health         = self.health
        self.species            = "Human"

        return True

    def init_companion(self):
        player_health_and_strength  = self.quester.player.max_health + self.quester.player.strength
        character_class             = randint(0, len(character_classes) - 1)
        self.name                   = companion_names1[randint(0, len(companion_names1) - 1)] + companion_names2[randint(0, len(companion_names2) - 1)] 
        self.character_class        = class_list[character_class]
        self.strength               = round((player_health_and_strength) * (character_classes[int(character_class)][0] / 100)) + randint(-3, 3)
        self.health                 = round((player_health_and_strength) * (character_classes[int(character_class)][1] / 100)) + randint(-3, 3)
        self.max_health             = self.health
        self.species                = ally_species[randint(0, len(ally_species) - 1)]
        self.lifetime               = randint(6, 10)

        if self.species == "Wolf":
            self.character_class = "Berserker"
        if self.species == "Dragon":
            self.character_class = "Mage"
            self.strength *= 3
            self.health *= 3
            self.max_health = self.health
            

    def load(self):
        save_name = input("Enter the name of your save or leave blank for default:\n>>>").lower()
        try:
            with open(save_name + " quester_save.txt", "r") as load_file:
                load_file = load_file.read()
                load_file = load_file.split()
        except:
            print("Error! Save not found!")
            return False

        self.name              = load_file[0]
        self.character_class   = load_file[1]
        self.max_health        = int(load_file[2])
        self.strength          = int(load_file[4])
        self.health            = int(load_file[3])
        self.gold              = int(load_file[5])
        self.loot              = int(load_file[6])
        self.mana              = int(load_file[7])
        self.mana_growth       = int(load_file[8])
        self.max_mana          = int(load_file[9])
        self.food              = int(load_file[10])
        self.enemies_defeated  = int(load_file[11])
        self.bosses_defeated   = int(load_file[12])
        self.visited_cities    = [] if load_file[13] == "," else load_file[13].split(",")

        print("Save found: {0} the {1}\nHealth : {3}/{2} ({4}%)\nStrength : {5}\nGold : {6}\nLoot : {7}\nMana : {8}/{14} ({15}%)\nMana growth : {9}\nFood : {10}\nEnemies defeated : {11}\nBosses defeated : {12}\nVisited cities : {13}".format(self.name, self.character_class, self.max_health, self.health, round(float(self.health) / int(self.max_health) * 100, 2), self.strength, self.gold, self.loot, self.mana, self.mana_growth, self.food, self.enemies_defeated, self.bosses_defeated, ", ".join(self.visited_cities), self.max_mana, round((int(self.mana) / int(self.max_mana)) * 100, 2)))

        select_save = input("\nWould you like to select this save? (y/n)\n>>>").lower()
        if select_save != "y" and select_save != "n":
            print("Please input 'y' or 'n'.")
            return False

        return select_save == "y"

    def save(self):
        save_name = input("Enter a name for your save or leave blank for default:\n>>>").lower()

        confirmation = self.quester.get_selected_option(("y", "n"), 'Are you sure you want to overwrite save "{}"? (y/n)\n>>>'.format(save_name), "Please use 'y' or 'n'.")
        if confirmation == "y":
            with open(save_name + " quester_save.txt", "w+") as save_file:
                visited_cities = [","] if len(self.visited_cities) == 0 else self.visited_cities
                save_file.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13}".format(self.name, self.character_class, self.max_health, self.health, self.strength, self.gold, self.loot, self.mana, self.mana_growth, self.max_mana, self.food, self.enemies_defeated, self.bosses_defeated, ",".join(visited_cities)))

    def die(self, enemy):
        if self.quester.player == self:
            print("\nYou lost! You were killed by {0} the {1} {2}.".format(enemy.name, enemy.species, enemy.character_class))
            exit()
        if self.quester.companion == self:
            print("Your companion, {0} the {1} {2}, was killed by {3} the {4} {5}.".format(self.name, self.species, self.character_class, enemy.name, enemy.species, enemy.character_class))
            self.quester.companion = None

    def rest(self):
        if self.food >= 20:
            self.food -= 20
            self.health += 10
            if self.health > self.max_health:
                self.health = self.max_health
            self.mana += self.mana_growth
            if self.mana > self.max_mana:
                self.mana = self.max_mana
            print("You rested and ate 20 food, restoring 10 of your health and {} of your mana.".format(self.mana_growth))
        else:
            print("You do not have enough food (20) to rest.")

    def retreat(self):
        escape = randint(0, 1)

        if escape:
            print("You successfully escaped {0} the {1}.".format(self.quester.battlefield.current_enemy.name, self.quester.battlefield.current_enemy.character_class))
            return True
        if not escape: 
            print("You failed to retreat from {0} the {1}.".format(self.quester.battlefield.current_enemy.name, self.quester.battlefield.current_enemy.character_class))
            return False

    def ability(self):
        abilities = {"Archer":self.fire_arrow,"Assassin":self.critical_hit,"Berserker":self.shout,"Mage":self.force_field,"Warrior":self.battle_valour}

        if self.mana >= 15:
            self.mana -= 15
        else:
            print("You do not have enough mana (15) to perform an ability!")
            return None
        abilities[self.character_class]()

    def fire_arrow(self):
        bonus = 0
        if not self.quester.in_dungeon:
            if attack_bonus[self.character_class] == self.quester.battlefield.current_enemy.character_class:
                bonus = randint(self.strength // 4, self.strength // 2)
            damage = round(2 * self.strength) + randint(-1, 1) + bonus 
            self.quester.battlefield.current_enemy.health -= damage
            if self.quester.battlefield.current_enemy.health < 0:
                self.quester.battlefield.current_enemy.health = 0
            print("{0} used Fire Arrow against {1} for {2} damage.\n{1} has {3} health remaining.".format(self.name, self.quester.battlefield.current_enemy.name, damage, self.quester.battlefield.current_enemy.health))
            if self.quester.battlefield.current_enemy.health == 0:
                self.quester.battlefield.current_enemy.die(self)
        
        if self.quester.in_dungeon:
            if attack_bonus[self.character_class] == self.quester.dungeon.battlefield.current_enemy.character_class:
                bonus = randint(self.strength // 4, self.strength // 2)
            damage = round(2 * self.strength) + randint(-1, 1) + bonus 
            self.quester.dungeon.battlefield.current_enemy.health -= damage
            if self.quester.dungeon.battlefield.current_enemy.health < 0:
                self.quester.dungeon.battlefield.current_enemy.health = 0
            print("{0} used Fire Arrow against {1} for {2} damage.\n{1} has {3} health remaining.".format(self.name, self.quester.dungeon.battlefield.current_enemy.name, damage, self.quester.dungeon.battlefield.current_enemy.health))
            if self.quester.dungeon.battlefield.current_enemy.health == 0:
                self.quester.dungeon.battlefield.current_enemy.die(self)

    def critical_hit(self):
        critical = randint(1, 3)

        if critical == 1:
            self.quester.battlefield.current_enemy.health = 0
            print("{0} used Critical Hit and succesfully assassinated {1}.".format(self.name, self.quester.battlefield.current_enemy.name))
            if not self.quester.in_dungeon:
                self.quester.battlefield.current_enemy.die(self)
            if self.quester.in_dungeon:
                self.quester.battlefield.current_enemy.die(self)
        else:
            print("{0} used Critical Hit but failed to assassinate {1}.".format(self.name, self.quester.battlefield.current_enemy.name))

    def shout(self):
        self.damage_affector += round(self.strength / 5)
        if not self.quester.in_dungeon:
            self.quester.battlefield.current_enemy.damage_affector -= round(self.quester.battlefield.current_enemy.strength / 10)
        if self.quester.in_dungeon:
            self.quester.dungeon.battlefield.current_enemy.damage_affector -= round(self.quester.dungeon.battlefield.current_enemy.strength / 10)
        print("{0} used Shout, which increased {0}'s damage by 20% and decreased {1}'s damage by 10%.".format(self.name, self.quester.battlefield.current_enemy.name)) 

    def force_field(self):
        if not self.quester.in_dungeon:
            self.defense_affector += round(self.quester.battlefield.current_enemy.strength / 5) 
        if self.quester.in_dungeon:
            self.defense_affector += round(self.quester.dungeon.battlefield.current_enemy.strength / 5) 
        self.health += round(self.max_health / 5)
        print("{0} used Force Field, which increased {0}'s defense by 20% and restored 20% of {0}'s health.".format(self.name))

    def battle_valour(self):
        if not self.quester.in_dungeon:
            self.defense_affector += round(self.quester.battlefield.current_enemy.strength / 5)
        if self.quester.in_dungeon:
            self.defense_affector += round(self.quester.dungeon.battlefield.current_enemy.strength / 5)
        self.damage_affector += round(self.strength / 10)
        print("{0} used Battle Valour, which increased {0}'s defense by 20% and damage by 10%.".format(self.name))

    def set_unbeatable(self):
        print("Enter the dev password:")
        password = input(">>>")
        if password != "nuffun":
            print("Incorrect password!")
            return None
        self.max_health   = 999999
        self.health       = 999999
        self.strength     = 999999
        self.max_mana     = 999999
        self.mana         = 999999
        self.mana_growth  = 999999
        self.gold         = 999999
        self.loot         = 999999
        self.food         = 999999999999999999999999999

    def print_status(self):
        print("\n================================================================================")
        print("Health : {0}/{1} ({2}%)         Mana growth : {3}".format(self.health, self.max_health, round((self.health / self.max_health) * 100, 2), self.mana_growth))
        print("Strength : {0}                   Food : {1}".format(self.strength, self.food))
        print("Gold : {0}                        Enemies defeated : {1}".format(self.gold, self.enemies_defeated))
        print("Loot : {0}                        Bosses defeated : {1}".format(self.loot, self.bosses_defeated))
        print("Mana : {0}/{1} ({2}%)           Visited cities : {3}".format(self.mana, self.max_mana, round((self.mana / self.max_mana) * 100, 2), ", ".join(self.visited_cities)))
        print("================================================================================\n")
        if self.quester.companion != None:
           self.print_companion_status(self.quester.companion)

    def print_companion_status(self, companion):
        print("--------------------------------------------------------------------------------")
        print("Companion : {0} the {1} {2}".format(companion.name, companion.species, companion.character_class))
        print("Health : {0}/{1} ({2}%)         Strength : {3}".format(companion.health, companion.max_health, round((companion.health / companion.max_health) * 100, 2), companion.strength))
        print("Turns remaining : {0}              Enemies defeated : {1}".format(companion.lifetime, companion.enemies_defeated))
        print("--------------------------------------------------------------------------------\n")
