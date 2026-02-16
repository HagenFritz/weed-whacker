"""
Weed Whacker - HUD and UI Rendering
"""

import pygame


class UI:
    """Handles HUD rendering and display"""

    def __init__(self):
        """Initialize UI"""
        self.font = None
        self.selected_purchase_index = 0
        self._init_font()

    def _init_font(self):
        """Initialize font for rendering text"""
        if not hasattr(pygame.font, '_initialized') or not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(None, 16)

    def render_hud(self, surface, money, income_rate, owned_tiles):
        """Render the compact HUD at top of screen

        Args:
            surface: Pygame surface to render to
            money: Current money (integer)
            income_rate: Income per second (float)
            owned_tiles: Total owned tiles
        """
        # Colors
        text_color = (255, 255, 255)
        icon_color = (255, 215, 0)
        tile_color = (100, 200, 100)
        
        # Position
        y_pos = 3
        x_margin = 3
        icon_size = 8
        
        # Money icon (simple coin shape)
        pygame.draw.circle(surface, icon_color, (x_margin + icon_size // 2, y_pos + icon_size // 2), icon_size // 2)
        pygame.draw.circle(surface, (200, 160, 0), (x_margin + icon_size // 2, y_pos + icon_size // 2), icon_size // 2, 1)
        
        # Money text: $X ($Y/sec)
        money_text = f"${money} (${income_rate:.2f}/sec)"
        money_surface = self.font.render(money_text, True, text_color)
        surface.blit(money_surface, (x_margin + icon_size + 3, y_pos))
        
        # Tiles icon (simple square)
        tile_icon_x = x_margin + 150
        pygame.draw.rect(surface, tile_color, (tile_icon_x, y_pos + 1, icon_size, icon_size))
        pygame.draw.rect(surface, (60, 120, 60), (tile_icon_x, y_pos + 1, icon_size, icon_size), 1)
        
        # Tiles text: just total count
        tiles_text = f"{owned_tiles}"
        tiles_surface = self.font.render(tiles_text, True, text_color)
        surface.blit(tiles_surface, (tile_icon_x + icon_size + 3, y_pos))

    def render_purchase_ui(self, surface, purchasable_tiles, cost, can_afford, internal_height):
        """Render purchase UI with tile selection

        Args:
            surface: Pygame surface to render to
            purchasable_tiles: List of (x, y) purchasable tile coordinates
            cost: Cost of next tile
            can_afford: Whether player can afford
            internal_height: Screen height for positioning
        """
        if not purchasable_tiles:
            return
        
        # Ensure selected index is valid
        if self.selected_purchase_index >= len(purchasable_tiles):
            self.selected_purchase_index = 0
        
        # Render purchase prompt at bottom
        x_margin = 3
        cost_color = (50, 255, 50) if can_afford else (255, 50, 50)
        
        # Show which tile is selected if multiple options
        if len(purchasable_tiles) > 1:
            cost_text = f"Press B to buy tile: ${cost} ({self.selected_purchase_index + 1}/{len(purchasable_tiles)}) [Tab: cycle]"
        else:
            cost_text = f"Press B to buy tile: ${cost}"
        
        cost_surface = self.font.render(cost_text, True, cost_color)
        surface.blit(cost_surface, (x_margin, internal_height - 14))

    def render_tile_highlight(self, surface, tile_x, tile_y, tile_size, camera_offset, is_selected):
        """Render highlight on purchasable tiles

        Args:
            surface: Pygame surface to render to
            tile_x, tile_y: Tile grid coordinates
            tile_size: Size of tiles in pixels
            camera_offset: Camera offset tuple (x, y)
            is_selected: Whether this is the currently selected tile
        """
        screen_x = tile_x * tile_size - camera_offset[0]
        screen_y = tile_y * tile_size - camera_offset[1]
        
        # Highlight color - brighter if selected
        if is_selected:
            color = (255, 255, 100)
            thickness = 2
        else:
            color = (150, 150, 80)
            thickness = 1
        
        # Draw highlight border
        pygame.draw.rect(surface, color, (screen_x, screen_y, tile_size, tile_size), thickness)

    def cycle_selected_tile(self, direction, max_tiles):
        """Cycle through purchasable tiles

        Args:
            direction: 1 for next, -1 for previous
            max_tiles: Total number of purchasable tiles
        """
        if max_tiles == 0:
            self.selected_purchase_index = 0
            return
        
        self.selected_purchase_index = (self.selected_purchase_index + direction) % max_tiles

    def reset_selection(self):
        """Reset tile selection to first tile"""
        self.selected_purchase_index = 0

    def get_selected_index(self):
        """Get current selected tile index"""
        return self.selected_purchase_index
