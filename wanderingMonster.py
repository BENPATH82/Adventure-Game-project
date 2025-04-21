import random
import pygame


class WanderingMonster:
    """
    Represents a wandering monster on the game map.

    Attributes:
        x (int): The x-coordinate (column) of the monster's position on the grid.
        y (int): The y-coordinate (row) of the monster's position on the grid.
        color (tuple): The RGB color of the monster.
        name (str): The name of the monster.
        gold (int): The amount of gold the monster carries.
    """

    def __init__(self, x, y, color, name, gold):
        """
        Initializes a new WanderingMonster.

        Args:
            x (int): The initial x-coordinate (column) of the monster.
            y (int): The initial y-coordinate (row) of the monster.
            color (tuple): The RGB color of the monster.
            name (str): The name of the monster.
            gold (int): The amount of gold the monster carries.
        """
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.gold = gold

    def move(self, grid_size, town_x, town_y):
        """
        Attempts to move the monster to a new position on the grid.

        The monster will move in a random direction (up, down, left, right)
        and the new position is validated to ensure it stays within the grid
        boundaries and does not enter the town square.

        Args:
            grid_size (int): The size of the game grid.
            town_x (int): The x-coordinate (column) of the town square.
            town_y (int): The y-coordinate (row) of the town square.
        """

        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Random direction
        new_x = self.x + dx
        new_y = self.y + dy

        if (
            0 <= new_x < grid_size
            and 0 <= new_y < grid_size
            and (new_x, new_y) != (town_x, town_y)
        ):
            self.x = new_x
            self.y = new_y

    @staticmethod
    def new_random_monster(grid_size, town_x, town_y):
        """
        Creates a new monster at a random valid location on the grid.

        Args:
            grid_size (int): The size of the game grid.
            town_x (int): The x-coordinate (column) of the town square.
            town_y (int): The y-coordinate (row) of the town square.

        Returns:
            WanderingMonster: A new WanderingMonster object.
        """
        while True:
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)
            if (x, y) != (town_x, town_y):
                break

        monster_type = random.choice(["Zombie", "Slime", "Goblin"])
        if monster_type == "Zombie":
            color = (100, 200, 100)  # Greenish
        elif monster_type == "Slime":
            color = (0, 150, 0)  # Darker Green
        else:  # Goblin
            color = (200, 100, 0)  # Orangeish

        return WanderingMonster(x, y, color, monster_type, random.randint(5, 20))
