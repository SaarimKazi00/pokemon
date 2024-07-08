import random

# Base classes
class Pokémon:
    def __init__(self, name, type, health, attack, defence, special_attack, special_defence, speed, level, experience, moves, is_wild):
        self.name = name
        self.type = type
        self.health = health
        self.attack = attack
        self.defence = defence
        self.special_attack = special_attack
        self.special_defence = special_defence
        self.speed = speed
        self.level = level
        self.experience = experience
        self.moves = moves
        self.is_wild = is_wild

    def perform_attack(self, move, opponent):
        # Calculate damage based on types and stats
        if move.category == "Physical":
            damage = (self.attack * move.power) / opponent.defence
        else:  # Special move
            damage = (self.special_attack * move.power) / opponent.special_defence
        
        damage = max(1, int(damage))  # Ensure at least 1 damage is dealt
        opponent.take_damage(damage)
        print(f"{self.name} used {move.name} and dealt {damage} damage!")

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has fainted!")

    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health += 10
        self.attack += 5
        self.defence += 5
        print(f"{self.name} has leveled up to level {self.level}!")

    def learn_move(self, move):
        self.moves.append(move)

    def get_stat(self, stat):
        return getattr(self, stat)

class Move:
    def __init__(self, name, type, power, accuracy, category, effect=None):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.category = category
        self.effect = effect

    def apply_effect(self, target):
        if self.effect:
            self.effect(target)

class Trainer:
    def __init__(self, name, team, inventory):
        self.name = name
        self.team = team
        self.inventory = inventory

    def catch_pokemon(self, wild_pokemon):
        pokeball = next((item for item in self.inventory if isinstance(item, Pokeball)), None)
        if pokeball and pokeball.catch_rate > random.random():
            self.team.append(wild_pokemon)
            print(f"You caught {wild_pokemon.name}!")
        else:
            print("The Pokémon broke free!")

    def use_item(self, item, target):
        item.use(target)

    def battle(self, opponent):
        while self.team and opponent.team:
            print(f"{self.name}'s turn!")
            pokemon = self.choose_pokemon()
            move = self.choose_move(pokemon)
            opponent_pokemon = opponent.choose_pokemon()
            pokemon.perform_attack(move, opponent_pokemon)
            if opponent_pokemon.health <= 0:
                opponent.team.remove(opponent_pokemon)
                print(f"{opponent_pokemon.name} has fainted!")
            else:
                print(f"{opponent_pokemon.name} has {opponent_pokemon.health} HP left!")
            
            # Opponent's turn
            if opponent.team:
                print(f"{opponent.name}'s turn!")
                opponent_pokemon = opponent.choose_pokemon()
                move = opponent.choose_move(opponent_pokemon)
                pokemon = self.choose_pokemon()
                opponent_pokemon.perform_attack(move, pokemon)
                if pokemon.health <= 0:
                    self.team.remove(pokemon)
                    print(f"{pokemon.name} has fainted!")
                else:
                    print(f"{pokemon.name} has {pokemon.health} HP left!")

    def choose_pokemon(self):
        print("Choose a Pokémon:")
        for i, pokemon in enumerate(self.team):
            print(f"{i+1}. {pokemon.name} (HP: {pokemon.health})")
        choice = int(input("Enter the number of the Pokémon: ")) - 1
        return self.team[choice]

    def choose_move(self, pokemon):
        print("Choose a move:")
        for i, move in enumerate(pokemon.moves):
            print(f"{i+1}. {move.name} (Power: {move.power}, Accuracy: {move.accuracy})")
        choice = int(input("Enter the number of the move: ")) - 1
        return pokemon.moves[choice]

class Item:
    def __init__(self, name, type, effect):
        self.name = name
        self.type = type
        self.effect =effect

    def use(self, target):
        self.effect(target)

class Pokeball:
    def __init__(self, name, catch_rate):
        self.name = name
        self.catch_rate = catch_rate

# Subclasses
class FirePokémon(Pokémon):
    def __init__(self, name, health, attack, defence, special_attack, special_defence, speed, level, experience, moves, is_wild):
        super().__init__(name, "Fire", health, attack, defence, special_attack, special_defence, speed, level, experience, moves, is_wild)

class WaterPokémon(Pokémon):
    def __init__(self, name, health, attack, defence, special_attack, special_defence, speed, level, experience, moves, is_wild):
        super().__init__(name, "Water", health, attack, defence, special_attack, special_defence, speed, level, experience, moves, is_wild)

class PhysicalMove(Move):
    def __init__(self, name, type, power, accuracy, effect=None):
        super().__init__(name, type, power, accuracy, "Physical", effect)

class SpecialMove(Move):
    def __init__(self, name, type, power, accuracy, effect=None):
        super().__init__(name, type, power, accuracy, "Special", effect)

# Example usage
flareon = FirePokémon("Flareon", 45, 60, 40, 65, 45, 60, 1, 0, [], False)
vaporeon = WaterPokémon("Vaporeon", 45, 40, 60, 45, 65, 40, 1, 0, [], False)

# Example moves
fire_punch = PhysicalMove("Fire Punch", "Fire", 75, 100, lambda target: target.take_damage(10))
water_gun = SpecialMove("Water Gun", "Water", 40, 100)

flareon.learn_move(fire_punch)
vaporeon.learn_move(water_gun)

# Example items
pokeball = Pokeball("Pokeball", 0.5)

# Example trainers
trainer1 = Trainer("Ash", [flareon], [pokeball])
trainer2 = Trainer("Misty", [vaporeon], [pokeball])

# Example battle
trainer1.battle(trainer2)
