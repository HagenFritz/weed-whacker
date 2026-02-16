"""
Tool asset manager - handles different tools and equipment
"""

import pygame
from .base_asset_manager import BaseAssetManager


class ToolManager(BaseAssetManager):
    """Manages tool sprites (scythe, hoe, watering can, etc.)"""
    
    def __init__(self, tile_size):
        """Initialize tool manager
        
        Args:
            tile_size: Size of tiles in pixels
        """
        super().__init__(tile_size, 'tools')
        self._load_tools()
    
    def _load_tools(self):
        """Load or generate all tool sprites"""
        # Tool icons (for UI and cooldown bar)
        icon_size = max(12, self.tile_size // 2)
        
        # Load actual tool assets
        self.sprites['hand_hoe_stone'] = self._load_or_generate(
            'hand_hoe_stone',
            self._generate_hoe,
            size=(icon_size, icon_size)
        )
        self.sprites['scythe_iron'] = self._load_or_generate(
            'scythe_iron',
            self._generate_scythe,
            size=(icon_size, icon_size)
        )
        
        # Future tools - ready to enable
        # self.sprites['hoe'] = self._load_or_generate(
        #     'hoe',
        #     self._generate_hoe,
        #     size=(icon_size, icon_size)
        # )
        # self.sprites['watering_can'] = self._load_or_generate(
        #     'watering_can',
        #     self._generate_watering_can,
        #     size=(icon_size, icon_size)
        # )
    
    def _generate_scythe(self):
        """Generate a scythe icon sprite programmatically"""
        size = max(12, self.tile_size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        handle_color = (139, 69, 19)
        blade_color = (200, 200, 200)
        
        # Handle (vertical brown line)
        handle_width = max(1, size // 8)
        pygame.draw.line(
            surface, 
            handle_color, 
            (size // 2, size // 3), 
            (size // 2, size - 2), 
            handle_width
        )
        
        # Blade (curved gray arc)
        blade_width = max(2, size // 6)
        pygame.draw.arc(
            surface, 
            blade_color, 
            (1, 1, size - 2, size - 2), 
            3.6, 6.0, 
            blade_width
        )
        pygame.draw.line(
            surface, 
            blade_color, 
            (size // 2, size // 3), 
            (size - 2, size // 4), 
            blade_width
        )
        
        return surface
    
    def _generate_hoe(self):
        """Generate a hoe icon sprite programmatically"""
        size = max(12, self.tile_size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        handle_color = (139, 69, 19)
        blade_color = (120, 120, 120)
        
        # Handle (diagonal brown line)
        handle_width = max(1, size // 8)
        pygame.draw.line(
            surface,
            handle_color,
            (size // 4, size - 2),
            (size - 2, size // 4),
            handle_width
        )
        
        # Blade (horizontal gray rectangle)
        blade_rect = pygame.Rect(size - 6, size // 4 - 2, 4, 4)
        pygame.draw.rect(surface, blade_color, blade_rect)
        
        return surface
    
    def _generate_watering_can(self):
        """Generate a watering can icon sprite programmatically"""
        size = max(12, self.tile_size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        can_color = (100, 150, 200)
        
        # Can body (circle)
        pygame.draw.circle(
            surface,
            can_color,
            (size // 2, size // 2),
            max(3, size // 4)
        )
        
        # Spout (small line)
        pygame.draw.line(
            surface,
            can_color,
            (size // 2 + size // 4, size // 2),
            (size - 2, size // 2 - size // 4),
            max(1, size // 8)
        )
        
        return surface
