"""Game Functions Module.

This module contains various functions for a game, such as purchasing items,
generating random monsters, printing welcome messages, and displaying shop 
menus. It is designed to be imported and used in other Python files.

Functions:
    - purchase_item: Calculates the number of items that can be purchased.
    - new_random_monster: Generates random monster properties.
    - print_welcome: Prints a welcome message for a player.
    - print_shop_menu: Displays shop menu with item prices.

Typical usage example:
    import gamefunctions
    gamefunctions.print_welcome("Player")
"""

import random

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1) -> tuple:
    """
    This function calculates the number of items that can be purchased with the given amount of money.
    
    Parameters:
    itemPrice (float): The price of a single item.
    startingMoney (float): The initial amount of money.
    quantityToPurchase (int, optional): The number of items to purchase. Defaults to 1.
    
    Returns:
    tuple: A tuple containing the number of items purchased and the remaining amount of money.
    Example:
        >>> purchase_item(10.0, 50.0, 2)
        (2, 30.0)
    """
    max_items = int(startingMoney / itemPrice)
    if max_items >= quantityToPurchase:
        return quantityToPurchase, round(startingMoney - quantityToPurchase * itemPrice, 2)
    else:
        return max_items, round(startingMoney - max_items * itemPrice, 2)

def new_random_monster() -> dict:
    """
    This function generates a random monster with various properties.
    
    Returns:
    dict: A dictionary containing the monster's name, description, health, power, and money.
    """
    names = ["Goblin", "Orc", "Troll"]
    name = random.choice(names)
    if name == "Goblin":
        health = round(random.uniform(10, 20), 2)
        power = round(random.uniform(5, 10), 2)
        money = round(random.uniform(10, 20), 2)
    elif name == "Orc":
        health = round(random.uniform(20, 30), 2)
        power = round(random.uniform(10, 15), 2)
        money = round(random.uniform(20, 30), 2)
    else:
        health = round(random.uniform(30, 40), 2)
        power = round(random.uniform(15, 20), 2)
        money = round(random.uniform(30, 40), 2)
    return {
        "name": name,
        "description": f"A {name} with {health} health and {power} power.",
        "health": health,
        "power": power,
        "money": money
    }

def print_welcome(name: str, width: int = 20) -> None:
    """
    This function prints a welcome message for the given name.
    
    Parameters:
    name (str): The name to welcome.
    width (int): The width of the welcome message. Defaults to 20.
    """
    welcome_message = f"Hello, {name}!"
    padding = " " * ((width - len(welcome_message)) // 2)
    print(padding + welcome_message + padding)

def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float) -> None:
    """
    This function prints a shop menu with two items and their prices.
    
    Parameters:
    item1Name (str): The name of the first item.
    item1Price (float): The price of the first item.
    item2Name (str): The name of the second item.
    item2Price (float): The price of the second item.
    """
    print("/----------------------\\")
    print(f"| {item1Name:<12} ${item1Price:7.2f} |")
    print(f"| {item2Name:<12} ${item2Price:7.2f} |")
    print("\\----------------------/")
	

def main():
    """Test the functions in this module."""
    print("Testing purchase_item:")
    print(purchase_item(10.0, 100.0, 5))
    print(purchase_item(5.0, 20.0, 3))

    print("\nTesting new_random_monster:")
    for _ in range(3):
        print(new_random_monster())

    print("\nTesting print_welcome:")
    print_welcome("PATHOU")

    print("\nTesting print_shop_menu:")
    print_shop_menu("Sword", 15.0, "Shield", 10.0)

if __name__ == "__main__":
    # Test the functions
    print("Testing purchase_item function:")
    print(purchase_item(10.0, 100.0, 5))
    print(purchase_item(5.0, 20.0, 3))
    print(purchase_item(20.0, 50.0, 2))
    print("\nTesting new_random_monster function:")
    for _ in range(3):
        monster = new_random_monster()
        print(monster)

    print("\nTesting print_welcome function:")
    print_welcome("Jeff")
    print_welcome("Audrey")

    print("\nTesting print_shop_menu function:")
    print_shop_menu("Apple", 31.0, "Pear", 1.234)
    print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)

    # Create a test_functions() function for testing purposes and call it conditionally based on the __name__ variable.
    main()


