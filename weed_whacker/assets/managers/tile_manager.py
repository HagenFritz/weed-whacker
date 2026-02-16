"""
Tile asset manager - handles grass, unowned tiles, and tile variations
"""

import pygame
from .base_asset_manager import BaseAssetManager


class TileManager(BaseAssetManager):
    """Manages tile sprites (grass variations, unowned, etc.)"""
    
    def __init__(self, tile_size):
        """Initialize tile manager
        
        Args:
            tile_size: Size of tiles in pixels
        """
        super().__init__(tile_size, 'tiles')
        self._load_tiles()
    
    def _load_tiles(self):
        """Load or generate all tile sprites"""
        # Load grass variations (grass_1, grass_2, grass_3 from PNG files)
        # Note: Using 1-based indexing to match asset filenames
        for i in range(1, 4):
            self.sprites[f'grass_{i}'] = self._load_or_generate(
                f'grass_{i}',
                lambda variation=i-1: self._generate_grass(variation)
            )
        
        # Generate unowned tiles
        self.sprites['unowned'] = self._load_or_generate(
            'unowned',
            self._generate_unowned
        )
        self.sprites['unowned_purchasable'] = self._load_or_generate(
            'unowned_purchasable',
            self._generate_unowned_purchasable
        )
    
    def _generate_grass(self, variation=0):
        """Generate grass tile sprite programmatically
        
        Args:
            variation: Color variation offset (0-2) for texture
        """
        surface = pygame.Surface((self.tile_size, self.tile_size))
        
        # Base green color with variation
        base_color_offsets = [0, -10, 10]
        color_offset = base_color_offsets[variation % 3]
        grass_color = (34 + color_offset, 139 + color_offset, 34 + color_offset)
        surface.fill(grass_color)
        
        # Add some texture with darker green dots
        dark_green = (20 + color_offset, 100 + color_offset, 20 + color_offset)
        for i in range(self.tile_size // 4):
            x = (i * 7 + variation * 3) % self.tile_size
            y = (i * 11 + variation * 5) % self.tile_size
            pygame.draw.circle(surface, dark_green, (x, y), max(1, self.tile_size // 16))
        
        return surface
    
    def _generate_unowned(self):
        """Generate unowned tile sprite programmatically"""
        surface = pygame.Surface((self.tile_size, self.tile_size))
        
        # Dark gray/brown background
        dirt_color = (60, 50, 40)
        surface.fill(dirt_color)
        
        # Lighter brown border
        border_color = (80, 70, 60)
        border_width = max(1, self.tile_size // 16)
        pygame.draw.rect(surface, border_color, surface.get_rect(), border_width)
        
        return surface
    
    def _generate_unowned_purchasable(self):
        """Generate purchasable unowned tile sprite programmatically"""
        surface = pygame.Surface((self.tile_size, self.tile_size))
        
        # Lighter dirt to indicate purchasable
        dirt_color = (70, 60, 50)
        surface.fill(dirt_color)
        
        # Yellow-ish border to hint it's purchasable
        border_color = (120, 110, 70)
        border_width = max(1, self.tile_size // 16)
        pygame.draw.rect(surface, border_color, surface.get_rect(), border_width)
        
        return surface
