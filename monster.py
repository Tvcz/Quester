from creature import Creature
from random import randint

character_classes = {"Archer":[25, 65], "Assassin":[65, 25], "Berserker":[40, 50], "Mage":[55, 35], "Warrior":[15, 75]}
class_list = ("Archer", "Assassin", "Berserker", "Mage", "Warrior")

monster_types = ("Skeleton", "Ogre", "Zombie", "Human", "Acolyte", "Aboleth", "Cloaker", "Golem", "Goblin", "Demon")
monster_names1 = ("Xe", "Va", "Cra", "Zi", "On", "Per", "Yi", "Be")
monster_names2 = ("men", "ta", "quo", "los", "bin", "kli", "vem", "con")
monster_names3 = ("ke", "me", "ta", "sha", "neo", "za", "rak", "ting", "-hai")

class Monster(Creature):

    def __init__(self, quester):

        self.quester = quester

        player_health_and_strength = self.quester.player.max_health + self.quester.player.strength

        self.damage_affector = 0
        self.defense_affector = 0
        
        self.name = monster_names1[randint(0, len(monster_names1) - 1)] + monster_names2[randint(0, len(monster_names2) - 1)] + monster_names3[randint(0, len(monster_names3) - 1)]
        self.character_class = class_list[randint(0, len(class_list) - 1)]
        self.health = round((player_health_and_strength) * (character_classes[self.character_class][1] / 100)) + randint(-3, 3)
        self.max_health = self.health
        self.strength = round((player_health_and_strength ) * (character_classes[self.character_class][0] / 100)) + randint(-3, 3)
        self.species = monster_types[randint(0, len(monster_types) - 1)]
        self.number = 1

    def die(self, enemy):
        loot_gain = int(((self.max_health * self.strength) // 200) + randint(-2, 5))
        if loot_gain <= 0:
            loot_gain = 1
        food_gain = randint(0, 3)
        mana_gain = randint(1, 5)
        self.quester.player.loot += loot_gain
        self.quester.player.food += food_gain
        self.quester.player.mana += mana_gain
        print("{0} killed {1} the {2} {3}. You gained {4} loot, {5} food, and {6} mana.".format(enemy.name, self.name, self.species, self.character_class, loot_gain, food_gain, mana_gain))
        
        if self.character_class == "Boss":
            self.quester.player.bosses_defeated += 1
        else:
            enemy.enemies_defeated += 1

        if not self.quester.in_dungeon:
            for monster in self.quester.battlefield.enemies:
                if monster.number > self.number:
                    monster.number -= 1
            self.quester.battlefield.enemies.remove(self)
        if self.quester.in_dungeon:
            for monster in self.quester.dungeon.battlefield.enemies:
                if monster.number > self.number:
                    monster.number -= 1
            self.quester.dungeon.battlefield.enemies.remove(self)
