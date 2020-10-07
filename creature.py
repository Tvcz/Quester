from random import randint

attack_bonus = {"Archer":"Mage", "Mage":"Assassin", "Assassin":"Berserker", "Warrior":"Archer", "Berserker":"Warrior", "Boss":"Boss"}
defense_bonus = {"Archer":"Assassin", "Mage":"Berserker", "Assassin":"Warrior", "Warrior":"Mage", "Berserker":"Archer", "Boss":"Boss"}


class Creature:
    def __init__(self):
      self.damage_affector = 0
      self.defense_affector = 0

    def attack(self, enemy):
        bonus = 0
        if attack_bonus[self.character_class] == enemy.character_class:
            bonus = randint(self.strength // 4, self.strength // 2)
        damage = int(self.strength - enemy.defend(self) + randint(-3, 3) + bonus + self.damage_affector)
        if damage <= 0:
            damage = randint(2, 5)
        enemy.health -= damage
        if enemy.health < 0:
            enemy.health = 0
        print("{0} attacked {1} for {2} damage.\n{1} has {3} health remaining.".format(self.name, enemy.name, damage, enemy.health))
        if enemy.health == 0:
            enemy.die(self)

    def defend(self, enemy):
        defense = self.defense_affector
        if defense_bonus[self.character_class] == enemy.character_class:
            defense += randint(enemy.strength // 4, enemy.strength // 2)
        return defense
