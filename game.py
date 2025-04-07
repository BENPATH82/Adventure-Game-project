import gamefunctions
import json
import os

SAVE_FILE = "game_save.json"

def save_game(player_hp, player_gold, player_inventory, equipped_weapon):
    """Saves the game state to a JSON file."""
    save_data = {
        "player_hp": player_hp,
        "player_gold": player_gold,
        "player_inventory": player_inventory,
        "equipped_weapon": equipped_weapon,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(save_data, f)
    print("Game saved.")

def load_game():
    """Loads the game state from a JSON file."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            save_data = json.load(f)
        print("Game loaded.")
        return (
            save_data["player_hp"],
            save_data["player_gold"],
            save_data["player_inventory"],
            save_data["equipped_weapon"],
        )
    else:
        print("No saved game found.")
        return None

def main():
    print("1) New Game")
    print("2) Load Game")
    choice = input("Enter your choice: ")

    if choice == '1':
        player_name = input("Welcome to the game! What's your name? ")
        gamefunctions.print_welcome(player_name)
        player_hp = 30
        player_gold = 10
        player_inventory = []
        equipped_weapon = None
    elif choice == '2':
        loaded_game = load_game()
        if loaded_game:
            player_hp, player_gold, player_inventory, equipped_weapon = loaded_game
            player_name = "Loaded Player" # place holder, we did not save player name.
        else:
            return #Exit if no game to load.
    else:
        print("Invalid choice.")
        return

    shop_items = [
        {"name": "Sword", "type": "weapon", "maxDurability": 40, "currentDurability": 40, "price": 25},
        {"name": "Spiderbane", "type": "misc", "use_on": "Spider", "price": 30},
    ]

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold}")
        print("What would you like to do?")
        print(" 1) Leave town (Fight Monster)")
        print(" 2) Sleep (Restore HP for 5 Gold)")
        print(" 3) Visit Shop")
        print(" 4) Equip Item")
        print(" 5) Save and Quit")
        print(" 6) Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            player_hp, player_gold, player_inventory, equipped_weapon = gamefunctions.handle_fight(player_hp, player_gold, player_inventory, equipped_weapon)
        elif choice == '2':
            player_hp, player_gold = gamefunctions.sleep(player_hp, player_gold)
        elif choice == '3':
            gamefunctions.print_shop_menu(shop_items)
            item_choice = int(input("Enter item number to buy (0 to cancel): "))
            if 0 < item_choice <= len(shop_items):
                quantity = int(input("Enter quantity: "))
                gamefunctions.purchase_item(shop_items[item_choice - 1], player_gold, quantity, player_inventory)
        elif choice == '4':
            equipped_weapon = gamefunctions.equip_item(player_inventory)
        elif choice == '5':
            save_game(player_hp, player_gold, player_inventory, equipped_weapon)
            break
        elif choice == '6':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
