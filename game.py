import gamefunctions

def main():
    player_name = input("Welcome to the game! What's your name? ")
    gamefunctions.print_welcome(player_name)

    print("\nA wild monster appears!")
    monster = gamefunctions.new_random_monster()
    print(f"You encountered: {monster['description']}")

    print("\nShop Menu:")
    gamefunctions.print_shop_menu("Health Potion", 10.0, "Mana Potion", 12.0)

    money = 50.0
    print(f"\nYou have ${money}.")
    choice = int(input("Enter 1 to buy Health Potion, or 2 to buy Mana Potion: "))
    if choice == 1:
        items_purchased, remaining_money = gamefunctions.purchase_item(10.0, money, 1)
    else:
        items_purchased, remaining_money = gamefunctions.purchase_item(12.0, money, 1)

    print(f"You bought {items_purchased} item(s). Remaining money: ${remaining_money}.")


if __name__ == '__main__':
    main()
