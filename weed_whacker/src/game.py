"""
Weed Whacker - Main Game State and Loop Logic
"""

import pygame
from .grid import Grid
from .player import Player
from ..config import (
    TILE_SIZE,
    INTERNAL_WIDTH,
    INTERNAL_HEIGHT,
    STARTING_GRID_SIZE,
    WORLD_GRID_SIZE,
    PLAYER_MOVE_COOLDOWN,
    CHOP_COOLDOWN
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
        
        # TODO: Initialize economy, UI

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
        
        # TODO: Update economy, spawn weeds

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
        
        # TODO: Render UI
