"""
Player asset manager - handles different player avatars and skins
"""

import pygame
from .base_asset_manager import BaseAssetManager


class PlayerManager(BaseAssetManager):
    """Manages player sprites (different avatars, skins, animations)"""
    
    def __init__(self, tile_size):
        """Initialize player manager
        
        Args:
            tile_size: Size of tiles in pixels
        """
        super().__init__(tile_size, 'players')
        self._load_players()
    
    def _load_players(self):
        """Load or generate all player sprites"""
        # Default player - loads farmer.png
        self.sprites['player'] = self._load_or_generate(
            'farmer',
            lambda: self._generate_player('default')
        )
        
        # TODO: Add character selection system to allow players to choose their avatar
        
        # Future player avatars - ready to enable
        # self.sprites['player_blue'] = self._load_or_generate(
        #     'player_blue',
        #     lambda: self._generate_player('blue')
        # )
        # self.sprites['player_red'] = self._load_or_generate(
        #     'player_red',
        #     lambda: self._generate_player('red')
        # )
    
    def _generate_player(self, avatar_type):
        """Generate player sprite programmatically
        
        Args:
            avatar_type: Type of player avatar (default, blue, red, etc.)
            
        Returns:
            Pygame surface with player sprite
        """
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        
        # Color variations based on avatar type
        color_map = {
            'default': (64, 164, 223),
            'blue': (50, 100, 200),
            'red': (200, 50, 50),
            'green': (50, 200, 50)
        }
        
        player_color = color_map.get(avatar_type, color_map['default'])
        border_color = tuple(max(0, c - 40) for c in player_color)
        
        padding = max(2, self.tile_size // 16)
        
        # Fill
        pygame.draw.rect(
            surface,
            player_color,
            (padding, padding, self.tile_size - padding * 2, self.tile_size - padding * 2)
        )
        
        # Border
        border_width = max(1, self.tile_size // 32)
        pygame.draw.rect(
            surface,
            border_color,
            (padding, padding, self.tile_size - padding * 2, self.tile_size - padding * 2),
            border_width
        )
        
        return surface
