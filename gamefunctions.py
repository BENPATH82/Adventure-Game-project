import random

def print_welcome(player_name):
    """Displays the welcome message and the player's name.

    Args:
        player_name (str): The name of the player.
    """
    print(f"Welcome, {player_name}!")


def new_random_monster():
    """Generates and returns a random monster with attributes.

    Returns:
        dict: A dictionary representing a monster, containing its name, hp, attack power, and description.
    """
    monsters = [
        {"name": "Goblin", "hp": 20, "attack": 5, "description": "A small, green goblin with sharp teeth."},
        {"name": "Orc", "hp": 30, "attack": 8, "description": "A large, muscular orc wielding a crude axe."},
        {"name": "Spider", "hp": 15, "attack": 7, "description": "A giant spider with venomous fangs."},
    ]
    return random.choice(monsters)


def print_shop_menu(item1_name, item1_price, item2_name, item2_price):
    """Prints a menu of items available in the shop along with their prices.

    Args:
        item1_name (str): Name of the first item.
        item1_price (int): Price of the first item.
        item2_name (str): Name of the second item.
        item2_price (int): Price of the second item.
    """
    print(f"1) {item1_name}: ${item1_price}")
    print(f"2) {item2_name}: ${item2_price}")


def purchase_item(item_price, money, quantity):
    """Handles the purchase of items and calculates the remaining money.

    Args:
        item_price (int): Price of a single item.
        money (int): The amount of money the player has.
        quantity (int): The number of items the player wants to buy.

    Returns:
        tuple: The number of items purchased and the remaining money.
    """
    total_cost = item_price * quantity
    if money >= total_cost:
        remaining_money = money - total_cost
        return quantity, remaining_money
    else:
        print("Not enough money!")
        return 0, money


def display_fight_statistics(player_hp, monster_hp, monster_name):
    """Displays the current health points (HP) of the player and the monster.

    Args:
        player_hp (int): The health points of the player.
        monster_hp (int): The health points of the monster.
        monster_name (str): The name of the monster.
    """
    print(f"\nYour HP: {player_hp}, {monster_name} HP: {monster_hp}")


def get_user_fight_options():
    print("1) Attack")
    print("2) Run Away")
    choice = input("Enter your choice: ")
    return choice


def handle_player_attack(player_attack, monster_hp):
    """Calculates and applies damage dealt by the player to the monster.

    Args:
        player_attack (int): The attack power of the player.
        monster_hp (int): The health points of the monster.

    Returns:
        int: The monster's remaining health points.
    """
    damage = random.randint(player_attack - 2, player_attack + 2)
    monster_hp -= damage
    print(f"You dealt {damage} damage!")
    return monster_hp


def handle_monster_attack(monster_attack, player_hp):
    """Calculates and applies damage dealt by the monster to the player.

    Args:
        monster_attack (int): The attack power of the monster.
        player_hp (int): The health points of the player.

    Returns:
        int: The player's remaining health points.
    """
    damage = random.randint(monster_attack - 2, monster_attack + 2)
    player_hp -= damage
    print(f"The monster dealt {damage} damage!")
    return player_hp


def sleep(player_hp, gold):
    """Restores the player's health points (HP) by sleeping if enough gold is available.

    Args:
        player_hp (int): The health points of the player before sleeping.
        gold (int): The amount of gold the player has.

    Returns:
        tuple: The player's health points after sleeping and the remaining gold.
    """
    if gold >= 5:
        player_hp = 30
        gold -= 5
        print("You feel rested and your HP is fully restored.")
    else:
        print("You don't have enough gold to sleep.")
    return player_hp, gold


def handle_fight(player_hp, player_gold):
    """
    Handles the combat logic between the player and a monster.

    Args:
        player_hp (int): The player's current hit points.
        player_gold (int): The player's current gold.

    Returns:
        tuple: The player's updated hit points and gold.
    """
    print("\nA wild monster appears!")
    monster = new_random_monster()
    monster_hp = monster["hp"]
    print(f"You encountered: {monster['description']}")

    while player_hp > 0 and monster_hp > 0:
        display_fight_statistics(player_hp, monster_hp, monster["name"])
        fight_choice = get_user_fight_options()

        if fight_choice == '1':
            monster_hp = handle_player_attack(10, monster_hp)  # player attack value is 10
            if monster_hp > 0:
                player_hp = handle_monster_attack(monster["attack"], player_hp)
        elif fight_choice == '2':
            print("You ran away!")
            return player_hp, player_gold
        else:
            print("Invalid choice. Try again.")

    if player_hp <= 0:
        print("You were defeated!")
        return 30, player_gold // 2  # player respawns with half gold
    else:
        print(f"You defeated the {monster['name']}!")
        player_gold += 20  # reward for winning
        return player_hp, player_gold
