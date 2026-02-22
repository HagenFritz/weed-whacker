"""
Player rendering module
"""

import pygame

from ..constants.colors import COOLDOWN_COOLING, COOLDOWN_READY, BAR_BG_DARK


class PlayerRenderer:
    """Handles player and cooldown bar rendering"""
    
    def __init__(self, asset_manager):
        """Initialize player renderer
        
        Args:
            asset_manager: AssetManager instance
        """
        self.asset_manager = asset_manager
    
    def render(self, surface, player, tile_size, camera_offset):
        """Render the player sprite
        
        Args:
            surface: Pygame surface to render to
            player: Player instance
            tile_size: Size of tiles in pixels
            camera_offset: (x, y) camera offset
        """
        # Calculate player screen position
        screen_x = player.x * tile_size - camera_offset[0]
        screen_y = player.y * tile_size - camera_offset[1]
        
        # Render player sprite
        self.asset_manager.render_sprite(surface, 'player', screen_x, screen_y)
    
    def render_cooldown(self, surface, player, tile_size, camera_offset):
        """Render the chop cooldown bar below the player with tool icon
        
        Args:
            surface: Pygame surface to render to
            player: Player instance
            tile_size: Size of tiles in pixels
            camera_offset: (x, y) camera offset
        """
        # Get player screen position
        player_screen_x = player.x * tile_size - camera_offset[0]
        player_screen_y = player.y * tile_size - camera_offset[1]
        
        # Get tool sprite
        tool_sprite = self.asset_manager.get_sprite(player.current_tool)
        icon_size = tool_sprite.get_width() if tool_sprite else 8
        
        # Position bar at bottom of player tile
        bar_width = tile_size - icon_size - 6
        bar_height = 3
        bar_x = player_screen_x + icon_size + 4
        bar_y = player_screen_y + tile_size - bar_height - 2
        
        # Render tool icon
        tool_x = player_screen_x + 2
        tool_y = player_screen_y + tile_size - icon_size - 1
        if tool_sprite:
            surface.blit(tool_sprite, (tool_x, tool_y))
        
        # Background (dark gray)
        pygame.draw.rect(surface, BAR_BG_DARK, (bar_x, bar_y, bar_width, bar_height))
        
        # Get cooldown percentage
        cooldown_percent = player.get_chop_cooldown_percent()
        
        # Fill bar based on cooldown state
        if cooldown_percent > 0:
            # Red when cooling down
            fill_color = COOLDOWN_COOLING
            fill_width = int(bar_width * (1.0 - cooldown_percent))
        else:
            # Green when ready
            fill_color = COOLDOWN_READY
            fill_width = bar_width
        
        if fill_width > 0:
            pygame.draw.rect(surface, fill_color, (bar_x, bar_y, fill_width, bar_height))
