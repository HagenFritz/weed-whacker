"""
Weed Whacker - HUD and UI Rendering
"""

import pygame # type: ignore
from pathlib import Path
from ..constants.colors import (
    PANEL_BG, PANEL_BORDER, UI_TEXT, UI_TEXT_SHADOW, UI_LABEL,
    COOLDOWN_COOLING, COOLDOWN_READY,
    AFFORDABLE, AFFORDABLE_DARK, UNAFFORDABLE, UNAFFORDABLE_DARK,
    HIGHLIGHT_ACTIVE, HIGHLIGHT_INACTIVE,
    FALLBACK_ICON, BAR_BG, BAR_BORDER,
    STORE_ICON_FALLBACK, STORE_INSTRUCTION, INNER_HIGHLIGHT,
    WHITE
)


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

    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within a specific width
        
        Args:
            text: String to wrap
            font: Pygame font object
            max_width: Maximum width in pixels
            
        Returns:
            List of strings, each fitting within max_width
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            width, _ = font.size(test_line)
            
            if width > max_width:
                # Word is too long, push it to the next line
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is longer than max_width, just add it
                    lines.append(' '.join(current_line))
                    current_line = []
                    
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines

    def render_hud(self, surface, money, income_rate, owned_tiles, player, asset_manager=None, event_manager=None, internal_width=0):
        """Render the heads-up display
        
        Args:
            surface: Pygame surface to render to
            money: Current money (integer)
            income_rate: Income per second (float)
            owned_tiles: Total owned tiles
            player: Player instance (for tool info)
            asset_manager: AssetManager instance (for tool sprite)
            event_manager: EventManager instance (for event info)
            internal_width: Screen width
        """
        # HUD styling
        panel_bg = PANEL_BG
        panel_border = PANEL_BORDER
        text_color = UI_TEXT
        text_shadow = UI_TEXT_SHADOW
        label_color = UI_LABEL
        
        margin = 12
        panel_padding = 8
        panel_spacing = 6  # Small gap between stacked panels
        y_pos = margin
        
        # === MONEY PANEL (top left) ===
        money_panel_x = margin
        money_text = f"${int(money)}"
        income_text = f"+${income_rate:.2f}/sec"
        
        money_surface = self.font.render(money_text, True, text_color)
        income_surface = self.font_small.render(income_text, True, AFFORDABLE)
        
        money_panel_width = max(money_surface.get_width(), income_surface.get_width()) + panel_padding * 2 + 64
        money_panel_height = money_surface.get_height() + income_surface.get_height() + panel_padding * 2 + 2
        
        self._draw_panel(surface, money_panel_x, y_pos, money_panel_width, money_panel_height, panel_bg, panel_border)
        
        # Money icon (gold coin)
        assets_dir = Path(__file__).parent.parent.parent / 'assets' / 'sprites' / 'objects'
        coin_path = assets_dir / 'coin.png'
        
        icon_size = 36 
        coin_x = money_panel_x + panel_padding + 8
        coin_y = y_pos + (money_panel_height - icon_size) // 2
        
        if coin_path.exists():
            original_coin = pygame.image.load(str(coin_path)).convert_alpha()
            scaled_coin = pygame.transform.smoothscale(original_coin, (icon_size, icon_size))
            surface.blit(scaled_coin, (coin_x, coin_y))
        
        # Money text with shadow (aligned with tiles text)
        text_x = coin_x + icon_size + 12
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
        
        # Tile icon
        tile_path = assets_dir / 'tile.png'
        tile_icon_x = tiles_panel_x + panel_padding + 8
        tile_icon_y = tiles_panel_y + (tiles_panel_height - icon_size) // 2
        
        if tile_path.exists():
            original_tile = pygame.image.load(str(tile_path)).convert_alpha()
            scaled_tile = pygame.transform.smoothscale(original_tile, (icon_size, icon_size))
            surface.blit(scaled_tile, (tile_icon_x, tile_icon_y))
        
        # Tiles text
        text_x = tile_icon_x + icon_size + 12
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
            tool_panel_width = 300  # Wider to accommodate inventory instruction
            tool_panel_height = total_left_height  # Spans full height of left panels
            
            self._draw_panel(surface, tool_panel_x, tool_panel_y, tool_panel_width, tool_panel_height, panel_bg, panel_border)
            
            # Tool icon - scale to fill panel height snugly (with small padding)
            icon_size = tool_panel_height - (panel_padding * 2) - 20  # Make room for instruction text at bottom
            icon_x = tool_panel_x + panel_padding
            icon_y = tool_panel_y + panel_padding
            
            # Load tool sprite at original high resolution for crisp rendering
            tool_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'sprites' / 'tools' / f'{player.current_tool}.png'
            
            if tool_sprite_path.exists():
                # Load original high-res PNG
                original_sprite = pygame.image.load(str(tool_sprite_path)).convert_alpha()
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
                    pygame.draw.rect(surface, FALLBACK_ICON, (icon_x + icon_size//4, icon_y + icon_size//4, fallback_size, fallback_size))
            
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
            pygame.draw.rect(surface, BAR_BG, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(surface, BAR_BORDER, (bar_x, bar_y, bar_width, bar_height), 1)
            
            # Fill bar
            if cooldown_percent > 0:
                # Cooling down - red
                fill_color = COOLDOWN_COOLING
                fill_width = int(bar_width * cooldown_percent)
            else:
                # Ready - bright green
                fill_color = COOLDOWN_READY
                fill_width = bar_width
            
            if fill_width > 0:
                pygame.draw.rect(surface, fill_color, (bar_x + 1, bar_y + 1, fill_width - 2, bar_height - 2))
                # Add highlight for 3D effect
                highlight_color = tuple(min(255, c + 40) for c in fill_color)
                pygame.draw.rect(surface, highlight_color, (bar_x + 1, bar_y + 1, fill_width - 2, 2))
            
            # Tool usage counter below cooldown bar
            current_uses = player.tool_uses.get(player.current_tool, 0)
            usage_text = f"Tool Used: {current_uses}"
            usage_surface = self.font_small.render(usage_text, True, label_color)
            usage_y = bar_y + bar_height + 6
            surface.blit(usage_surface, (text_x, usage_y))
            
            # Inventory Instruction Text
            inv_inst_text = "Press 'I' to open your inventory"
            inv_inst_surface = self.font_small.render(inv_inst_text, True, STORE_INSTRUCTION)
            inst_x = tool_panel_x + (tool_panel_width - inv_inst_surface.get_width()) // 2
            inst_y = tool_panel_y + tool_panel_height - inv_inst_surface.get_height() - panel_padding + 4
            surface.blit(inv_inst_surface, (inst_x, inst_y))
            
        # === EVENT PANEL (top right) ===
        if event_manager and internal_width > 0:
            current_event = event_manager.current_event
            
            # Event panel dimensions
            event_panel_width = 280
            
            # Text surfaces
            title_surface = self.font.render(current_event.name, True, text_color)
            
            # Prepare description lines
            desc_max_width = event_panel_width - (panel_padding * 2)
            desc_lines = self._wrap_text(current_event.description, self.font_small, desc_max_width)
            
            # Text height (title + gap + bar)
            bar_height = 12
            top_area_height = title_surface.get_height() + 6 + bar_height
            
            # Icon dimensions
            icon_size = 48
            
            # Calculate height needed for the top area (icon vs text)
            top_section_height = max(icon_size, top_area_height)
            
            # Calculate height needed for description
            desc_line_height = self.font_small.get_linesize()
            desc_total_height = len(desc_lines) * desc_line_height
            
            # Total panel height (padding + top section + gap + desc section + padding)
            desc_gap = 10
            event_panel_height = panel_padding + top_section_height + desc_gap + desc_total_height + panel_padding
            
            event_panel_x = internal_width - event_panel_width - margin
            event_panel_y = margin
            
            self._draw_panel(surface, event_panel_x, event_panel_y, event_panel_width, event_panel_height, panel_bg, panel_border)
            
            # Draw Event Icon
            event_icon_x = event_panel_x + panel_padding
            event_icon_y = event_panel_y + panel_padding
            
            # Try to load the event icon
            event_icon_path = Path(__file__).parent.parent.parent / 'assets' / 'sprites' / 'events' / f'{current_event.icon_name}.png'
            
            if event_icon_path.exists():
                original_icon = pygame.image.load(str(event_icon_path)).convert_alpha()
                scaled_icon = pygame.transform.smoothscale(original_icon, (icon_size, icon_size))
                surface.blit(scaled_icon, (event_icon_x, event_icon_y))
            else:
                # Placeholder for icon if missing
                pygame.draw.rect(surface, FALLBACK_ICON, (event_icon_x, event_icon_y, icon_size, icon_size), border_radius=8)
            
            # Draw Texts
            text_x = event_icon_x + icon_size + 12
            start_text_y = event_panel_y + panel_padding
            
            # Title
            surface.blit(self.font.render(current_event.name, True, text_shadow), (text_x + 1, start_text_y + 1))
            surface.blit(title_surface, (text_x, start_text_y))
            
            # Cooldown bar
            bar_y = start_text_y + title_surface.get_height() + 6
            bar_width = event_panel_width - (text_x - event_panel_x) - panel_padding
            
            pygame.draw.rect(surface, BAR_BG, (text_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(surface, BAR_BORDER, (text_x, bar_y, bar_width, bar_height), 1)
            
            # If infinite (duration <= 0), show full bar (deactivated state)
            if current_event.duration <= 0:
                fill_color = (100, 200, 255) # A nice deactivated/infinite color
                pygame.draw.rect(surface, fill_color, (text_x + 1, bar_y + 1, bar_width - 2, bar_height - 2))
                highlight_color = tuple(min(255, c + 40) for c in fill_color)
                pygame.draw.rect(surface, highlight_color, (text_x + 1, bar_y + 1, bar_width - 2, 2))
            else:
                progress = event_manager.get_progress_percent()
                if progress > 0:
                    fill_color = COOLDOWN_COOLING
                    fill_width = int(bar_width * progress)
                    pygame.draw.rect(surface, fill_color, (text_x + 1, bar_y + 1, fill_width - 2, bar_height - 2))
                    highlight_color = tuple(min(255, c + 40) for c in fill_color)
                    pygame.draw.rect(surface, highlight_color, (text_x + 1, bar_y + 1, fill_width - 2, 2))
            
            # Draw Description lines below everything else
            desc_y = event_panel_y + panel_padding + top_section_height + desc_gap
            for line in desc_lines:
                desc_surface = self.font_small.render(line, True, label_color)
                surface.blit(desc_surface, (event_panel_x + panel_padding, desc_y))
                desc_y += desc_line_height

    def _draw_panel(self, surface, x, y, width, height, bg_color, border_color):
        """Draw a panel with background and border
        
        Args:
            surface: Surface to draw on
            x, y: Top-left coordinates
            width, height: Dimensions
            bg_color: Fill color
            border_color: Border color
        """
        # Create semi-transparent panel surface
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill(bg_color)
        surface.blit(panel, (x, y))
        
        # Draw border
        pygame.draw.rect(surface, border_color, (x, y, width, height), 2)
        
        # Draw subtle inner highlight
        pygame.draw.line(surface, INNER_HIGHLIGHT, (x + 2, y + 2), (x + width - 2, y + 2), 1)

    def render_purchase_ui(self, surface, purchasable_tiles, cost, can_afford, internal_width, internal_height):
        """Render purchase UI with tile selection

        Args:
            surface: Pygame surface to render to
            purchasable_tiles: List of (x, y) purchasable tile coordinates
            cost: Cost of next tile
            can_afford: Whether player can afford
            internal_width: Screen width for positioning
            internal_height: Screen height for positioning
        """
        if not purchasable_tiles:
            return
        
        # Ensure selected index is valid
        if self.selected_purchase_index >= len(purchasable_tiles):
            self.selected_purchase_index = 0
            
        # HUD styling matching the top panels
        panel_bg = PANEL_BG
        panel_border = PANEL_BORDER
        text_color = UI_TEXT
        text_shadow = UI_TEXT_SHADOW
        label_color = UI_LABEL
        
        # Determine colors based on affordability
        if can_afford:
            cost_color = AFFORDABLE
            icon_color = AFFORDABLE_DARK
        else:
            cost_color = UNAFFORDABLE
            icon_color = UNAFFORDABLE_DARK
            
        # Create text surfaces
        action_text = "Buy Land"
        action_surface = self.font.render(action_text, True, text_color)
        
        cost_text = f"${cost}"
        cost_surface = self.font.render(cost_text, True, cost_color)
        
        if len(purchasable_tiles) > 1:
            instruction_text = f"Press B to buy • Tab to cycle ({self.selected_purchase_index + 1}/{len(purchasable_tiles)})"
        else:
            instruction_text = "Press B to buy"
            
        instruction_surface = self.font_small.render(instruction_text, True, label_color)
        
        # Calculate panel dimensions
        panel_padding = 12
        icon_size = 24
        
        # Width needs to accommodate the longest element
        top_row_width = icon_size + 10 + action_surface.get_width() + 8 + cost_surface.get_width()
        text_width = max(
            top_row_width,
            instruction_surface.get_width()
        )
        
        panel_width = text_width + (panel_padding * 2)
        panel_height = action_surface.get_height() + instruction_surface.get_height() + (panel_padding * 2) + 4
        
        # Position at bottom center
        panel_x = (internal_width - panel_width) // 2
        panel_y = internal_height - panel_height - 20
        
        # Draw the panel background and border
        self._draw_panel(surface, panel_x, panel_y, panel_width, panel_height, panel_bg, panel_border)
        
        # Draw icon (a stylized 'plus' or 'land' icon)
        icon_x = panel_x + panel_padding
        icon_y = panel_y + panel_padding
        
        # Draw a little land/plus icon
        pygame.draw.rect(surface, icon_color, (icon_x, icon_y, icon_size, icon_size), border_radius=4)
        pygame.draw.rect(surface, WHITE, (icon_x, icon_y, icon_size, icon_size), 2, border_radius=4)
        # Plus sign inside
        pygame.draw.line(surface, WHITE, (icon_x + 6, icon_y + 12), (icon_x + 18, icon_y + 12), 2)
        pygame.draw.line(surface, WHITE, (icon_x + 12, icon_y + 6), (icon_x + 12, icon_y + 18), 2)
        
        # Draw text
        text_x = icon_x + icon_size + 10
        text_y = panel_y + panel_padding + (icon_size - action_surface.get_height()) // 2
        
        # Action text with shadow
        surface.blit(self.font.render(action_text, True, text_shadow), (text_x + 1, text_y + 1))
        surface.blit(action_surface, (text_x, text_y))
        
        # Cost text next to action text
        cost_x = text_x + action_surface.get_width() + 8
        surface.blit(self.font.render(cost_text, True, text_shadow), (cost_x + 1, text_y + 1))
        surface.blit(cost_surface, (cost_x, text_y))
        
        # Instruction text below
        inst_x = panel_x + (panel_width - instruction_surface.get_width()) // 2
        inst_y = panel_y + panel_padding + max(icon_size, action_surface.get_height()) + 4
        surface.blit(instruction_surface, (inst_x, inst_y))

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
            color = HIGHLIGHT_ACTIVE
            thickness = 2
        else:
            color = HIGHLIGHT_INACTIVE
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
