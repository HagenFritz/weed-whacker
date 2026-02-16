"""
Weed Whacker - Main Game State and Loop Logic
"""

import pygame
from .grid import Grid
from ..config import (
    TILE_SIZE,
    INTERNAL_WIDTH,
    INTERNAL_HEIGHT,
    STARTING_GRID_SIZE,
    WORLD_GRID_SIZE
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
        
        # TODO: Initialize player, economy, UI

    def handle_event(self, event):
        """Handle pygame events"""
        # TODO: Pass events to relevant systems (player input, etc.)
        pass

    def update(self, dt):
        """Update game state

        Args:
            dt: Delta time in milliseconds since last frame
        """
        # TODO: Update player, grid, economy, spawn weeds
        pass

    def render(self, surface):
        """Render game to surface

        Args:
            surface: Pygame surface to render to
        """
        # Clear screen
        surface.fill((0, 0, 0))

        # Render grid
        self.grid.render(surface, TILE_SIZE, self.camera_offset)
        
        # TODO: Render player, UI
