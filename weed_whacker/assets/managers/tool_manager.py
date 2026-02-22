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
        self.sprites['hand_hoe'] = self._load_or_generate(
            'hand_hoe',
            self._generate_hoe,
            size=(icon_size, icon_size)
        )
        self.sprites['scythe'] = self._load_or_generate(
            'scythe',
            self._generate_scythe,
            size=(icon_size, icon_size)
        )
        self.sprites['chainsaw'] = self._load_or_generate(
            'chainsaw',
            self._generate_chainsaw,
            size=(icon_size, icon_size)
        )
        self.sprites['aerosol'] = self._load_or_generate(
            'aerosol',
            self._generate_aerosol,
            size=(icon_size, icon_size)
        )
        self.sprites['shears'] = self._load_or_generate(
            'shears',
            self._generate_shears,
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
    
    def _generate_shears(self):
        """Generate a shears icon sprite programmatically"""
        size = max(12, self.tile_size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        handle_color = (200, 50, 50)
        blade_color = (180, 180, 180)
        
        # Handles
        pygame.draw.line(surface, handle_color, (size // 4, size), (size // 2, size // 2), 2)
        pygame.draw.line(surface, handle_color, (size * 3 // 4, size), (size // 2, size // 2), 2)
        
        # Blades
        pygame.draw.line(surface, blade_color, (size // 2, size // 2), (size // 4, 0), 2)
        pygame.draw.line(surface, blade_color, (size // 2, size // 2), (size * 3 // 4, 0), 2)
        
        # Pivot point
        pygame.draw.circle(surface, (50, 50, 50), (size // 2, size // 2), 2)
        
        return surface
        
    def _generate_aerosol(self):
        """Generate an aerosol can icon sprite programmatically"""
        size = max(12, self.tile_size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        can_color = (200, 200, 200)
        label_color = (50, 200, 50)
        cap_color = (50, 50, 50)
        
        # Can body
        body_width = size // 2
        body_height = size * 2 // 3
        body_x = (size - body_width) // 2
        body_y = size - body_height
        pygame.draw.rect(surface, can_color, (body_x, body_y, body_width, body_height))
        
        # Label
        pygame.draw.rect(surface, label_color, (body_x, body_y + body_height // 4, body_width, body_height // 2))
        
        # Cap
        cap_width = body_width * 3 // 4
        cap_height = size // 6
        cap_x = (size - cap_width) // 2
        cap_y = body_y - cap_height
        pygame.draw.rect(surface, cap_color, (cap_x, cap_y, cap_width, cap_height))
        
        # Nozzle
        pygame.draw.rect(surface, (100, 100, 100), (cap_x + cap_width // 4, cap_y - 2, cap_width // 2, 2))
        
        return surface
        
    def _generate_chainsaw(self):
        """Generate a chainsaw icon sprite programmatically"""
        size = max(12, self.tile_size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        body_color = (220, 100, 0)
        handle_color = (50, 50, 50)
        blade_color = (150, 150, 150)
        
        # Body
        body_width = size // 2
        body_height = size // 2
        body_x = 0
        body_y = (size - body_height) // 2
        pygame.draw.rect(surface, body_color, (body_x, body_y, body_width, body_height))
        
        # Blade
        blade_width = size // 2
        blade_height = size // 4
        blade_x = body_width
        blade_y = (size - blade_height) // 2
        pygame.draw.rect(surface, blade_color, (blade_x, blade_y, blade_width, blade_height))
        
        # Chain dots
        for x in range(blade_x + 2, blade_x + blade_width, 4):
            pygame.draw.circle(surface, (50, 50, 50), (x, blade_y), 1)
            pygame.draw.circle(surface, (50, 50, 50), (x, blade_y + blade_height), 1)
            
        # Handles
        pygame.draw.rect(surface, handle_color, (body_x, body_y - 2, body_width // 2, 2)) # Top
        pygame.draw.rect(surface, handle_color, (body_x - 2, body_y, 2, body_height)) # Back
        
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
