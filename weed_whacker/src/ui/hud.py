"""
Weed Whacker - HUD and UI Rendering
"""

import pygame # type: ignore


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
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

    def render_hud(self, surface, money, income_rate, owned_tiles, player=None, asset_manager=None):
        """Render the HUD with panels at top of screen

        Args:
            surface: Pygame surface to render to
            money: Current money (integer)
            income_rate: Income per second (float)
            owned_tiles: Total owned tiles
            player: Player instance (for tool info)
            asset_manager: AssetManager instance (for tool sprite)
        """
        # HUD styling
        panel_bg = (40, 40, 50, 200)  # Semi-transparent dark background
        panel_border = (80, 80, 100)
        text_color = (255, 255, 255)
        text_shadow = (0, 0, 0)
        label_color = (180, 180, 200)
        
        margin = 12
        panel_padding = 8
        panel_spacing = 6  # Small gap between stacked panels
        y_pos = margin
        
        # === MONEY PANEL (top left) ===
        money_panel_x = margin
        money_text = f"${money}"
        income_text = f"+${income_rate:.2f}/sec"
        
        money_surface = self.font.render(money_text, True, text_color)
        income_surface = self.font_small.render(income_text, True, (100, 255, 100))
        
        money_panel_width = max(money_surface.get_width(), income_surface.get_width()) + panel_padding * 2 + 64
        money_panel_height = money_surface.get_height() + income_surface.get_height() + panel_padding * 2 + 2
        
        self._draw_panel(surface, money_panel_x, y_pos, money_panel_width, money_panel_height, panel_bg, panel_border)
        
        # Money icon (gold coin)
        coin_x = money_panel_x + panel_padding + 8
        coin_y = y_pos + money_panel_height // 2
        pygame.draw.circle(surface, (255, 215, 0), (coin_x, coin_y), 10)
        pygame.draw.circle(surface, (200, 150, 0), (coin_x, coin_y), 10, 2)
        pygame.draw.circle(surface, (255, 235, 100), (coin_x - 2, coin_y - 2), 3)
        
        # Money text with shadow
        text_x = coin_x + 16
        text_y = y_pos + panel_padding
        surface.blit(self.font.render(money_text, True, text_shadow), (text_x + 1, text_y + 1))
        surface.blit(money_surface, (text_x, text_y))
        
        # Income text
        surface.blit(income_surface, (text_x, text_y + money_surface.get_height() + 2))
        
        # === TILES PANEL (below money, vertically stacked) ===
        tiles_panel_x = money_panel_x  # Same x position as money panel
        tiles_panel_y = y_pos + money_panel_height + panel_spacing  # Below money with small gap
        tiles_label = str(owned_tiles)
        tiles_text = "Owned Tiles"
        
        tiles_label_surface = self.font.render(tiles_label, True, text_color)
        tiles_surface = self.font_small.render(tiles_text, True, label_color)
        
        tiles_panel_width = money_panel_width  # Match money panel width
        tiles_panel_height = money_panel_height  # Match money panel height
        
        self._draw_panel(surface, tiles_panel_x, tiles_panel_y, tiles_panel_width, tiles_panel_height, panel_bg, panel_border)
        
        # Tile icon (grass square with detail)
        tile_icon_x = tiles_panel_x + panel_padding + 8
        tile_icon_y = tiles_panel_y + tiles_panel_height // 2 - 8
        pygame.draw.rect(surface, (80, 180, 80), (tile_icon_x, tile_icon_y, 16, 16))
        pygame.draw.rect(surface, (100, 220, 100), (tile_icon_x, tile_icon_y, 16, 16), 2)
        pygame.draw.line(surface, (60, 140, 60), (tile_icon_x + 4, tile_icon_y + 8), (tile_icon_x + 12, tile_icon_y + 8), 1)
        pygame.draw.line(surface, (60, 140, 60), (tile_icon_x + 8, tile_icon_y + 4), (tile_icon_x + 8, tile_icon_y + 12), 1)
        
        # Tiles text
        text_x = tile_icon_x + 20
        text_y = tiles_panel_y + panel_padding
        surface.blit(tiles_label_surface, (text_x, text_y))
        surface.blit(tiles_surface, (text_x, text_y + tiles_label_surface.get_height() + 2))
        
        # === TOOL PANEL (right side, spans full height of money + tiles + gap) ===
        if player and asset_manager:
            from ..game.tools import get_tool
            from ...config import TILE_SIZE
            
            tool = get_tool(player.current_tool)
            
            # Tool panel positioned to right of money/tiles stack
            tool_panel_x = money_panel_x + money_panel_width + 10
            tool_panel_y = y_pos
            
            # Calculate total height: money + gap + tiles
            total_left_height = money_panel_height + panel_spacing + tiles_panel_height
            
            # Tool panel dimensions
            tool_panel_width = 260  # Wider to accommodate larger icon and text
            tool_panel_height = total_left_height  # Spans full height of left panels
            
            self._draw_panel(surface, tool_panel_x, tool_panel_y, tool_panel_width, tool_panel_height, panel_bg, panel_border)
            
            # Tool icon - scale to fill panel height snugly (with small padding)
            icon_size = tool_panel_height - (panel_padding * 2)  # Fill height minus padding top/bottom
            icon_x = tool_panel_x + panel_padding
            icon_y = tool_panel_y + panel_padding
            
            # Load tool sprite at original high resolution for crisp rendering
            from pathlib import Path
            tool_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'sprites' / 'tools' / f'{player.current_tool}.png'
            
            if tool_sprite_path.exists():
                # Load original high-res PNG
                original_sprite = pygame.image.load(str(tool_sprite_path))
                # Convert with alpha to preserve transparency
                original_sprite = original_sprite.convert_alpha()
                # Scale down from original for crisp rendering
                scaled_sprite = pygame.transform.smoothscale(original_sprite, (icon_size, icon_size))
                surface.blit(scaled_sprite, (icon_x, icon_y))
            else:
                # Fallback: try asset manager or draw simple icon
                tool_sprite = asset_manager.get_sprite(player.current_tool)
                if tool_sprite:
                    scaled_sprite = pygame.transform.smoothscale(tool_sprite, (icon_size, icon_size))
                    surface.blit(scaled_sprite, (icon_x, icon_y))
                else:
                    fallback_size = icon_size // 2
                    pygame.draw.rect(surface, (150, 150, 150), (icon_x + icon_size//4, icon_y + icon_size//4, fallback_size, fallback_size))
            
            # Tool name
            tool_name_surface = self.font.render(tool.name, True, text_color)
            text_x = icon_x + icon_size + 10
            text_y = tool_panel_y + panel_padding + 4
            surface.blit(self.font.render(tool.name, True, text_shadow), (text_x + 1, text_y + 1))
            surface.blit(tool_name_surface, (text_x, text_y))
            
            # Cooldown bar (wider to fit nicely in panel)
            bar_x = text_x
            bar_y = text_y + tool_name_surface.get_height() + 6
            bar_width = tool_panel_width - (text_x - tool_panel_x) - panel_padding
            bar_height = 12
            
            # Cooldown percentage
            cooldown_percent = player.get_chop_cooldown_percent()
            
            # Bar background with border
            pygame.draw.rect(surface, (20, 20, 30), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(surface, (60, 60, 80), (bar_x, bar_y, bar_width, bar_height), 1)
            
            # Fill bar
            if cooldown_percent > 0:
                # Cooling down - red
                fill_color = (220, 80, 60)
                fill_width = int(bar_width * cooldown_percent)
            else:
                # Ready - bright green
                fill_color = (80, 220, 80)
                fill_width = bar_width
            
            if fill_width > 0:
                pygame.draw.rect(surface, fill_color, (bar_x + 1, bar_y + 1, fill_width - 2, bar_height - 2))
                # Add highlight for 3D effect
                highlight_color = tuple(min(255, c + 40) for c in fill_color)
                pygame.draw.rect(surface, highlight_color, (bar_x + 1, bar_y + 1, fill_width - 2, 2))
            
            # Tool usage counter below cooldown bar
            usage_text = f"Tool Used: {player.tool_uses}"
            usage_surface = self.font_small.render(usage_text, True, label_color)
            usage_y = bar_y + bar_height + 6
            surface.blit(usage_surface, (text_x, usage_y))

    def _draw_panel(self, surface, x, y, width, height, bg_color, border_color):
        """Draw a panel with background and border
        
        Args:
            surface: Surface to draw on
            x, y: Position
            width, height: Dimensions
            bg_color: Background RGBA color
            border_color: Border RGB color
        """
        # Create semi-transparent panel surface
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill(bg_color)
        surface.blit(panel, (x, y))
        
        # Draw border
        pygame.draw.rect(surface, border_color, (x, y, width, height), 2)
        
        # Draw subtle inner highlight
        pygame.draw.line(surface, (100, 100, 120), (x + 2, y + 2), (x + width - 2, y + 2), 1)
    
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
