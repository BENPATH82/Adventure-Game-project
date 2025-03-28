import random

def print_welcome(player_name):
    print(f"Welcome, {player_name}!")

def new_random_monster():
    monsters = [
        {"name": "Goblin", "hp": 20, "attack": 5, "description": "A small, green goblin with sharp teeth."},
        {"name": "Orc", "hp": 30, "attack": 8, "description": "A large, muscular orc wielding a crude axe."},
        {"name": "Spider", "hp": 15, "attack": 7, "description": "A giant spider with venomous fangs."},
    ]
    return random.choice(monsters)

def print_shop_menu(items):
    print("Shop:")
    for i, item in enumerate(items):
        print(f"{i + 1}) {item['name']}: ${item['price']}")

def purchase_item(item, money, quantity, inventory):
    total_cost = item['price'] * quantity
    if money >= total_cost:
        remaining_money = money - total_cost
        for _ in range(quantity):
            inventory.append(item.copy()) # adding a copy to avoid modification of original item
        return quantity, remaining_money
    else:
        print("Not enough money!")
        return 0, money

def display_fight_statistics(player_hp, monster_hp, monster_name):
    print(f"\nYour HP: {player_hp}, {monster_name} HP: {monster_hp}")

def get_user_fight_options():
    print("1) Attack")
    print("2) Run Away")
    print("3) Use Item")
    choice = input("Enter your choice: ")
    return choice

def handle_player_attack(player_attack, monster_hp, equipped_weapon):
    damage = random.randint(player_attack - 2, player_attack + 2)
    if equipped_weapon:
        damage += 5  # Example weapon bonus
        equipped_weapon['currentDurability'] -= 1
        if equipped_weapon['currentDurability'] <= 0:
            print("Your weapon broke!")
            equipped_weapon = None
    monster_hp -= damage
    print(f"You dealt {damage} damage!")
    return monster_hp, equipped_weapon

def handle_monster_attack(monster_attack, player_hp):
    damage = random.randint(monster_attack - 2, monster_attack + 2)
    player_hp -= damage
    print(f"The monster dealt {damage} damage!")
    return player_hp

def sleep(player_hp, gold):
    if gold >= 5:
        player_hp = 30
        gold -= 5
        print("You feel rested and your HP is fully restored.")
    else:
        print("You don't have enough gold to sleep.")
    return player_hp, gold

def handle_fight(player_hp, player_gold, inventory, equipped_weapon):
    print("\nA wild monster appears!")
    monster = new_random_monster()
    monster_hp = monster["hp"]
    print(f"You encountered: {monster['description']}")

    while player_hp > 0 and monster_hp > 0:
        display_fight_statistics(player_hp, monster_hp, monster["name"])
        fight_choice = get_user_fight_options()

        if fight_choice == '1':
            monster_hp, equipped_weapon = handle_player_attack(10, monster_hp, equipped_weapon)
            if monster_hp > 0:
                player_hp = handle_monster_attack(monster["attack"], player_hp)
        elif fight_choice == '2':
            print("You ran away!")
            return player_hp, player_gold, inventory, equipped_weapon
        elif fight_choice == '3':
            item_used, inventory = handle_item_use(inventory, monster)
            if item_used:
                print(f"You used {item_used['name']}!")
                monster_hp = 0 # instant kill
        else:
            print("Invalid choice. Try again.")

    if player_hp <= 0:
        print("You were defeated!")
        return 30, player_gold // 2, inventory, equipped_weapon
    else:
        print(f"You defeated the {monster['name']}!")
        player_gold += 20
        return player_hp, player_gold, inventory, equipped_weapon

def handle_item_use(inventory, monster):
    usable_items = [item for item in inventory if item.get('use_on') == monster['name']]
    if not usable_items:
        print("No usable items found.")
        return None, inventory

    print("Choose an item to use:")
    for i, item in enumerate(usable_items):
        print(f"{i + 1}) {item['name']}")

    try:
        choice = int(input("Enter your choice: ")) - 1
        used_item = usable_items.pop(choice)
        inventory.remove(used_item)
        return used_item, inventory
    except (ValueError, IndexError):
        print("Invalid choice.")
        return None, inventory

def equip_item(inventory):
    weapon_items = [item for item in inventory if item['type'] == 'weapon']
    if not weapon_items:
        print("No weapons to equip.")
        return None

    print("Choose a weapon to equip:")
    for i, item in enumerate(weapon_items):
        print(f"{i + 1}) {item['name']}")
    print(f"{len(weapon_items) + 1}) None")

    try:
        choice = int(input("Enter your choice: "))
        if choice == len(weapon_items) + 1:
            return None
        equipped_weapon = weapon_items[choice - 1]
        return equipped_weapon
    except (ValueError, IndexError):
        print("Invalid choice.")
        return None
