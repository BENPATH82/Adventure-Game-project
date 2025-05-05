import gamefunctions
import json
import os
import pygame
import sys
import wanderingMonster

SAVE_FILE = "game_save.json"

# --- Main Game Logic ---
def main():
    # Initialize variables with default values
    player_name = "Player"
    player_hp = 30
    player_gold = 10
    player_inventory = []
    equipped_weapon = None
    player_map_pos = list(TOWN_POS)
    monsters = []  # Initialize empty monster list

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
            print(f"Welcome, {player_name}!")

        # Set initial stats for a new game
        player_hp = 30
        player_gold = 10
        player_inventory = []
        equipped_weapon = None
        player_map_pos = list(TOWN_POS)
        monsters = []  # Initialize empty monster list
        print("New game started.")

        # Spawn initial monsters for a new game
        monsters.append(wanderingMonster.WanderingMonster.new_random_monster(GRID_SIZE, TOWN_POS[0], TOWN_POS[1]))
        monsters.append(wanderingMonster.WanderingMonster.new_random_monster(GRID_SIZE, TOWN_POS[0], TOWN_POS[1]))

    elif choice == '2':
        loaded_data = load_game()
        if loaded_data:
            # Unpack loaded data including player_map_pos and monsters
            player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos, monsters = loaded_data
            player_name = "Loaded Player"
            print(f"Welcome back, {player_name}!")
            print(f"Loaded state - HP: {player_hp}, Gold: {player_gold}, Map Pos: {player_map_pos}")
        else:
            print("Failed to load game. Exiting.")
            return
    else:
        print("Invalid choice. Exiting.")
        return

    # Define shop_items
    shop_items = [
        {"name": "Sword", "type": "weapon", "maxDurability": 40, "currentDurability": 40, "price": 25, "damage": 5},
        {"name": "Health Potion", "type": "potion", "heal_amount": 15, "price": 10},
        {"name": "Spiderbane", "type": "misc", "use_on": "Spider", "price": 30},
    ]

    # --- Main Game Loop (Town Menu) ---
    game_running = True
    while game_running:
        print("\n--- Town Menu ---")
        print(f"Status - HP: {player_hp}, Gold: {player_gold}")
        if equipped_weapon:
            dura_str = f"{equipped_weapon.get('currentDurability', '?')}/{equipped_weapon.get('maxDurability', '?')}"
            dmg_str = equipped_weapon.get('damage', '?')
            print(f"Equipped: {equipped_weapon['name']} (Dura: {dura_str}, Dmg: {dmg_str})")
        else:
            print("Equipped: Nothing")
        print("-----------------")
        print("Actions:")
        print(" 1) Explore World Map")
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
                # Call the map function, passing the current game state and monsters
                (
                    map_outcome,
                    player_hp,
                    player_gold,
                    player_inventory,
                    equipped_weapon,
                    player_map_pos,
                    monsters,  # Get updated monster list back
                ) = explore_map(
                    player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos, monsters
                )

                # Handle the outcome of the map exploration
                if map_outcome == 'quit':
                    print("\nGame window closed. Exiting application abruptly.")
                    sys.exit()

                elif map_outcome == 'game_over':
                    # Player died during a fight triggered from the map
                    print("\nYou have fallen...")
                    print("--- GAME OVER ---")
                    game_running = False

                elif map_outcome == 'town':
                    # Player returned to the town square on the map
                    print("You are back at the town entrance.")
                    # If all monsters were defeated, spawn two new ones
                    if not monsters:
                        monsters.append(wanderingMonster.WanderingMonster.new_random_monster(GRID_SIZE, TOWN_POS[0], TOWN_POS[1]))
                        monsters.append(wanderingMonster.WanderingMonster.new_random_monster(GRID_SIZE, TOWN_POS[0], TOWN_POS[1]))


            except ImportError:
                print("\nError: Pygame module not found. Please install it (`pip install pygame`).")
            except NameError as e:
                print(
                    f"\nError: Could not start map. Is 'gamefunctions' module available and correct? Missing: {e}"
                )
            except Exception as e:
                # Catch other potential errors during map exploration/pygame init
                print(f"\nAn unexpected error occurred related to the map: {e}")
                print("Returning to town.")
                player_map_pos = list(TOWN_POS)
                # Ensure monsters are cleared if there was an error
                monsters = []

        elif action_choice == '2':  # Sleep
            try:
                player_hp, player_gold = gamefunctions.sleep(player_hp, player_gold)
            except AttributeError:
                print("\nError: Pygame module not found.")

# --- Pygame Map Constants ---
GRID_SIZE = 10
CELL_SIZE = 32
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# --- Map Feature Positions ---
TOWN_POS = (0, 0)


# --- NPC Data ---
npcs = [
    {"name": "Old Man", "pos": (1, 2), "dialogue": "Welcome to our humble town."},
    {"name": "Shopkeeper", "pos": (3, 4), "dialogue": "Come browse my wares!"},
]

# --- Save/Load Game ---
def save_game(player_hp, player_gold, player_inventory, equipped_weapon, player_map_pos, monsters):
    """Saves the game state, including map position and monster positions."""
    monster_data = [{"x": m.x, "y": m.y, "name": m.name, "gold": m.gold} for m in monsters]
    save_data = {
        "player_hp": player_hp,
        "player_gold": player_gold,
        "player_inventory": player_inventory,
        "equipped_weapon": equipped_weapon,
        "player_map_pos": player_map_pos,
        "monsters": monster_data,
    }
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(save_data, f, indent=4)
        print("Game saved.")
    except IOError as e:
        print(f"Error saving game: {e}")

