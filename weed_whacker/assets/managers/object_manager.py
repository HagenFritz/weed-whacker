"""
Object asset manager - handles decorative objects, buildings, etc.
"""

import pygame
from .base_asset_manager import BaseAssetManager


class ObjectManager(BaseAssetManager):
    """Manages object sprites (rocks, trees, buildings, decorations, etc.)"""
    
    def __init__(self, tile_size):
        """Initialize object manager
        
        Args:
            tile_size: Size of tiles in pixels
        """
        super().__init__(tile_size, 'objects')
        self._load_objects()
    
    def _load_objects(self):
        """Load or generate all object sprites"""
        # Future objects - ready to enable when needed
        # self.sprites['rock_small'] = self._load_or_generate(
        #     'rock_small',
        #     lambda: self._generate_rock('small')
        # )
        # self.sprites['rock_large'] = self._load_or_generate(
        #     'rock_large',
        #     lambda: self._generate_rock('large')
        # )
        # self.sprites['tree'] = self._load_or_generate(
        #     'tree',
        #     self._generate_tree
        # )
        # self.sprites['fence'] = self._load_or_generate(
        #     'fence',
        #     self._generate_fence
        # )
        pass
    
    def _generate_rock(self, size_type):
        """Generate rock sprite programmatically
        
        Args:
            size_type: Size type (small, medium, large)
            
        Returns:
            Pygame surface with rock sprite
        """
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        
        rock_color = (100, 100, 100)
        highlight_color = (130, 130, 130)
        
        size_map = {
            'small': self.tile_size // 4,
            'medium': self.tile_size // 3,
            'large': self.tile_size // 2
        }
        
        radius = size_map.get(size_type, size_map['medium'])
        center = self.tile_size // 2
        
        # Main rock body
        pygame.draw.circle(surface, rock_color, (center, center), radius)
        
        # Highlight for 3D effect
        pygame.draw.circle(surface, highlight_color, (center - radius // 3, center - radius // 3), radius // 3)
        
        return surface
    
    def _generate_tree(self):
        """Generate tree sprite programmatically"""
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        
        trunk_color = (101, 67, 33)
        leaves_color = (34, 139, 34)
        
        # Trunk
        trunk_width = max(2, self.tile_size // 8)
        trunk_height = self.tile_size // 2
        trunk_x = self.tile_size // 2 - trunk_width // 2
        trunk_y = self.tile_size - trunk_height
        pygame.draw.rect(surface, trunk_color, (trunk_x, trunk_y, trunk_width, trunk_height))
        
        # Leaves (circle)
        leaves_radius = max(4, self.tile_size // 3)
        leaves_center = self.tile_size // 2
        pygame.draw.circle(surface, leaves_color, (leaves_center, leaves_center), leaves_radius)
        
        return surface
    
    def _generate_fence(self):
        """Generate fence sprite programmatically"""
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        
        fence_color = (139, 90, 43)
        
        # Vertical posts
        post_width = max(1, self.tile_size // 16)
        post_height = self.tile_size // 2
        
        pygame.draw.rect(surface, fence_color, (0, self.tile_size // 4, post_width, post_height))
        pygame.draw.rect(surface, fence_color, (self.tile_size - post_width, self.tile_size // 4, post_width, post_height))
        
        # Horizontal rails
        rail_height = max(1, self.tile_size // 16)
        pygame.draw.rect(surface, fence_color, (0, self.tile_size // 3, self.tile_size, rail_height))
        pygame.draw.rect(surface, fence_color, (0, self.tile_size // 2, self.tile_size, rail_height))
        
        return surface
