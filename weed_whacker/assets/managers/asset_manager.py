"""
Unified asset manager - coordinates all specialized asset managers
"""

from .tile_manager import TileManager
from .weed_manager import WeedManager
from .player_manager import PlayerManager
from .tool_manager import ToolManager
from .object_manager import ObjectManager
import pygame
from pathlib import Path


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
        
        # Sound dictionary
        self.sounds = {}
        self.assets_dir = Path(__file__).parent.parent.parent / 'assets'
        
        # Initialize mixer if not already
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def get_sound(self, sound_file: str):
        """Get or load a sound file
        
        Args:
            sound_file: Relative path to sound file from weed_whacker directory
            
        Returns:
            pygame.mixer.Sound object or None if failed
        """
        if not sound_file:
            return None
            
        if sound_file not in self.sounds:
            # We assume sound_file is relative to the weed_whacker directory, e.g. 'assets/sounds/scythe.wav'
            # Adjust path relative to weed_whacker directory
            full_path = Path(__file__).parent.parent.parent / sound_file
            if full_path.exists():
                try:
                    self.sounds[sound_file] = pygame.mixer.Sound(str(full_path))
                except pygame.error:
                    print(f"Failed to load sound: {full_path}")
                    self.sounds[sound_file] = None
            else:
                print(f"Sound file not found: {full_path}")
                self.sounds[sound_file] = None
                
        return self.sounds.get(sound_file)

    def play_sound(self, sound_file: str):
        """Play a sound file
        
        Args:
            sound_file: Relative path to sound file
        """
        sound = self.get_sound(sound_file)
        if sound:
            sound.play()
    
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
