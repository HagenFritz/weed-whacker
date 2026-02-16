"""
Base asset manager providing common sprite loading/generation functionality
"""

import pygame
from pathlib import Path


class BaseAssetManager:
    """Base class for asset managers with common sprite loading logic"""
    
    def __init__(self, tile_size, asset_subdir):
        """Initialize base asset manager
        
        Args:
            tile_size: Size of tiles in pixels
            asset_subdir: Subdirectory under assets/sprites/ for this asset type
        """
        self.tile_size = tile_size
        self.sprites = {}
        self.asset_dir = Path(__file__).parent.parent / 'sprites' / asset_subdir
        self.asset_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_or_generate(self, name, generator_func, size=None):
        """Load sprite from file or generate it
        
        Args:
            name: Sprite name (without extension)
            generator_func: Function to generate sprite if file not found
            size: Custom size tuple (width, height), defaults to (tile_size, tile_size)
            
        Returns:
            Pygame surface with the sprite
        """
        if size is None:
            size = (self.tile_size, self.tile_size)
        
        # Try to load from PNG file
        sprite_path = self.asset_dir / f'{name}.png'
        if sprite_path.exists():
            try:
                loaded_sprite = pygame.image.load(str(sprite_path))
                # Scale to desired size if needed
                if loaded_sprite.get_size() != size:
                    return pygame.transform.scale(loaded_sprite, size)
                return loaded_sprite
            except pygame.error:
                pass
        
        # Generate programmatically as fallback
        return generator_func()
    
    def get_sprite(self, name):
        """Get a sprite by name
        
        Args:
            name: Sprite identifier
            
        Returns:
            Pygame surface or None if not found
        """
        return self.sprites.get(name)
    
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
