"""
Weed Whacker - Grid and Tile Management
"""

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
        
        # Weed state tracking
        self.weed_type = None  # Weed instance (from weeds.py)
        self.weed_health = 0.0  # Current health of the weed
        self.last_movement_count = 0  # Player movement count when last damaged

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

    def render(self, surface, tile_size, camera_offset=(0, 0), sprite_manager=None):
        """Render the grid to a surface

        Args:
            surface: Pygame surface to render to
            tile_size: Size of each tile in pixels
            camera_offset: (x, y) camera offset in pixels for future scrolling
            sprite_manager: SpriteManager instance for rendering sprites
        """
        for y in range(self.world_size):
            for x in range(self.world_size):
                tile = self.tiles[y][x]
                
                # Calculate screen position with camera offset
                screen_x = x * tile_size - camera_offset[0]
                screen_y = y * tile_size - camera_offset[1]
                
                # Render base tile
                if tile.tile_type == TileType.GRASS or tile.tile_type == TileType.WEED:
                    # Use variation based on tile position for visual variety
                    variation = (x + y) % 3
                    grass_sprite = f'grass_{variation}'
                    if sprite_manager:
                        sprite_manager.render_sprite(surface, grass_sprite, screen_x, screen_y)
                elif tile.tile_type == TileType.UNOWNED:
                    # Check if this is a purchasable tile
                    if self._is_purchasable(x, y):
                        sprite_name = 'unowned_purchasable'
                    else:
                        sprite_name = 'unowned'
                    if sprite_manager:
                        sprite_manager.render_sprite(surface, sprite_name, screen_x, screen_y)
                
                # Render weed overlay on top of grass
                if tile.tile_type == TileType.WEED:
                    if sprite_manager:
                        sprite_manager.render_sprite(surface, 'weed_basic', screen_x, screen_y)

    def _is_purchasable(self, x, y):
        """Check if an unowned tile is purchasable (adjacent to owned tiles)
        
        Args:
            x, y: Tile coordinates
            
        Returns:
            True if tile is unowned and adjacent to at least one owned tile
        """
        tile = self.get_tile(x, y)
        if not tile or tile.tile_type != TileType.UNOWNED:
            return False
        
        # Check all four adjacent tiles (not diagonals)
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            neighbor = self.get_tile(x + dx, y + dy)
            if neighbor and neighbor.is_owned():
                return True
        
        return False
