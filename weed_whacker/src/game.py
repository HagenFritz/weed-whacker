"""
Weed Whacker - Main Game State and Loop Logic
"""

import pygame
import random
from .grid import Grid, TileType
from .player import Player
from .economy import Economy
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
        
        # TODO: Initialize UI

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
                self._try_purchase_adjacent_tile()
        
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

        # Render grid
        self.grid.render(surface, TILE_SIZE, self.camera_offset)
        
        # Render player
        self.player.render(surface, TILE_SIZE, self.camera_offset)
        
        # Render chop cooldown indicator near player
        self._render_chop_cooldown(surface)
        
        # Render UI
        self._render_ui(surface)

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

    def _render_chop_cooldown(self, surface):
        """Render the chop cooldown indicator near the player
        
        Args:
            surface: Pygame surface to render to
        """
        # Get cooldown percentage (0.0 = ready, 1.0 = just chopped)
        cooldown_percent = self.player.chop_cooldown / CHOP_COOLDOWN if self.player.chop_cooldown > 0 else 0.0
        
        # Calculate player screen position
        player_screen_x = self.player.x * TILE_SIZE - self.camera_offset[0]
        player_screen_y = self.player.y * TILE_SIZE - self.camera_offset[1]
        
        # Draw cooldown bar below the player
        bar_width = TILE_SIZE - 4
        bar_height = 3
        bar_x = player_screen_x + 2
        bar_y = player_screen_y + TILE_SIZE + 1
        
        # Background (empty bar)
        bg_color = (60, 60, 60)
        pygame.draw.rect(surface, bg_color, (bar_x, bar_y, bar_width, bar_height))
        
        # Foreground (filled portion based on cooldown)
        if cooldown_percent > 0:
            # Red when cooling down
            fill_color = (200, 50, 50)
            fill_width = int(bar_width * (1.0 - cooldown_percent))
        else:
            # Green when ready
            fill_color = (50, 200, 50)
            fill_width = bar_width
        
        if fill_width > 0:
            pygame.draw.rect(surface, fill_color, (bar_x, bar_y, fill_width, bar_height))

    def _render_ui(self, surface):
        """Render the UI/HUD displaying game stats
        
        Args:
            surface: Pygame surface to render to
        """
        # Initialize font if needed
        if not hasattr(pygame.font, '_initialized') or not pygame.font.get_init():
            pygame.font.init()
        
        # Use default font, small size
        font = pygame.font.Font(None, 20)
        
        # Get stats
        money = self.economy.get_money_display()
        income_rate = self.economy.get_income_rate()
        owned_tiles = self.economy.get_owned_tile_count()
        grass_tiles = self.grid.count_tiles_by_type(TileType.GRASS)
        weed_tiles = self.grid.count_tiles_by_type(TileType.WEED)
        
        # Text color
        text_color = (255, 255, 255)
        
        # Position for UI elements at top of screen
        y_pos = 4
        x_margin = 4
        
        # Money display
        money_text = f"Money: ${money}"
        money_surface = font.render(money_text, True, text_color)
        surface.blit(money_surface, (x_margin, y_pos))
        
        # Income rate display
        income_text = f"Income: ${income_rate}/sec"
        income_surface = font.render(income_text, True, text_color)
        surface.blit(income_surface, (x_margin + 100, y_pos))
        
        # Tile count display
        tiles_text = f"Tiles: {owned_tiles} ({grass_tiles} grass, {weed_tiles} weeds)"
        tiles_surface = font.render(tiles_text, True, text_color)
        surface.blit(tiles_surface, (x_margin, y_pos + 16))
        
        # Purchase cost display if on border facing unowned tile
        purchasable_tile = self._get_purchasable_tile()
        if purchasable_tile:
            cost = self.economy.get_next_tile_cost()
            can_afford = self.economy.can_afford_tile()
            cost_color = (50, 255, 50) if can_afford else (255, 50, 50)
            cost_text = f"Press B to buy tile: ${cost}"
            cost_surface = font.render(cost_text, True, cost_color)
            # Position at bottom of screen
            surface.blit(cost_surface, (x_margin, INTERNAL_HEIGHT - 20))

    def _get_purchasable_tile(self):
        """Get the coordinates of a purchasable tile adjacent to the player
        
        Returns:
            Tuple (x, y) of purchasable tile, or None if no valid tile
        """
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
                    return (tile_x, tile_y)
        
        return None

    def _try_purchase_adjacent_tile(self):
        """Attempt to purchase a tile adjacent to the player"""
        purchasable_tile = self._get_purchasable_tile()
        if purchasable_tile:
            x, y = purchasable_tile
            success = self.economy.try_purchase_tile(x, y)
            if success:
                pass  # Could add success feedback/sound here
