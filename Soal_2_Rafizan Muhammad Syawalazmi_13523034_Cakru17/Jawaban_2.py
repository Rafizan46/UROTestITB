import random
import copy

class Action:
    PassAction = 0
    Attack = 1
    ShootPrimary = 2
    ShootSecondary = 3
    Defend = 4


class Weapon:
    def __init__(self, name, damage, ammo):
        self.name = name
        self.damage = damage
        self.ammo = ammo


class Robot:
    def __init__(self, name, max_health, damage, primary_weapon, secondary_weapon):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.defended = False
        self.primary_weapon = primary_weapon
        self.secondary_weapon = secondary_weapon

    def do_action(self, action, target, announce):
        if action == Action.PassAction:
            if announce:
                print(f"{self.name} passed their turn!")
        elif action == Action.Attack:
            self.attack(target, announce)
        elif action == Action.ShootPrimary:
            self.shoot(self.primary_weapon, target, announce)
        elif action == Action.ShootSecondary:
            self.shoot(self.secondary_weapon, target, announce)
        elif action == Action.Defend:
            self.defend(announce)

    def printHealth(self):
        print(f"{self.name}'s HP = {self.health}/{self.max_health}")

    def attack(self, target, announce):
        if announce:
            print(f"{self.name} attacked {target.name} using their fists!")
        target.damaged(self.damage, announce)

    def shoot(self, using_weapon, target, announce):
        if using_weapon.ammo > 0:
            if announce:
                print(f"{self.name} attacked {target.name} using {using_weapon.name}!")
            target.damaged(using_weapon.damage, announce)
            using_weapon.ammo -= 1
        else:
            if announce:
                print(f"{self.name} tried using {using_weapon.name} but it has no ammo!")

    def defend(self, announce):
        if announce:
            print(f"{self.name} defended!")
        self.defended = True

    def damaged(self, damage, announce):
        if self.defended:
            damage /= 2
            self.defended = False
            if announce:
                print(f"The Attack is not effective!")
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if announce:
            print(f"{self.name} got hit by {damage:.2f} damage!")

    def is_alive(self):
        return self.health > 0


class Battle:
    def __init__(self, robot1, robot2):
        self.robots = [robot1, robot2]

    def start_fight(self):
        is_first = True
        while self.robots[0].is_alive() and self.robots[1].is_alive():
            action = self.minimax(self.robots, 10, float('-inf'), float('inf'), is_first)[0]
            self.robots[0 if is_first else 1].do_action(action, self.robots[1 if is_first else 0], True)
            self.robots[0].printHealth()
            self.robots[1].printHealth()
            print(f"\n\n")
            is_first = not is_first
        if (self.robots[0].is_alive()):
            print(f"{self.robots[0].name} won!!!")
        else:
            print(f"{self.robots[1].name} won!!!")

    def minimax(self, robots, depth, alpha, beta, is_first):
        if depth == 0 or not robots[0].is_alive() or not robots[1].is_alive():
            return Action.PassAction, robots[0].health - robots[1].health

        if is_first:
            max_value = float('-inf')
            best_action = Action.PassAction
            for action in [Action.PassAction, Action.Attack, Action.ShootPrimary, Action.ShootSecondary, Action.Defend]:
                new_robots = copy.deepcopy(robots)
                new_robots[0].do_action(action, new_robots[1], False)
                new_value = self.minimax(new_robots, depth - 1, alpha, beta, not is_first)[1]
                if new_value > max_value:
                    best_action = action
                    max_value = new_value
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break
            return best_action, max_value
        else:
            min_value = float('inf')
            best_action = Action.PassAction
            for action in [Action.PassAction, Action.Attack, Action.ShootPrimary, Action.ShootSecondary, Action.Defend]:
                new_robots = copy.deepcopy(robots)
                new_robots[1].do_action(action, new_robots[0], False)
                new_value = self.minimax(new_robots, depth - 1, alpha, beta, not is_first)[1]
                if new_value < min_value:
                    best_action = action
                    min_value = new_value
                beta = min(beta, min_value)
                if beta <= alpha:
                    break
            return best_action, min_value


class Game:
    def __init__(self, robots, weapons):
        self.battle = None
        self.robots = robots
        self.weapons = weapons

    def add_robot(self):
        name = input("Type the robot's name: ")
        max_health = float(input("Type the robot's max health: "))
        damage = float(input("Type the robot's melee damage: "))
        print("Choose the robot's weapon:")
        for i in range(len(self.weapons)):
            print(f"{i+1}. {self.weapons[i].name}")
        while True:
            primary = int(input("Select the robot's primary: "))
            if (0 < primary <= len(self.weapons)):
                break
            print("Invalid input, please try again")
        while True:
            secondary = int(input("Select the robot's secondary: "))
            if (0 < secondary <= len(self.weapons)):
                break
            print("Invalid input, please try again")
        self.robots.append(Robot(name, max_health, damage, self.weapons[primary-1], self.weapons[secondary-1]))
        

    def add_weapon(self):
        name = input("Type the weapon's name: ")
        damage = float(input("Type the weapon's damage: "))
        ammo = int(input("Type the weapon's ammo cap: "))
        self.weapons.append(Weapon(name, damage, ammo))

    def start_game(self):
        print("Choose robots for the battle:")
        for i in range(len(self.robots)):
            print(f"{i+1}. {self.robots[i].name}")
        while True:
            first = int(input("Select the first robot: "))
            if (0 < first <= len(self.robots)):
                break
            print("Invalid input, please try again")
        while True:
            second = int(input("Select the second robot: "))
            if (0 < second <= len(self.robots) and first != second):
                break
            print("Invalid input, please try again")

        self.battle = Battle(self.robots[first-1], self.robots[second-1])
        self.battle.start_fight()


if __name__ == "__main__":
    weapon_pack = [Weapon("None", -1, 0), Weapon("AK47", 20, 3), Weapon("RPG", 40, 1), Weapon("Sniper", 70, 1)]

    robot_pack = [Robot("RobotMelee", 100, 10, weapon_pack[0], weapon_pack[0]), Robot("RobotSoldier", 80, 5, weapon_pack[1], weapon_pack[2]), Robot("RobotSniper", 60, 5, weapon_pack[3], weapon_pack[0])]

    game = Game(robot_pack, weapon_pack)
    while True:
        print("Welcome to Battle of robots!")
        print("Choose your option: ")
        print("1. Start Game")
        print("2. Add Robots")
        print("3. Add Weapons")
        ans = int(input("Select your option: "))
        if ans == 1:
            game.start_game()
        elif ans == 2:
            game.add_robot()
        elif ans == 3:
            game.add_weapon()
