import gamefunctions # Assuming this file exists and has necessary functions
import json
import os
import pygame # Import pygame
import sys    # To handle abrupt exit on window close

SAVE_FILE = "game_save.json"

# --- Pygame Map Constants ---
GRID_SIZE = 10
CELL_SIZE = 32
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Player color
BLACK = (0, 0, 0)   # Grid color

# --- Map Feature Positions ---
# Grid coordinates (col, row), starting from (0, 0) top-left
TOWN_POS = (0, 0)
MONSTER_POS = (5, 5) # Example position

# --- Save/Load Game --- (Modified to include map position)
def save_game(player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos):
    """Saves the game state, including map position, to a JSON file."""
    save_data = {
        "player_hp": player_hp,
        "player_gold": player_gold,
        "player_inventory": player_inventory,
        "equipped_weapon": equipped_weapon,
        "player_map_pos": player_map_pos, # Save map position
    }
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(save_data, f, indent=4) # Added indent for readability
        print("Game saved.")
    except IOError as e:
        print(f"Error saving game: {e}")

def load_game():
    """Loads the game state, including map position, from a JSON file."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                save_data = json.load(f)
            print("Game loaded.")
            # Ensure map position exists in save, provide default if not (for older saves)
            player_map_pos = save_data.get("player_map_pos", list(TOWN_POS))
            # Ensure all expected keys are present
            return (
                save_data.get("player_hp", 30),
                save_data.get("player_gold", 10),
                save_data.get("player_inventory", []),
                save_data.get("equipped_weapon", None),
                list(player_map_pos), # Return as list for mutability
            )
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading saved game: {e}. Starting new game.")
            return None
        except KeyError as e:
             print(f"Saved game file is missing data: {e}. Starting new game.")
             return None
    else:
        print("No saved game found.")
        return None

# --- Map Exploration Function ---
def explore_map(player_hp, player_gold, player_inventory, equipped_weapon, current_player_map_pos):
    """
    Handles the graphical map exploration using Pygame.

    Args:
        player_hp, player_gold, player_inventory, equipped_weapon: Current player state.
        current_player_map_pos: Player's starting [col, row] on the map for this session.

    Returns:
        tuple: (outcome, updated_hp, updated_gold, updated_inv, updated_weapon, updated_map_pos)
               outcome can be 'town', 'game_over', 'quit'.
    """
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("World Map")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 24) # Font for potential text rendering later
    except Exception as e:
        print(f"Error initializing Pygame: {e}")
        # Return gracefully, indicating failure to start map? Or let it raise?
        # For now, assume it worked or the calling code handles it.
        # Let's return 'town' to go back safely.
        return 'town', player_hp, player_gold, player_inventory, equipped_weapon, current_player_map_pos


    player_pos = list(current_player_map_pos) # Use a mutable list for position
    initial_pos = tuple(current_player_map_pos) # Remember where we started this map session

    running = True
    map_outcome = 'map_running' # Tracks the reason for exiting the map loop

    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # Signal abrupt quit - main loop should check for this and sys.exit()
                return 'quit', player_hp, player_gold, player_inventory, equipped_weapon, player_pos

            # Respond only to keydown to prevent rapid movement from holding key
            if event.type == pygame.KEYDOWN:
                next_pos = list(player_pos) # Start with current position

                if event.key == pygame.K_UP:
                    next_pos[1] -= 1 # Decrease row (move up)
                elif event.key == pygame.K_DOWN:
                    next_pos[1] += 1 # Increase row (move down)
                elif event.key == pygame.K_LEFT:
                    next_pos[0] -= 1 # Decrease col (move left)
                elif event.key == pygame.K_RIGHT:
                    next_pos[0] += 1 # Increase col (move right)
                else:
                    continue # Ignore other key presses

                # --- Boundary Check ---
                if 0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE:
                    # --- Valid Move: Update Player Position ---
                    player_pos = next_pos
                    current_pos_tuple = tuple(player_pos) # Use tuple for comparisons

                    # --- Check for Special Squares AFTER Moving ---

                    # 1. Check for Town Return
                    # Must have moved away first during this map session
                    if current_pos_tuple == TOWN_POS and current_pos_tuple != initial_pos:
                        print("Returning to the safety of the town.")
                        map_outcome = 'town'
                        running = False # Exit map loop

                    # 2. Check for Monster Encounter
                    elif current_pos_tuple == MONSTER_POS:
                        print("\nYou stepped onto a dangerous square!")
                        # --- Trigger Fight ---
                        # We need the fight logic from gamefunctions
                        try:
                            # Assuming handle_fight takes current stats and returns
                            # the updated stats and a fight status string ('won', 'fled', 'died')
                            (player_hp, player_gold, player_inventory, equipped_weapon, fight_status
                             ) = gamefunctions.handle_fight(
                                player_hp, player_gold, player_inventory, equipped_weapon
                             )

                            if fight_status == 'died':
                                map_outcome = 'game_over'
                                running = False # Exit map loop
                            else: # Player won or fled
                                print("The immediate danger has passed. You remain on the map.")
                                # Player stays at MONSTER_POS, map loop continues.
                                # No change needed here, the drawing part below will handle showing player
                                # We might want to remove the monster visually after defeat? Future task.
                                # For now, re-entering the square will trigger another fight.

                        except AttributeError:
                            print("Error: 'handle_fight' function not found in gamefunctions.")
                            print("Retreating to town due to error.")
                            map_outcome = 'town' # Go back to town if fight cannot occur
                            running = False
                        except Exception as e:
                            print(f"An error occurred during the fight: {e}")
                            print("Retreating to town due to error.")
                            map_outcome = 'town' # Go back to town
                            running = False

        # --- Drawing --- (Happens every frame)
        screen.fill(WHITE) # Clear screen with white background

        # Draw Grid Lines (Optional, but helpful for visualization)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

        # Draw Town Square (Green Circle)
        # Calculate pixel coordinates for the center of the town cell
        town_center_x = TOWN_POS[0] * CELL_SIZE + CELL_SIZE // 2
        town_center_y = TOWN_POS[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, GREEN, (town_center_x, town_center_y), CELL_SIZE // 2 - 4, 4) # Draw circle outline

        # Draw Monster Square (Red Circle)
        monster_center_x = MONSTER_POS[0] * CELL_SIZE + CELL_SIZE // 2
        monster_center_y = MONSTER_POS[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, RED, (monster_center_x, monster_center_y), CELL_SIZE // 2 - 4, 4) # Draw circle outline


        # Draw Player (Blue Square)
        player_rect = pygame.Rect(
            player_pos[0] * CELL_SIZE,  # Left edge (col * cell_size)
            player_pos[1] * CELL_SIZE,  # Top edge (row * cell_size)
            CELL_SIZE,                  # Width
            CELL_SIZE                   # Height
        )
        pygame.draw.rect(screen, BLUE, player_rect)

        pygame.display.flip() # Update the full screen to show drawings
        clock.tick(10) # Limit frames per second (controls game speed and CPU usage)

    # --- End of Map Loop ---
    pygame.quit() # Close the Pygame window
    # Return the outcome and the potentially updated player state and position
    return map_outcome, player_hp, player_gold, player_inventory, equipped_weapon, player_pos


# --- Main Game Logic ---
def main():
    # Initialize variables with default values
    player_name = "Player"
    player_hp = 30
    player_gold = 10
    player_inventory = []
    equipped_weapon = None
    player_map_pos = list(TOWN_POS) # Start at town by default

    print("--------------------")
    print(" Text Adventure RPG ")
    print("--------------------")
    print("1) New Game")
    print("2) Load Game")
    choice = input("Enter your choice: ")

    if choice == '1':
        player_name = input("Welcome to the game! What's your name? ")
        try:
            gamefunctions.print_welcome(player_name)
        except AttributeError:
            print(f"Welcome, {player_name}!") # Fallback

        # Set initial stats for a new game
        player_hp = 30
        player_gold = 10
        player_inventory = []
        equipped_weapon = None
        player_map_pos = list(TOWN_POS) # Start at town square
        print("New game started.")

    elif choice == '2':
        loaded_data = load_game()
        if loaded_data:
            # Unpack loaded data including player_map_pos
            player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos = loaded_data
            player_name = "Loaded Player" # Consider saving/loading player name too
            print(f"Welcome back, {player_name}!")
            print(f"Loaded state - HP: {player_hp}, Gold: {player_gold}, Map Pos: {player_map_pos}")
        else:
            print("Failed to load game. Exiting.")
            return # Exit if no game could be loaded
    else:
        print("Invalid choice. Exiting.")
        return

    # Define shop_items (Consider moving this to gamefunctions or a data file)
    shop_items = [
        {"name": "Sword", "type": "weapon", "maxDurability": 40, "currentDurability": 40, "price": 25, "damage": 5}, # Added damage
        {"name": "Health Potion", "type": "potion", "heal_amount": 15, "price": 10}, # Added potion example
        {"name": "Spiderbane", "type": "misc", "use_on": "Spider", "price": 30},
    ]

    # --- Main Game Loop (Town Menu) ---
    game_running = True
    while game_running:
        print("\n--- Town Menu ---")
        print(f"Status - HP: {player_hp}, Gold: {player_gold}")
        if equipped_weapon:
             # Try to display durability and damage if available
             dura_str = f"{equipped_weapon.get('currentDurability', '?')}/{equipped_weapon.get('maxDurability', '?')}"
             dmg_str = equipped_weapon.get('damage', '?')
             print(f"Equipped: {equipped_weapon['name']} (Dura: {dura_str}, Dmg: {dmg_str})")
        else:
             print("Equipped: Nothing")
        print("-----------------")
        print("Actions:")
        print(" 1) Explore World Map") # Text updated
        print(" 2) Sleep (Restore HP for 5 Gold)")
        print(" 3) Visit Shop")
        print(" 4) Equip Item")
        print(" 5) Save and Quit")
        print(" 6) Quit Game (No Save)")

        action_choice = input("Enter your choice: ")

        if action_choice == '1':
            # --- Explore Map ---
            print("\nLeaving town to explore the map...")
            try:
                # Call the map function, passing the current game state
                (map_outcome, player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos
                 ) = explore_map(
                    player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos
                 )

                # Handle the outcome of the map exploration
                if map_outcome == 'quit':
                    print("\nGame window closed. Exiting application abruptly.")
                    sys.exit() # Exit immediately as requested

                elif map_outcome == 'game_over':
                    # Player died during a fight triggered from the map
                    print("\nYou have fallen...")
                    print("--- GAME OVER ---")
                    game_running = False # Exit the main loop

                elif map_outcome == 'town':
                    # Player returned to the town square on the map
                    print("You are back at the town entrance.")
                    # Loop continues naturally, showing town menu again
                    # player_map_pos is already updated to TOWN_POS by explore_map return

            except ImportError:
                 print("\nError: Pygame module not found. Please install it (`pip install pygame`).")
            except NameError as e:
                 print(f"\nError: Could not start map. Is 'gamefunctions' module available and correct? Missing: {e}")
            except Exception as e:
                 # Catch other potential errors during map exploration/pygame init
                 print(f"\nAn unexpected error occurred related to the map: {e}")
                 print("Returning to town.")
                 # Ensure player is back at town position if map crashes
                 player_map_pos = list(TOWN_POS)


        elif action_choice == '2': # Sleep
            try:
                player_hp, player_gold = gamefunctions.sleep(player_hp, player_gold)
            except AttributeError:
                print("Sleep function not implemented yet.")
            except Exception as e:
                print(f"Error during sleep: {e}")

        elif action_choice == '3': # Visit Shop
            try:
                # Assume these functions exist in gamefunctions
                gamefunctions.print_shop_menu(shop_items)
                item_choice_str = input("Enter item number to buy (0 to cancel): ")

                if item_choice_str.isdigit():
                    item_choice = int(item_choice_str)
                    if 0 < item_choice <= len(shop_items):
                        item_to_buy = shop_items[item_choice - 1]
                        quantity_str = input(f"Enter quantity for {item_to_buy['name']} (Price: {item_to_buy['price']} gold): ")
                        if quantity_str.isdigit():
                            quantity = int(quantity_str)
                            if quantity > 0:
                                # purchase_item should handle gold check, update inventory, and return new gold total
                                player_gold = gamefunctions.purchase_item(
                                    item_to_buy, player_gold, quantity, player_inventory
                                )
                            else:
                                print("Quantity must be positive.")
                        else:
                             print("Invalid quantity.")
                    elif item_choice == 0:
                        print("Cancelled purchase.")
                    else:
                        print("Invalid item number.")
                else:
                     print("Please enter a number.")

            except AttributeError:
                 print("Shop functions ('print_shop_menu', 'purchase_item') not implemented yet.")
            except Exception as e:
                 print(f"Error during shopping: {e}")

        elif action_choice == '4': # Equip Item
             try:
                 # equip_item likely takes inventory, maybe equipped item, and returns the newly equipped item (or None)
                 equipped_weapon = gamefunctions.equip_item(player_inventory, equipped_weapon) # Pass current weapon too?
                 if equipped_weapon:
                     print(f"Equipped {equipped_weapon['name']}.")
                 # equip_item function should handle message if nothing equipped or selection cancelled
             except AttributeError:
                 print("Equip function ('equip_item') not implemented yet.")
             except Exception as e:
                 print(f"Error equipping item: {e}")

        elif action_choice == '5': # Save and Quit
            # Save game state including map position
            save_game(player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos)
            print("See you next time!")
            game_running = False # Exit the main loop

        elif action_choice == '6': # Quit without Saving
            print("Quitting without saving. Goodbye!")
            game_running = False # Exit the main loop
        else:
            print("Invalid choice. Please try again.")

# --- Entry Point ---
if __name__ == '__main__':
    # Ensure gamefunctions module is accessible
    try:
        import gamefunctions
        main()
    except ModuleNotFoundError:
        print("="*40)
        print("ERROR: The required 'gamefunctions.py' file was not found.")
        print("Please make sure 'gamefunctions.py' is in the same")
        print("directory as 'game.py'.")
        print("="*40)
    except ImportError as e:
         print(f"ERROR: Failed to import 'gamefunctions': {e}")
    except Exception as e:
        # Catch any other unexpected errors during startup or main execution
        print(f"\nAn unexpected error occurred: {e}")
        # Clean up pygame if it was initialized and crashed
        if pygame.get_init():
            pygame.quit()
