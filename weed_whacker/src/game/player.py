"""
Weed Whacker - Player Movement and Actions
"""

from .grid import TileType

class Player:
    """Player character with tile-based movement"""

    def __init__(self, start_x, start_y, grid, asset_manager=None):
        """Initialize player

        Args:
            start_x, start_y: Starting tile coordinates
            grid: Reference to the game grid
            asset_manager: Asset manager for playing sounds
        """
        self.x = start_x
        self.y = start_y
        self.grid = grid
        self.asset_manager = asset_manager

        # Cooldowns
        self.move_cooldown = 0
        self.chop_cooldown = 0
        
        # Current equipped tool
        self.current_tool = 'hand_hoe'  # Default starting tool
        
        # Tools owned by the player
        self.owned_tools = ['hand_hoe']
        
        # Tool usage tracking per tool
        self.tool_uses = {'hand_hoe': 0}
        
        # Movement tracking for weed regrowth
        self.movement_count = 0

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
            self.movement_count += 1  # Track movements for weed regrowth
            return True

        return False

    def try_chop(self, chop_cooldown_time):
        """Attempt to chop weeds based on current tool's reach

        Args:
            chop_cooldown_time: Cooldown duration in ms

        Returns:
            Tuple of (True if chop was successful (damage dealt to at least one weed), Broken tool key or None)
        """
        if self.chop_cooldown > 0:
            return False, None
        
        # Get current tool
        from .tools import get_tool
        tool = get_tool(self.current_tool)
        
        chopped_any = False
        
        for dx, dy in tool.reach:
            target_x = self.x + dx
            target_y = self.y + dy
            tile = self.grid.get_tile(target_x, target_y)
            
            if tile and tile.tile_type == TileType.WEED and tile.weed_type:
                # Calculate regrowth since last damage
                if tile.weed_health < tile.weed_type.toughness:
                    movements_since_damage = self.movement_count - tile.last_movement_count
                    regrowth_amount = movements_since_damage // tile.weed_type.regrow
                    tile.weed_health = min(tile.weed_type.toughness, tile.weed_health + regrowth_amount)
                
                # Deal damage based on tool efficiency
                tile.weed_health -= tool.efficiency
                tile.last_movement_count = self.movement_count
                
                # Check if weed is destroyed
                if tile.weed_health <= 0:
                    tile.tile_type = TileType.GRASS
                    tile.weed_type = None
                    tile.weed_health = 0.0
                    
                chopped_any = True
                
        if chopped_any:
            # Play tool sound if it has one
            if tool.sound_file and hasattr(self, 'asset_manager'):
                self.asset_manager.play_sound(tool.sound_file)
                
            # Increment tool usage counter
            if self.current_tool not in self.tool_uses:
                self.tool_uses[self.current_tool] = 0
            self.tool_uses[self.current_tool] += 1
            
            self.chop_cooldown = chop_cooldown_time
            
            # Check if tool breaks
            broken_tool = None
            if tool.longevity > 0 and self.tool_uses[self.current_tool] >= tool.longevity:
                broken_tool = self.current_tool
                self.owned_tools.remove(self.current_tool)
                self.current_tool = 'hand_hoe' # Default back to hand hoe
            
            return True, broken_tool

        return False, None

    def get_chop_cooldown_percent(self):
        """Get chop cooldown progress as percentage

        Returns:
            Float between 0.0 (ready) and 1.0 (just chopped)
        """
        if self.chop_cooldown <= 0:
            return 0.0
            
        from .tools import get_tool
        tool = get_tool(self.current_tool)
        # Using base cooldown for UI percentage calculation
        return min(1.0, self.chop_cooldown / float(tool.cooldown))

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
