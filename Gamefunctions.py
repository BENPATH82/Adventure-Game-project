
# Game functions file
# PATHOU BETALE
# 02/16/2025



import random      # this helps choose numbers at random 

# Function to purchase items

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1):
    total_cost = itemPrice * quantityToPurchase
    if total_cost > startingMoney:
        quantity_purchased = startingMoney // itemPrice
        money_remaining = startingMoney - (quantity_purchased * itemPrice)
    else:
        quantity_purchased = quantityToPurchase
        money_remaining = startingMoney - total_cost
    return int(quantity_purchased), money_remaining

# Function to generate a new random monster

def new_random_monster():
    monsters = [
        {
            "name": "A goblin",
            "description": "This is a lone goblin. When it notices you, it rushes at you quickly with a sharp dagger drawn.",
            "health": random.randint(5, 10),
            "power": random.randint(3, 7),
            "money": round(random.uniform(1.0, 20.0), 2)
        },
        {
            "name": "A dragon",
            "description": "A fearsome dragon appears, with scales glistening and fire in its eyes.",
            "health": random.randint(50, 100),
            "power": random.randint(20, 35),
            "money": round(random.uniform(100.0, 500.0), 2)
        },
        {
            "name": " Vulture",
            "description": "You discover a vulture eating the remains of two orcs that appear to have killed each other.They were carrying a chest that contains a small treasure horde.",
            "health": random.randint(30, 60),
            "power": random.randint(15, 25),
            "money": round(random.uniform(10.0, 50.0), 2)
        }
    ]
    return random.choice(monsters)

# showing the purchase_item() function

print("purchase_item function:")
num_purchased, leftover_money = purchase_item(1.23, 10, 3)
print(num_purchased)  
print(leftover_money) 

num_purchased, leftover_money = purchase_item(1.23, 2.01, 3)
print(num_purchased)  
print(leftover_money) 

num_purchased, leftover_money = purchase_item(3.41, 21.12)
print(num_purchased)  
print(leftover_money) 

num_purchased, leftover_money = purchase_item(31.41, 21.12)
print(num_purchased)  
print(leftover_money) 

# Showing the new_random_monster() function

print("\n new_random_monster function:")

my_monster = new_random_monster()
print(my_monster['name'])
print(my_monster['description'])
print(my_monster['health'])
print(my_monster['power'])
print(my_monster['money'])

my_monster = new_random_monster()
print(my_monster['name'])
print(my_monster['description'])
print(my_monster['health'])
print(my_monster['power'])
print(my_monster['money'])

my_monster = new_random_monster()
print(my_monster['name'])
print(my_monster['description'])
print(my_monster['health'])
print(my_monster['power'])
print(my_monster['money'])
