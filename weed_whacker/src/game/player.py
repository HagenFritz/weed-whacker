"""
Weed Whacker - Player Movement and Actions
"""

import pygame


class Player:
    """Player character with tile-based movement"""

    def __init__(self, start_x, start_y, grid):
        """Initialize player

        Args:
            start_x, start_y: Starting tile coordinates
            grid: Reference to the game grid
        """
        self.x = start_x
        self.y = start_y
        self.grid = grid

        # Cooldowns
        self.move_cooldown = 0
        self.chop_cooldown = 0
        
        # Current equipped tool
        self.current_tool = 'hand_hoe_stone'  # Default starting tool
        # TODO: Implement tool inventory and equipment system for store purchases

    def update(self, dt):
        """Update player state

        Args:
            dt: Delta time in milliseconds
        """
        # Update cooldowns
        if self.move_cooldown > 0:
            self.move_cooldown -= dt
        if self.chop_cooldown > 0:
            self.chop_cooldown -= dt

    def try_move(self, dx, dy, move_cooldown_time):
        """Attempt to move in a direction

        Args:
            dx, dy: Direction to move (-1, 0, or 1)
            move_cooldown_time: Cooldown duration in ms

        Returns:
            True if move was successful
        """
        if self.move_cooldown > 0:
            return False

        new_x = self.x + dx
        new_y = self.y + dy

        # Check if target tile is walkable
        tile = self.grid.get_tile(new_x, new_y)
        if tile and tile.is_walkable():
            self.x = new_x
            self.y = new_y
            self.move_cooldown = move_cooldown_time
            return True

        return False

    def try_chop(self, chop_cooldown_time):
        """Attempt to chop weed on current tile

        Args:
            chop_cooldown_time: Cooldown duration in ms

        Returns:
            True if chop was successful
        """
        if self.chop_cooldown > 0:
            return False

        from .grid import TileType

        tile = self.grid.get_tile(self.x, self.y)
        if tile and tile.tile_type == TileType.WEED:
            tile.tile_type = TileType.GRASS
            self.chop_cooldown = chop_cooldown_time
            return True

        return False

    def get_chop_cooldown_percent(self):
        """Get chop cooldown progress as percentage

        Returns:
            Float between 0.0 (ready) and 1.0 (just chopped)
        """
        if self.chop_cooldown <= 0:
            return 0.0
        return self.chop_cooldown / 1000.0  # Assuming 1000ms cooldown

    def render(self, surface, tile_size, camera_offset=(0, 0), sprite_manager=None):
        """Render the player to a surface

        Args:
            surface: Pygame surface to render to
            tile_size: Size of each tile in pixels
            camera_offset: (x, y) camera offset in pixels
            sprite_manager: SpriteManager instance for rendering sprites
        """
        # Calculate screen position
        screen_x = self.x * tile_size - camera_offset[0]
        screen_y = self.y * tile_size - camera_offset[1]
        
        # Render the player sprite
        if sprite_manager:
            sprite_manager.render_sprite(surface, 'player', screen_x, screen_y)
