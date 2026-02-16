"""
Weed Whacker - Income, Money, and Purchasing System
"""

from .grid import TileType


class Economy:
    """Manages money, income, and tile purchasing"""

    def __init__(self, grid, income_per_tile, base_cost, cost_increment):
        """Initialize economy system

        Args:
            grid: Reference to the game grid
            income_per_tile: Income per grass tile per second
            base_cost: Base cost for first additional tile
            cost_increment: Cost increase per tile purchased
        """
        self.grid = grid
        self.money = 0.0
        self.income_per_tile = income_per_tile
        self.base_cost = base_cost
        self.cost_increment = cost_increment
        self.tiles_purchased = 0  # Number of tiles beyond starting plot

    def update(self, dt):
        """Update income accumulation

        Args:
            dt: Delta time in milliseconds
        """
        # Calculate income per frame
        grass_count = self.grid.count_tiles_by_type(TileType.GRASS)
        income_per_ms = (grass_count * self.income_per_tile) / 1000.0
        self.money += income_per_ms * dt

    def get_money_display(self):
        """Get money as whole number for display

        Returns:
            Integer money value
        """
        return int(self.money)

    def get_income_rate(self):
        """Get current income rate per second

        Returns:
            Income per second
        """
        grass_count = self.grid.count_tiles_by_type(TileType.GRASS)
        return grass_count * self.income_per_tile

    def get_next_tile_cost(self):
        """Calculate cost of next tile purchase

        Returns:
            Cost in dollars
        """
        return self.base_cost + (self.tiles_purchased * self.cost_increment)

    def can_afford_tile(self):
        """Check if player can afford the next tile

        Returns:
            True if player has enough money
        """
        return self.money >= self.get_next_tile_cost()

    def try_purchase_tile(self, x, y):
        """Attempt to purchase a tile

        Args:
            x, y: Tile coordinates to purchase

        Returns:
            True if purchase was successful
        """
        tile = self.grid.get_tile(x, y)
        if not tile or tile.tile_type != TileType.UNOWNED:
            return False

        # Check if adjacent to owned tile
        if not self._is_adjacent_to_owned(x, y):
            return False

        # Check if player can afford it
        cost = self.get_next_tile_cost()
        if self.money < cost:
            return False

        # Purchase the tile
        self.money -= cost
        self.tiles_purchased += 1
        tile.tile_type = TileType.GRASS
        return True

    def _is_adjacent_to_owned(self, x, y):
        """Check if a tile is adjacent to an owned tile

        Args:
            x, y: Tile coordinates

        Returns:
            True if adjacent to at least one owned tile
        """
        # Check up, down, left, right (not diagonals)
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            neighbor = self.grid.get_tile(x + dx, y + dy)
            if neighbor and neighbor.is_owned():
                return True
        return False

    def get_owned_tile_count(self):
        """Get total number of owned tiles

        Returns:
            Number of grass and weed tiles
        """
        grass = self.grid.count_tiles_by_type(TileType.GRASS)
        weeds = self.grid.count_tiles_by_type(TileType.WEED)
        return grass + weeds
