"""
Weed Whacker - Main Game State and Loop Logic
"""

import pygame
import random
from .game.grid import Grid, TileType
from .game.player import Player
from .game.economy import Economy
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
        
        # Initialize asset manager
        self.asset_manager = AssetManager(TILE_SIZE)
        
        # Initialize renderers
        self.grid_renderer = GridRenderer(self.asset_manager)
        self.player_renderer = PlayerRenderer(self.asset_manager)
        
        # Initialize UI
        self.ui = UI()
        
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
        self.player = Player(center_tile, center_tile, self.grid)
        
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
            # Movement with WASD or arrow keys
            if event.key in (pygame.K_w, pygame.K_UP):
                self.player.try_move(0, -1, PLAYER_MOVE_COOLDOWN)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.player.try_move(0, 1, PLAYER_MOVE_COOLDOWN)
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                self.player.try_move(-1, 0, PLAYER_MOVE_COOLDOWN)
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.player.try_move(1, 0, PLAYER_MOVE_COOLDOWN)
            # Chop action
            elif event.key == pygame.K_SPACE:
                self.player.try_chop(CHOP_COOLDOWN)
            # Buy tile
            elif event.key == pygame.K_b:
                self._try_purchase_selected_tile()
            # Cycle through purchasable tiles
            elif event.key == pygame.K_TAB:
                purchasable_tiles = self._get_all_purchasable_tiles()
                self.ui.cycle_selected_tile(1, len(purchasable_tiles))
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left click to chop
            if event.button == 1:
                self.player.try_chop(CHOP_COOLDOWN)

    def update(self, dt):
        """Update game state

        Args:
            dt: Delta time in milliseconds since last frame
        """
        # Update player cooldowns
        self.player.update(dt)
        
        # Update economy (income accumulation)
        self.economy.update(dt)
        
        # Update weed spawn timer
        self.weed_spawn_timer += dt
        if self.weed_spawn_timer >= WEED_SPAWN_INTERVAL:
            self.weed_spawn_timer = 0
            self._spawn_weed()

    def render(self, surface):
        """Render game to surface

        Args:
            surface: Pygame surface to render to
        """
        # Clear screen
        surface.fill((0, 0, 0))

        # Render grid using renderer
        self.grid_renderer.render(surface, self.grid, TILE_SIZE, self.camera_offset)
        
        # Render player using renderer
        self.player_renderer.render(surface, self.player, TILE_SIZE, self.camera_offset)
        
        # Render purchasable tile highlights
        purchasable_tiles = self._get_all_purchasable_tiles()
        for i, (tile_x, tile_y) in enumerate(purchasable_tiles):
            is_selected = (i == self.ui.get_selected_index())
            self.ui.render_tile_highlight(surface, tile_x, tile_y, TILE_SIZE, self.camera_offset, is_selected)
        
        # Render chop cooldown indicator using renderer
        self.player_renderer.render_cooldown(surface, self.player, TILE_SIZE, self.camera_offset)
        
        # Render UI/HUD
        money = self.economy.get_money_display()
        income_rate = self.economy.get_income_rate()
        owned_tiles = self.economy.get_owned_tile_count()
        self.ui.render_hud(surface, money, income_rate, owned_tiles)
        
        # Render purchase UI if tiles available
        if purchasable_tiles:
            cost = self.economy.get_next_tile_cost()
            can_afford = self.economy.can_afford_tile()
            self.ui.render_purchase_ui(surface, purchasable_tiles, cost, can_afford, INTERNAL_HEIGHT)

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
            self.grid.get_tile(x, y).tile_type = TileType.WEED

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
