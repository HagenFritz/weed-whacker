"""
Weed Whacker - Grid and Tile Management
"""

import pygame
from enum import Enum


class TileType(Enum):
    """Types of tiles in the game"""
    GRASS = "grass"      # Clear, earnable tile
    WEED = "weed"        # Tile with a weed on it
    UNOWNED = "unowned"  # Not part of the plot


class Tile:
    """Represents a single tile in the grid"""

    def __init__(self, tile_type=TileType.UNOWNED):
        self.tile_type = tile_type

    def is_owned(self):
        """Check if this tile is owned by the player"""
        return self.tile_type in (TileType.GRASS, TileType.WEED)

    def is_walkable(self):
        """Check if the player can walk on this tile"""
        return self.is_owned()


class Grid:
    """Manages the game grid and tiles"""

    def __init__(self, world_size, starting_size):
        """Initialize grid

        Args:
            world_size: Total grid size (e.g., 30x30)
            starting_size: Starting owned plot size (e.g., 5x5)
        """
        self.world_size = world_size
        self.tiles = [[Tile() for _ in range(world_size)] for _ in range(world_size)]

        # Initialize starting plot in the center
        self._initialize_starting_plot(starting_size)

    def _initialize_starting_plot(self, size):
        """Create the starting owned plot in the center"""
        center = self.world_size // 2
        start = center - size // 2

        for y in range(start, start + size):
            for x in range(start, start + size):
                self.tiles[y][x].tile_type = TileType.GRASS

    def get_tile(self, x, y):
        """Get tile at position

        Args:
            x, y: Tile coordinates

        Returns:
            Tile object or None if out of bounds
        """
        if 0 <= x < self.world_size and 0 <= y < self.world_size:
            return self.tiles[y][x]
        return None

    def count_tiles_by_type(self, tile_type):
        """Count how many tiles of a given type exist

        Args:
            tile_type: TileType to count

        Returns:
            Number of tiles of that type
        """
        count = 0
        for row in self.tiles:
            for tile in row:
                if tile.tile_type == tile_type:
                    count += 1
        return count

    def render(self, surface, tile_size, camera_offset=(0, 0)):
        """Render the grid to a surface

        Args:
            surface: Pygame surface to render to
            tile_size: Size of each tile in pixels
            camera_offset: (x, y) camera offset in pixels for future scrolling
        """
        for y in range(self.world_size):
            for x in range(self.world_size):
                tile = self.tiles[y][x]
                
                # Calculate screen position with camera offset
                screen_x = x * tile_size - camera_offset[0]
                screen_y = y * tile_size - camera_offset[1]
                
                # Choose color based on tile type
                if tile.tile_type == TileType.GRASS:
                    # Green with slight variation for texture
                    base_green = (34, 139, 34)
                    variation = ((x + y) % 3) * 8
                    color = (
                        max(0, base_green[0] - variation),
                        max(0, base_green[1] - variation),
                        max(0, base_green[2] - variation)
                    )
                elif tile.tile_type == TileType.WEED:
                    # Same green base (will add weed sprite on top later)
                    color = (34, 139, 34)
                elif tile.tile_type == TileType.UNOWNED:
                    # Dark gray
                    color = (40, 40, 40)
                
                # Draw the tile
                pygame.draw.rect(
                    surface,
                    color,
                    (screen_x, screen_y, tile_size, tile_size)
                )
                
                # Draw subtle border for owned tiles
                if tile.is_owned():
                    border_color = (25, 100, 25)
                    pygame.draw.rect(
                        surface,
                        border_color,
                        (screen_x, screen_y, tile_size, tile_size),
                        1
                    )
