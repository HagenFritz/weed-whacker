"""
Weed Whacker - Sprite Management
Handles sprite loading and generation (programmatic or from files)
"""

import pygame
import os


class SpriteManager:
    """Manages game sprites with fallback to programmatic generation"""
    
    def __init__(self, tile_size=16):
        """Initialize sprite manager
        
        Args:
            tile_size: Size of tiles in pixels
        """
        self.tile_size = tile_size
        self.sprites = {}
        self._load_or_generate_sprites()
    
    def _load_or_generate_sprites(self):
        """Load sprites from files or generate programmatically as fallback"""
        sprite_dir = os.path.join(os.path.dirname(__file__), 'sprites')
        
        # Try to load each sprite, fall back to generation if not found
        self.sprites['player'] = self._load_or_generate('player', sprite_dir, self._generate_player)
        
        # Generate grass variations (0, 1, 2 for color variety)
        for i in range(3):
            sprite_name = f'grass_{i}'
            self.sprites[sprite_name] = self._load_or_generate(
                sprite_name, sprite_dir, lambda v=i: self._generate_grass(v)
            )
        
        # Generate basic weed (future: weed_thistle, weed_dandelion, etc.)
        self.sprites['weed_basic'] = self._load_or_generate(
            'weed_basic', sprite_dir, lambda: self._generate_weed(0)
        )
        
        self.sprites['unowned'] = self._load_or_generate('unowned', sprite_dir, self._generate_unowned)
        self.sprites['unowned_purchasable'] = self._load_or_generate(
            'unowned_purchasable', sprite_dir, self._generate_unowned_purchasable
        )
        self.sprites['scythe'] = self._load_or_generate('scythe', sprite_dir, self._generate_scythe)
    
    def _load_or_generate(self, name, sprite_dir, generator_func):
        """Load sprite from file or generate it
        
        Args:
            name: Sprite name
            sprite_dir: Directory containing sprite files
            generator_func: Function to generate sprite if file not found
            
        Returns:
            Pygame Surface with the sprite
        """
        # Try to load PNG file
        filepath = os.path.join(sprite_dir, f'{name}.png')
        if os.path.exists(filepath):
            try:
                sprite = pygame.image.load(filepath).convert_alpha()
                # Scale if needed
                if sprite.get_width() != self.tile_size or sprite.get_height() != self.tile_size:
                    sprite = pygame.transform.scale(sprite, (self.tile_size, self.tile_size))
                return sprite
            except Exception as e:
                print(f"Warning: Failed to load {filepath}: {e}")
        
        # Fall back to programmatic generation
        return generator_func()
    
    def _generate_player(self):
        """Generate player sprite programmatically"""
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        
        # Blue square with darker border
        player_color = (64, 164, 223)
        border_color = (40, 100, 140)
        padding = 2
        
        # Fill
        pygame.draw.rect(
            surface,
            player_color,
            (padding, padding, self.tile_size - padding * 2, self.tile_size - padding * 2)
        )
        
        # Border
        pygame.draw.rect(
            surface,
            border_color,
            (padding, padding, self.tile_size - padding * 2, self.tile_size - padding * 2),
            1
        )
        
        return surface

    def _generate_scythe(self):
        """Generate a simple scythe icon sprite programmatically"""
        size = min(12, self.tile_size // 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        handle_color = (139, 69, 19)
        blade_color = (200, 200, 200)
        # Handle
        pygame.draw.line(surface, handle_color, (size // 2, size // 3), (size // 2, size - 2), 2)
        # Blade
        pygame.draw.arc(surface, blade_color, (1, 1, size - 2, size - 2), 3.6, 6.0, 2)
        pygame.draw.line(surface, blade_color, (size // 2, size // 3), (size - 2, size // 4), 2)
        return surface
    
    def _generate_grass(self, variation=0):
        """Generate grass tile sprite programmatically
        
        Args:
            variation: Color variation offset (0-2) for texture
        """
        surface = pygame.Surface((self.tile_size, self.tile_size))
        
        # Base green color with variation
        base_green = (34, 139, 34)
        variation_offset = variation * 8
        color = (
            max(0, base_green[0] - variation_offset),
            max(0, base_green[1] - variation_offset),
            max(0, base_green[2] - variation_offset)
        )
        surface.fill(color)
        
        # Add some texture variation
        for i in range(5):
            x = (i * 7) % self.tile_size
            y = (i * 5) % self.tile_size
            darker = (max(0, color[0] - 10), max(0, color[1] - 10), max(0, color[2] - 10))
            pygame.draw.line(surface, darker, (x, 0), (x, self.tile_size), 1)
        
        # Border
        border_color = (25, 100, 25)
        pygame.draw.rect(surface, border_color, (0, 0, self.tile_size, self.tile_size), 1)
        
        return surface
    
    def _generate_weed(self, variation=0):
        """Generate weed sprite on grass background
        
        Args:
            variation: Color variation offset for grass background
        """
        # Start with grass background
        surface = self._generate_grass(variation)
        
        # Weed colors
        stem_color = (60, 80, 40)
        leaf_color = (80, 120, 60)
        
        center_x = self.tile_size // 2
        center_y = self.tile_size // 2
        
        # Draw stem
        pygame.draw.line(surface, stem_color, (center_x, center_y + 2), (center_x, center_y - 4), 2)
        
        # Draw leaves
        pygame.draw.line(surface, leaf_color, (center_x, center_y - 1), (center_x - 3, center_y - 3), 1)
        pygame.draw.line(surface, leaf_color, (center_x, center_y - 1), (center_x + 3, center_y - 3), 1)
        pygame.draw.line(surface, leaf_color, (center_x, center_y - 3), (center_x - 2, center_y - 5), 1)
        pygame.draw.line(surface, leaf_color, (center_x, center_y - 3), (center_x + 2, center_y - 5), 1)
        
        return surface
    
    def _generate_unowned(self):
        """Generate unowned tile sprite programmatically"""
        surface = pygame.Surface((self.tile_size, self.tile_size))
        surface.fill((40, 40, 40))
        return surface
    
    def _generate_unowned_purchasable(self):
        """Generate purchasable unowned tile sprite programmatically"""
        surface = pygame.Surface((self.tile_size, self.tile_size))
        surface.fill((60, 60, 60))
        
        # Highlight border
        highlight_color = (100, 100, 120)
        pygame.draw.rect(surface, highlight_color, (0, 0, self.tile_size, self.tile_size), 1)
        
        return surface
    
    def get_sprite(self, name):
        """Get a sprite by name
        
        Args:
            name: Sprite name (e.g., 'player', 'grass', 'weed')
            
        Returns:
            Pygame Surface with the sprite
        """
        return self.sprites.get(name)
    
    def render_sprite(self, surface, name, x, y):
        """Render a sprite at a specific position
        
        Args:
            surface: Surface to render to
            name: Sprite name
            x, y: Position to render at
        """
        sprite = self.get_sprite(name)
        if sprite:
            surface.blit(sprite, (x, y))