def load_game():
    """Loads the game state, including map position and monster positions."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                save_data = json.load(f)
            print("Game loaded.")
            player_map_pos = save_data.get("player_map_pos", list(TOWN_POS))
            monster_data = save_data.get("monsters", [])
            monsters = [
                wanderingMonster.WanderingMonster(m["x"], m["y"], None, m["name"], m["gold"])
                for m in monster_data
            ]
            return (
                save_data.get("player_hp", 30),
                save_data.get("player_gold", 10),
                save_data.get("player_inventory", []),
                save_data.get("equipped_weapon", None),
                list(player_map_pos),
                monsters,
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
def explore_map(player_hp, player_gold, player_inventory, equipped_weapon, current_player_map_pos, monsters):
    """
    Handles the graphical map exploration using Pygame.
    """
    pygame.init()
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("World Map")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 24)

        # --- Image Loading ---
        image_cache = {}

        def load_image(filename):
            """Loads an image with error handling and caching."""
            filepath = os.path.join('images', filename)
            try:
                if filename not in image_cache:
                    if os.path.exists(filepath):
                        image_cache[filename] = pygame.image.load(filepath).convert_alpha()
                        image_cache[filename] = pygame.transform.scale(image_cache[filename], (CELL_SIZE, CELL_SIZE))
                    else:
                        print(f"Warning: Image file not found: {filepath}. Using fallback.")
                        fallback_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
                        if 'player' in filename:
                            fallback_surface.fill(BLACK)
                        else:
                            fallback_surface.fill(RED)
                        image_cache[filename] = fallback_surface
                return image_cache[filename]
            except pygame.error as e:
                print(f"Error loading image '{filename}': {e}. Using fallback.")
                fallback_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
                if 'player' in filename:
                    fallback_surface.fill(BLACK)
                else:
                    fallback_surface.fill(RED)
                image_cache[filename] = fallback_surface
                return fallback_surface

        player_image = load_image('player.png')
        monster_images = {
            "Zombie": load_image("Zombie.png"),
            "Slime": load_image("slime.png"),
            "Goblin": load_image("goblin.png")
        }

        player_pos = list(current_player_map_pos)
        initial_pos = tuple(current_player_map_pos)
        running = True
        map_outcome = 'map_running'
        player_move_count = 0
        interacting_with_npc = False
        npc_interaction_text = ""

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'quit', player_hp, player_gold, player_inventory, equipped_weapon, player_pos, monsters

                if not interacting_with_npc:
                    if event.type == pygame.KEYDOWN:
                        next_pos = list(player_pos)
                        if event.key == pygame.K_UP:
                            next_pos[1] -= 1
                        elif event.key == pygame.K_DOWN:
                            next_pos[1] += 1
                        elif event.key == pygame.K_LEFT:
                            next_pos[0] -= 1
                        elif event.key == pygame.K_RIGHT:
                            next_pos[0] += 1
                        else:
                            continue

                        if 0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE:
                            player_pos = next_pos
                            current_pos_tuple = tuple(player_pos)

                            for npc in npcs:
                                if npc["pos"] == current_pos_tuple:
                                    interacting_with_npc = True
                                    npc_interaction_text = npc["dialogue"]
                                    print(f"You encountered {npc['name']}: {npc_interaction_text}")
                                    break

                            for i, monster in enumerate(monsters):
                                if (monster.x, monster.y) == current_pos_tuple:
                                    print(f"\nYou encountered a {monster.name}!")
                                    try:
                                        (
                                            player_hp,
                                            player_gold,
                                            player_inventory,
                                            equipped_weapon,
                                            fight_status,
                                        ) = gamefunctions.handle_fight(
                                            player_hp, player_gold, player_inventory, equipped_weapon, monster.name
                                        )
                                        if fight_status == 'died':
                                            map_outcome = 'game_over'
                                            running = False
                                        elif fight_status == 'won':
                                            del monsters[i]
                                            break
                                    except AttributeError:
                                        print("Error: 'handle_fight' function not found in gamefunctions.")
                                        map_outcome = 'town'
                                        running = False
                                    except Exception as e:
                                        print(f"An error occurred during the fight: {e}")
                                        map_outcome = 'town'
                                        running = False
                elif event.type == pygame.KEYDOWN:
                    interacting_with_npc = False
                    npc_interaction_text = ""

            screen.fill(WHITE)

            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

            town_center_x = TOWN_POS[0] * CELL_SIZE + CELL_SIZE // 2
            town_center_y = TOWN_POS[1] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, GREEN, (town_center_x, town_center_y), CELL_SIZE // 2 - 4, 4)

            for monster in monsters:
                monster_image_to_draw = monster_images.get(monster.name)
                if monster_image_to_draw:
                    monster_rect = monster_image_to_draw.get_rect(topleft=(monster.x * CELL_SIZE, monster.y * CELL_SIZE))
                    screen.blit(monster_image_to_draw, monster_rect)
                else:
                    monster_rect = pygame.Rect(monster.x * CELL_SIZE, monster.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, RED, monster_rect)

            for npc in npcs:
                npc_x = npc["pos"][0] * CELL_SIZE + CELL_SIZE // 2
                npc_y = npc["pos"][1] * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, YELLOW, (npc_x, npc_y), CELL_SIZE // 2 - 4, 4)

            player_rect = player_image.get_rect(topleft=(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE))
            screen.blit(player_image, player_rect)

            if interacting_with_npc:
                text_surface = font.render(npc_interaction_text, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
                pygame.draw.rect(screen, WHITE, text_rect.inflate(10, 5))
                screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(10)

    # --- End of Map Loop ---
      
        pygame.quit()
    except Exception as e:
        print(f"Error during pygame.quit(): {e}")
    return map_outcome, player_hp, player_gold, player_inventory, equipped_weapon, player_pos, monsters


if __name__ == "__main__":
    main()
