"""
Unified asset manager - coordinates all specialized asset managers
"""

from .tile_manager import TileManager
from .weed_manager import WeedManager
from .player_manager import PlayerManager
from .tool_manager import ToolManager
from .object_manager import ObjectManager


class AssetManager:
    """Unified manager coordinating all asset types"""
    
    def __init__(self, tile_size):
        """Initialize all asset managers
        
        Args:
            tile_size: Size of tiles in pixels
        """
        self.tile_size = tile_size
        
        # Initialize specialized managers
        self.tiles = TileManager(tile_size)
        self.weeds = WeedManager(tile_size)
        self.players = PlayerManager(tile_size)
        self.tools = ToolManager(tile_size)
        self.objects = ObjectManager(tile_size)
    
    def get_sprite(self, sprite_name):
        """Get a sprite by name from any manager
        
        Tries each manager in order until sprite is found.
        
        Args:
            sprite_name: Name of the sprite to retrieve
            
        Returns:
            Pygame surface or None if not found
        """
        # Try each manager
        for manager in [self.tiles, self.weeds, self.players, self.tools, self.objects]:
            sprite = manager.get_sprite(sprite_name)
            if sprite:
                return sprite
        
        return None
    
    def render_sprite(self, surface, sprite_name, x, y):
        """Render a sprite to a surface
        
        Args:
            surface: Target surface to render to
            sprite_name: Name of the sprite to render
            x, y: Screen coordinates
        """
        sprite = self.get_sprite(sprite_name)
        if sprite:
            surface.blit(sprite, (x, y))
