"""
Grid rendering module
"""

import pygame
from ..game.grid import TileType


class GridRenderer:
    """Handles grid and tile rendering"""
    
    def __init__(self, asset_manager):
        """Initialize grid renderer
        
        Args:
            asset_manager: AssetManager instance
        """
        self.asset_manager = asset_manager
    
    def render(self, surface, grid, tile_size, camera_offset):
        """Render the grid to a surface
        
        Args:
            surface: Pygame surface to render to
            grid: Grid instance
            tile_size: Size of each tile in pixels
            camera_offset: (x, y) camera offset in pixels
        """
        for y in range(grid.world_size):
            for x in range(grid.world_size):
                tile = grid.tiles[y][x]
                
                # Calculate screen position with camera offset
                screen_x = x * tile_size - camera_offset[0]
                screen_y = y * tile_size - camera_offset[1]
                
                # Render base tile (only owned and purchasable tiles)
                if tile.tile_type == TileType.GRASS or tile.tile_type == TileType.WEED:
                    # Use variation based on tile position for visual variety (1-3 to match assets)
                    variation = ((x + y) % 3) + 1
                    grass_sprite = f'grass_{variation}'
                    self.asset_manager.render_sprite(surface, grass_sprite, screen_x, screen_y)
                elif tile.tile_type == TileType.UNOWNED:
                    # Only render if purchasable (adjacent to owned tiles)
                    if self._is_purchasable(grid, x, y):
                        sprite_name = 'unowned_purchasable'
                        self.asset_manager.render_sprite(surface, sprite_name, screen_x, screen_y)
                    # Skip rendering non-purchasable unowned tiles
                
                # Render weed overlay on top of grass
                if tile.tile_type == TileType.WEED:
                    self.asset_manager.render_sprite(surface, 'weed_basic', screen_x, screen_y)
    
    def _is_purchasable(self, grid, x, y):
        """Check if an unowned tile is purchasable (adjacent to owned tiles)
        
        Args:
            grid: Grid instance
            x, y: Tile coordinates
            
        Returns:
            True if tile is unowned and adjacent to at least one owned tile
        """
        tile = grid.get_tile(x, y)
        if not tile or tile.tile_type != TileType.UNOWNED:
            return False
        
        # Check all four adjacent tiles
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            neighbor = grid.get_tile(x + dx, y + dy)
            if neighbor and neighbor.tile_type in (TileType.GRASS, TileType.WEED):
                return True
        
        return False
