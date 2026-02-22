"""
Weed Whacker - Main Game State and Loop Logic
"""

import pygame # type: ignore
import random
from .constants.colors import BLACK

from .game.grid import Grid, TileType
from .game.player import Player
from .game.economy import Economy
from .game.weeds import WEED_BASIC
from .ui.hud import UI
from .render.grid_renderer import GridRenderer
from .render.player_renderer import PlayerRenderer
from ..assets.managers.asset_manager import AssetManager
from ..config import (
    TILE_SIZE,
    INTERNAL_WIDTH,
    INTERNAL_HEIGHT,
    STARTING_GRID_SIZE,
    WORLD_GRID_SIZE,
    PLAYER_MOVE_COOLDOWN,
    CHOP_COOLDOWN,
    WEED_SPAWN_INTERVAL,
    INCOME_PER_TILE_PER_SECOND,
    TILE_BASE_COST,
    TILE_COST_INCREMENT
)


class Game:
    """Main game state manager"""

    def __init__(self):
        """Initialize game state"""
        self.running = True
        
        # Initialize grid first
        self.grid = Grid(WORLD_GRID_SIZE, STARTING_GRID_SIZE)
        
        # Initialize sub-systems
        self.economy = Economy(
            self.grid,
            INCOME_PER_TILE_PER_SECOND,
            TILE_BASE_COST,
            TILE_COST_INCREMENT
        )
        
        from weed_whacker.src.game.events import EventManager
        self.event_manager = EventManager()
        
        # Initialize asset manager
        self.asset_manager = AssetManager(TILE_SIZE)
        
        # Initialize renderers
        self.grid_renderer = GridRenderer(self.asset_manager)
        self.player_renderer = PlayerRenderer(self.asset_manager)
        
        # Initialize UI
        self.ui = UI()
        from weed_whacker.src.ui.inventory_ui import InventoryUI
        self.inventory_ui = InventoryUI()
        
        # Initialize grid
        self.grid = Grid(WORLD_GRID_SIZE, STARTING_GRID_SIZE)
        
        # Calculate camera offset to center the grid on screen
        # The grid is WORLD_GRID_SIZE tiles, we want to center it
        grid_pixel_width = WORLD_GRID_SIZE * TILE_SIZE
        grid_pixel_height = WORLD_GRID_SIZE * TILE_SIZE
        self.camera_offset = (
            (grid_pixel_width - INTERNAL_WIDTH) // 2,
            (grid_pixel_height - INTERNAL_HEIGHT) // 2
        )
        
        # Initialize player at center of starting plot
        center_tile = WORLD_GRID_SIZE // 2
        self.player = Player(center_tile, center_tile, self.grid, self.asset_manager)
        
        # Initialize economy system
        self.economy = Economy(
            self.grid,
            INCOME_PER_TILE_PER_SECOND,
            TILE_BASE_COST,
            TILE_COST_INCREMENT
        )
        
        # Weed spawning timer
        self.weed_spawn_timer = 0
        

    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            # DEBUG CHEATS (F1-F12 keys)
            if event.key == pygame.K_F1:
                # Add $1000
                self.economy.money += 1000
                print("DEBUG: Added $1000")
            elif event.key == pygame.K_F2:
                # Unlock all tools
                from weed_whacker.src.game.tools import TOOLS
                for tool_id in TOOLS:
                    if tool_id not in self.player.owned_tools:
                        self.player.owned_tools.append(tool_id)
                        self.player.tool_uses[tool_id] = 0
                print("DEBUG: Unlocked all tools")
            elif event.key == pygame.K_F3:
                # Spawn weed everywhere
                for y in range(self.grid.world_size):
                    for x in range(self.grid.world_size):
                        tile = self.grid.get_tile(x, y)
                        if tile and tile.tile_type == TileType.GRASS:
                            tile.tile_type = TileType.WEED
                            tile.weed_type = WEED_BASIC
                            tile.weed_health = WEED_BASIC.toughness
                            tile.last_movement_count = self.player.movement_count
                print("DEBUG: Spawned weeds everywhere")

            # Handle inventory toggling
            if event.key == pygame.K_i:
                self.inventory_ui.toggle()
            elif event.key == pygame.K_ESCAPE and self.inventory_ui.is_open:
                self.inventory_ui.toggle()
                
            # Ignore other inputs if inventory is open
            if self.inventory_ui.is_open:
                return

            # Movement with WASD or arrow keys
            move_cooldown = PLAYER_MOVE_COOLDOWN * self.event_manager.get_player_speed_mult()
            if event.key in (pygame.K_w, pygame.K_UP):
                self.player.try_move(0, -1, move_cooldown)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.player.try_move(0, 1, move_cooldown)
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                self.player.try_move(-1, 0, move_cooldown)
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.player.try_move(1, 0, move_cooldown)
            # Chop action
            elif event.key == pygame.K_SPACE:
                from weed_whacker.src.game.tools import get_tool
                current_tool = get_tool(self.player.current_tool)
                chop_cooldown = current_tool.cooldown * self.event_manager.get_tool_cooldown_mult()
                success, broken_tool = self.player.try_chop(chop_cooldown)
                if broken_tool:
                    from weed_whacker.src.game.tools import get_tool
                    tool_name = get_tool(broken_tool).name
                    from weed_whacker.src.ui.shared import MessageDialog
                    if not hasattr(self, 'message_dialog'):
                        self.message_dialog = MessageDialog()
                    self.message_dialog.show(
                        "Tool Broke!",
                        f"Your {tool_name} broke and was removed from your inventory."
                    )
            # Buy tile
            elif event.key == pygame.K_b:
                self._try_purchase_selected_tile()
            # Cycle through purchasable tiles
            elif event.key == pygame.K_TAB:
                purchasable_tiles = self._get_all_purchasable_tiles()
                self.ui.cycle_selected_tile(1, len(purchasable_tiles))
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle message dialog clicks
            if hasattr(self, 'message_dialog') and self.message_dialog.active:
                if event.button == 1:
                    self.message_dialog.handle_click(event.pos)
                return

            # Handle inventory clicks if open
            if self.inventory_ui.is_open:
                if event.button == 1: # Left click
                    self.inventory_ui.handle_click(event.pos, self.player, self.economy)
                return
                
            # Left click to chop
            if event.button == 1:
                from weed_whacker.src.game.tools import get_tool
                current_tool = get_tool(self.player.current_tool)
                chop_cooldown = current_tool.cooldown * self.event_manager.get_tool_cooldown_mult()
                success, broken_tool = self.player.try_chop(chop_cooldown)
                if broken_tool:
                    from weed_whacker.src.game.tools import get_tool
                    tool_name = get_tool(broken_tool).name
                    from weed_whacker.src.ui.shared import MessageDialog
                    if not hasattr(self, 'message_dialog'):
                        self.message_dialog = MessageDialog()
                    self.message_dialog.show(
                        "Tool Broke!",
                        f"Your {tool_name} broke and was removed from your inventory."
                    )

    def update(self, dt):
        """Update game state

        Args:
            dt: Delta time in milliseconds since last frame
        """
        # Update event manager
        self.event_manager.update(dt)
        
        # Apply event multipliers to economy
        current_income_rate = INCOME_PER_TILE_PER_SECOND * self.event_manager.get_income_mult()
        self.economy.income_rate = current_income_rate
        
        # Update player cooldowns
        self.player.update(dt)
        
        # Update economy (income accumulation)
        self.economy.update(dt)
        
        # Update UI components
        if self.inventory_ui.is_open:
            self.inventory_ui.update()
        
        # Update weed spawn timer
        self.weed_spawn_timer += dt
        spawn_interval = WEED_SPAWN_INTERVAL / self.event_manager.get_weed_spawn_rate_mult()
        if self.weed_spawn_timer >= spawn_interval:
            self.weed_spawn_timer = 0
            self._spawn_weed()

    def render(self, surface):
        """Render game to surface

        Args:
            surface: Pygame surface to render to
        """
        # Clear screen
        surface.fill(BLACK)

        # Render grid using renderer
        self.grid_renderer.render(surface, self.grid, TILE_SIZE, self.camera_offset)
        
        # Render player using renderer
        self.player_renderer.render(surface, self.player, TILE_SIZE, self.camera_offset)
        
        # Render purchasable tile highlights
        purchasable_tiles = self._get_all_purchasable_tiles()
        for i, (tile_x, tile_y) in enumerate(purchasable_tiles):
            is_selected = (i == self.ui.get_selected_index())
            self.ui.render_tile_highlight(surface, tile_x, tile_y, TILE_SIZE, self.camera_offset, is_selected)
        
        # Render UI/HUD
        money = self.economy.money
        income_rate = self.economy.income_rate
        owned_tiles = self.economy.get_owned_tile_count()
        self.ui.render_hud(surface, money, income_rate, owned_tiles, self.player, self.asset_manager, self.event_manager, INTERNAL_WIDTH)
        
        # Render purchase UI if tiles available
        if purchasable_tiles:
            cost = self.economy.get_next_tile_cost()
            can_afford = self.economy.can_afford_tile()
            self.ui.render_purchase_ui(surface, purchasable_tiles, cost, can_afford, INTERNAL_WIDTH, INTERNAL_HEIGHT)
            
        # Render store UI (renders on top of everything else if open)
        self.inventory_ui.render(surface, INTERNAL_WIDTH, INTERNAL_HEIGHT, self.player, self.asset_manager)

        # Render message dialog if active
        if hasattr(self, 'message_dialog') and self.message_dialog.active:
            self.message_dialog.render(surface, INTERNAL_WIDTH, INTERNAL_HEIGHT)

    def _spawn_weed(self):
        """Spawn a weed on a random GRASS tile"""
        
        # Collect all GRASS tiles
        grass_tiles = []
        for y in range(self.grid.world_size):
            for x in range(self.grid.world_size):
                tile = self.grid.get_tile(x, y)
                if tile and tile.tile_type == TileType.GRASS:
                    grass_tiles.append((x, y))
        
        # If there are valid grass tiles, spawn on a random one
        if grass_tiles:
            x, y = random.choice(grass_tiles)
            tile = self.grid.get_tile(x, y)
            tile.tile_type = TileType.WEED
            tile.weed_type = WEED_BASIC
            tile.weed_health = WEED_BASIC.toughness
            tile.last_movement_count = self.player.movement_count

    def _get_all_purchasable_tiles(self):
        """Get all coordinates of purchasable tiles adjacent to the player
        
        Returns:
            List of (x, y) tuples for all purchasable tiles
        """
        purchasable = []
        
        # Check all four directions from player
        directions = [
            (0, -1),  # Up
            (0, 1),   # Down
            (-1, 0),  # Left
            (1, 0)    # Right
        ]
        
        for dx, dy in directions:
            tile_x = self.player.x + dx
            tile_y = self.player.y + dy
            tile = self.grid.get_tile(tile_x, tile_y)
            
            # Check if tile is unowned and has at least one owned neighbor
            if tile and tile.tile_type == TileType.UNOWNED:
                # Verify it's adjacent to owned tiles (should be, since player is owned)
                if self.economy._is_adjacent_to_owned(tile_x, tile_y):
                    purchasable.append((tile_x, tile_y))
        
        return purchasable

    def _try_purchase_selected_tile(self):
        """Attempt to purchase the currently selected tile"""
        purchasable_tiles = self._get_all_purchasable_tiles()
        
        if not purchasable_tiles:
            return
        
        # Get selected tile
        selected_index = self.ui.get_selected_index()
        if selected_index < len(purchasable_tiles):
            x, y = purchasable_tiles[selected_index]
            success = self.economy.try_purchase_tile(x, y)
            if success:
                # Reset selection after successful purchase
                self.ui.reset_selection()
