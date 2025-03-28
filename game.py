import gamefunctions

def main():
    """
    Main function to run the game.

    Initializes player stats, presents the town menu, and handles game flow.
    """
    player_name = input("Welcome to the game! What's your name? ")
    gamefunctions.print_welcome(player_name)

    player_hp = 30
    player_gold = 10

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold}")
        print("What would you like to do?")
        print(" 1) Leave town (Fight Monster)")
        print(" 2) Sleep (Restore HP for 5 Gold)")
        print(" 3) Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            player_hp, player_gold = gamefunctions.handle_fight(player_hp, player_gold)
        elif choice == '2':
            player_hp, player_gold = gamefunctions.sleep(player_hp, player_gold)
        elif choice == '3':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
