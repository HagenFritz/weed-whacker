"""
Weed asset manager - handles different weed types and variations
"""

import pygame
from .base_asset_manager import BaseAssetManager


class WeedManager(BaseAssetManager):
    """Manages weed sprites (basic, thistle, dandelion, etc. with variations)"""
    
    def __init__(self, tile_size):
        """Initialize weed manager
        
        Args:
            tile_size: Size of tiles in pixels
        """
        super().__init__(tile_size, 'weeds')
        self._load_weeds()
    
    def _load_weeds(self):
        """Load or generate all weed sprites"""
        # Basic weed (current default)
        self.sprites['weed_basic'] = self._load_or_generate(
            'weed_basic',
            lambda: self._generate_weed('basic', 0)
        )
        
        # Future weed types - commented out for now, ready to enable
        # self.sprites['weed_thistle'] = self._load_or_generate(
        #     'weed_thistle',
        #     lambda: self._generate_weed('thistle', 0)
        # )
        # self.sprites['weed_dandelion'] = self._load_or_generate(
        #     'weed_dandelion',
        #     lambda: self._generate_weed('dandelion', 0)
        # )
    
    def _generate_weed(self, weed_type, variation=0):
        """Generate weed sprite on grass background for transparency
        
        Args:
            weed_type: Type of weed (basic, thistle, dandelion, etc.)
            variation: Visual variation of the same type
            
        Returns:
            Pygame surface with weed sprite
        """
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        
        if weed_type == 'basic':
            self._draw_basic_weed(surface, variation)
        elif weed_type == 'thistle':
            self._draw_thistle_weed(surface, variation)
        elif weed_type == 'dandelion':
            self._draw_dandelion_weed(surface, variation)
        
        return surface
    
    def _draw_basic_weed(self, surface, variation):
        """Draw a basic weed sprite
        
        Args:
            surface: Surface to draw on
            variation: Visual variation
        """
        # Dark green weed color
        weed_color = (20, 80, 20)
        center_x = self.tile_size // 2
        center_y = self.tile_size // 2
        weed_radius = max(2, self.tile_size // 6)
        
        # Draw clumpy weed shape
        for offset in [(-1, -1), (1, -1), (0, 1), (-1, 1), (1, 0)]:
            x = center_x + offset[0] * weed_radius
            y = center_y + offset[1] * weed_radius
            pygame.draw.circle(surface, weed_color, (x, y), weed_radius)
    
    def _draw_thistle_weed(self, surface, variation):
        """Draw a thistle weed sprite (spiky, purple tint)
        
        Args:
            surface: Surface to draw on
            variation: Visual variation
        """
        # Purple-ish thistle color
        thistle_color = (60, 40, 80)
        center_x = self.tile_size // 2
        center_y = self.tile_size // 2
        
        # Draw spiky shapes
        points = []
        num_spikes = 6
        for i in range(num_spikes):
            angle = (i / num_spikes) * 6.28
            radius = max(3, self.tile_size // 4)
            x = center_x + int(radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
            y = center_y + int(radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, thistle_color, points)
    
    def _draw_dandelion_weed(self, surface, variation):
        """Draw a dandelion weed sprite (fluffy, yellow tint)
        
        Args:
            surface: Surface to draw on
            variation: Visual variation
        """
        # Yellow dandelion color
        dandelion_color = (180, 180, 60)
        center_x = self.tile_size // 2
        center_y = self.tile_size // 2
        
        # Draw fluffy circle with small dots around
        main_radius = max(2, self.tile_size // 8)
        pygame.draw.circle(surface, dandelion_color, (center_x, center_y), main_radius)
        
        # Add fluffy dots around
        for i in range(8):
            angle = (i / 8) * 6.28
            radius = max(4, self.tile_size // 5)
            x = center_x + int(radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
            y = center_y + int(radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
            pygame.draw.circle(surface, dandelion_color, (x, y), max(1, main_radius // 2))
