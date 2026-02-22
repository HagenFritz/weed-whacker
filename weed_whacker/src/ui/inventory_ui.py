"""
Weed Whacker - Inventory UI
Handles the rendering and logic of the in-game inventory and store.
"""

import pygame # type: ignore
from pathlib import Path

from ..constants.colors import (
    PANEL_BG, PANEL_BORDER, UI_TEXT, UI_TEXT_SHADOW,
    OVERLAY_BG, PLACEHOLDER_TEXT, CLOSE_TEXT, WHITE
)

class InventoryUI:
    """Handles the Inventory UI rendering and interaction"""
    
    def __init__(self):
        """Initialize Inventory UI"""
        self.is_open = False
        self.font = None
        self.font_large = None
        self.font_small = None
        self.buttons = []  # Store clickable rects: [(rect, action, tool_key)]
        
        self.sort_by = "cost"
        self.sort_descending = False
        
        from .shared import Toast, ConfirmDialog
        self.toast = Toast()
        self.confirm_dialog = ConfirmDialog()
        
        self._init_fonts()
        
    def _init_fonts(self):
        """Initialize fonts for rendering text"""
        if not hasattr(pygame.font, '_initialized') or not pygame.font.get_init():
            pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
    def toggle(self):
        """Toggle inventory open/closed state"""
        self.is_open = not self.is_open
        
    def handle_click(self, mouse_pos, player, economy):
        """Handle mouse clicks when inventory is open"""
        if not self.is_open:
            return False
            
        if self.confirm_dialog.active:
            if self.confirm_dialog.handle_click(mouse_pos):
                return True
            
        for rect, action, tool_key in self.buttons:
            if rect.collidepoint(mouse_pos):
                if action == "equip":
                    player.current_tool = tool_key
                    return True
                elif action == "buy":
                    from ..game.tools import TOOLS
                    tool = TOOLS[tool_key]
                    if economy.money >= tool.cost:
                        economy.money -= tool.cost
                        player.owned_tools.append(tool_key)
                        player.current_tool = tool_key
                    else:
                        self.toast.show(f"Not enough money! Need ${tool.cost}", duration=2.0)
                    return True
                elif action == "sell":
                    if len(player.owned_tools) <= 1:
                        self.toast.show("Cannot sell your only tool!", duration=2.0)
                        return True
                        
                    from ..game.tools import TOOLS
                    tool = TOOLS[tool_key]
                    uses = player.tool_uses.get(tool_key, 0)
                    # Sell price = floor((cost / 2) * (1 - uses/longevity))
                    import math
                    if tool.longevity <= 0:
                        longevity_ratio = 1.0
                    else:
                        longevity_ratio = max(0, 1 - (uses / tool.longevity))
                    sell_price = math.floor((tool.cost / 2) * longevity_ratio)
                    
                    def on_sell_confirm():
                        economy.money += sell_price
                        player.owned_tools.remove(tool_key)
                        if player.current_tool == tool_key:
                            player.current_tool = player.owned_tools[0]
                            
                    self.confirm_dialog.show(f"Sell {tool.name} for ${sell_price}?", on_sell_confirm)
                    return True
                    
        return True # Handled click on UI (prevent propagating to game)
        
    def update(self):
        """Update active components like toasts"""
        self.toast.update()
        
    def render(self, surface, internal_width, internal_height, player, asset_manager):
        """Render the inventory dialog
        
        Args:
            surface: Pygame surface to render to
            internal_width: Screen width
            internal_height: Screen height
            player: Player instance
            asset_manager: AssetManager instance
        """
        if not self.is_open:
            return
            
        self.buttons.clear()
            
        # Dialog dimensions
        dialog_width = internal_width - 100
        dialog_height = internal_height - 100
        dialog_x = (internal_width - dialog_width) // 2
        dialog_y = (internal_height - dialog_height) // 2
        
        # Colors
        bg_color = PANEL_BG
        border_color = PANEL_BORDER
        text_color = UI_TEXT
        text_shadow = UI_TEXT_SHADOW
        
        # Create semi-transparent overlay for background
        overlay = pygame.Surface((internal_width, internal_height), pygame.SRCALPHA)
        overlay.fill(OVERLAY_BG)
        surface.blit(overlay, (0, 0))
        
        # Draw main dialog panel
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        dialog_surface.fill(bg_color)
        surface.blit(dialog_surface, (dialog_x, dialog_y))
        pygame.draw.rect(surface, border_color, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=8)
        
        # Title
        title_text = "Inventory & Store"
        title_surface = self.font_large.render(title_text, True, text_color)
        title_x = dialog_x + (dialog_width - title_surface.get_width()) // 2
        title_y = dialog_y + 20
        
        surface.blit(self.font_large.render(title_text, True, text_shadow), (title_x + 2, title_y + 2))
        surface.blit(title_surface, (title_x, title_y))
        
        # Render tools list
        from ..game.tools import TOOLS
        
        # Sort tools
        tools_list = list(TOOLS.items())
        if self.sort_by == "cost":
            tools_list.sort(key=lambda item: item[1].cost, reverse=self.sort_descending)
        elif self.sort_by == "cooldown":
            tools_list.sort(key=lambda item: item[1].cooldown, reverse=self.sort_descending)
        elif self.sort_by == "longevity":
            # For longevity, treat -1 (infinite) as infinity for sorting
            tools_list.sort(key=lambda item: float('inf') if item[1].longevity <= 0 else item[1].longevity, reverse=self.sort_descending)
            
        list_y = title_y + title_surface.get_height() + 50
        item_height = 80
        padding = 15
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Render Sort Controls
        sort_y = title_y + title_surface.get_height() + 10
        sort_label = self.font.render("Sort by:", True, text_color)
        surface.blit(sort_label, (dialog_x + padding, sort_y))
        
        sort_options = [("Cost", "cost"), ("Cooldown", "cooldown"), ("Longevity", "longevity")]
        sort_x = dialog_x + padding + sort_label.get_width() + 15
        
        for label, sort_key in sort_options:
            btn_rect = pygame.Rect(sort_x, sort_y - 2, 80, 24)
            is_hovered = btn_rect.collidepoint(mouse_pos)
            is_active = self.sort_by == sort_key
            
            # Handle click
            if is_hovered and pygame.mouse.get_pressed()[0]:
                if is_active:
                    self.sort_descending = not self.sort_descending
                else:
                    self.sort_by = sort_key
                    self.sort_descending = False
                    
                # Small delay to prevent multiple toggles
                pygame.time.wait(100)
                
            bg_color = (80, 100, 80) if is_active else ((60, 60, 80) if is_hovered else (40, 40, 50))
            pygame.draw.rect(surface, bg_color, btn_rect, border_radius=4)
            pygame.draw.rect(surface, WHITE if is_active else (150, 150, 150), btn_rect, 1, border_radius=4)
            
            # Add arrow if active
            display_label = label
            if is_active:
                display_label += " ↓" if self.sort_descending else " ↑"
                
            txt_color = WHITE if is_active else (200, 200, 200)
            txt_surface = self.font_small.render(display_label, True, txt_color)
            surface.blit(txt_surface, (sort_x + (80 - txt_surface.get_width()) // 2, sort_y + 4))
            
            sort_x += 90
        
        for tool_key, tool in tools_list:
            is_owned = tool_key in player.owned_tools
            is_equipped = tool_key == player.current_tool
            
            # Tool Item Background
            item_rect = (dialog_x + padding, list_y, dialog_width - (padding * 2), item_height)
            
            # Highlight if equipped
            if is_equipped:
                pygame.draw.rect(surface, (60, 70, 60), item_rect, border_radius=6)
                pygame.draw.rect(surface, (100, 255, 100), item_rect, 2, border_radius=6)
            else:
                pygame.draw.rect(surface, (40, 40, 50), item_rect, border_radius=6)
                pygame.draw.rect(surface, (80, 80, 100), item_rect, 1, border_radius=6)
            
            # Tool Icon
            icon_size = 48
            icon_x = dialog_x + padding + 15
            icon_y = list_y + (item_height - icon_size) // 2
            
            # Try to load sprite from asset manager or fallback to disk
            tool_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'sprites' / 'tools' / f'{tool.sprite_name}.png'
            if tool_sprite_path.exists():
                original_sprite = pygame.image.load(str(tool_sprite_path)).convert_alpha()
                scaled_sprite = pygame.transform.smoothscale(original_sprite, (icon_size, icon_size))
                surface.blit(scaled_sprite, (icon_x, icon_y))
            elif asset_manager:
                tool_sprite = asset_manager.get_sprite(tool.sprite_name)
                if tool_sprite:
                    scaled_sprite = pygame.transform.smoothscale(tool_sprite, (icon_size, icon_size))
                    surface.blit(scaled_sprite, (icon_x, icon_y))
                else:
                    pygame.draw.rect(surface, (150, 150, 150), (icon_x, icon_y, icon_size, icon_size))
            
            # Tool Info
            info_x = icon_x + icon_size + 20
            
            # Name and Cost
            name_surface = self.font.render(tool.name, True, text_color)
            surface.blit(name_surface, (info_x, list_y + 10))
            
            cost_text = f"Cost: ${tool.cost}" if not is_owned and tool.cost > 0 else "Owned"
            cost_color = (100, 255, 100) if not is_owned and tool.cost > 0 else (150, 150, 150)
            cost_surface = self.font.render(cost_text, True, cost_color)
            surface.blit(cost_surface, (info_x + name_surface.get_width() + 20, list_y + 10))
            
            # Description
            desc_surface = self.font_small.render(tool.description, True, (200, 200, 200))
            surface.blit(desc_surface, (info_x, list_y + 35))
            
            # Stats (Efficiency, Cooldown, Longevity)
            durability_text = f"{tool.longevity} uses" if tool.longevity > 0 else "Infinite"
            stats_text = f"Efficiency: {tool.efficiency}x  |  Cooldown: {tool.cooldown / 1000.0}s  |  Durability: {durability_text}"
            stats_surface = self.font_small.render(stats_text, True, (150, 200, 255))
            surface.blit(stats_surface, (info_x, list_y + 55))
            
            # Buttons
            btn_width = 80
            btn_height = 30
            btn_x = dialog_x + dialog_width - padding - btn_width - 10
            btn_y = list_y + (item_height - btn_height) // 2
            
            btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
            is_hovered = btn_rect.collidepoint(mouse_pos)
            
            # Additional Sell Button (Left of action button)
            sell_btn_width = 100
            sell_btn_x = btn_x - sell_btn_width - 10
            sell_btn_rect = pygame.Rect(sell_btn_x, btn_y, sell_btn_width, btn_height)
            sell_is_hovered = sell_btn_rect.collidepoint(mouse_pos)
            
            if is_owned:
                if is_equipped:
                    # Equipped - no button needed or show "Equipped" text
                    eq_text = "Equipped"
                    eq_surface = self.font.render(eq_text, True, (100, 255, 100))
                    surface.blit(eq_surface, (btn_x + (btn_width - eq_surface.get_width()) // 2, btn_y + 5))
                else:
                    # Equip button
                    btn_color = (80, 150, 80) if is_hovered else (50, 120, 50)
                    pygame.draw.rect(surface, btn_color, btn_rect, border_radius=4)
                    pygame.draw.rect(surface, WHITE, btn_rect, 1, border_radius=4)
                    
                    txt_surface = self.font.render("Equip", True, WHITE)
                    surface.blit(txt_surface, (btn_x + (btn_width - txt_surface.get_width()) // 2, btn_y + 6))
                    self.buttons.append((btn_rect, "equip", tool_key))
            else:
                # Buy button
                btn_color = (150, 120, 50) if is_hovered else (120, 90, 40)
                pygame.draw.rect(surface, btn_color, btn_rect, border_radius=4)
                pygame.draw.rect(surface, WHITE, btn_rect, 1, border_radius=4)
                
                txt_surface = self.font.render("Buy", True, WHITE)
                surface.blit(txt_surface, (btn_x + (btn_width - txt_surface.get_width()) // 2, btn_y + 6))
                self.buttons.append((btn_rect, "buy", tool_key))
                
            # Render Sell Button if owned
            if is_owned and tool.longevity > 0:
                sell_btn_color = (150, 80, 80) if sell_is_hovered else (120, 50, 50)
                pygame.draw.rect(surface, sell_btn_color, sell_btn_rect, border_radius=4)
                pygame.draw.rect(surface, WHITE, sell_btn_rect, 1, border_radius=4)
                
                import math
                uses = player.tool_uses.get(tool_key, 0)
                longevity_ratio = max(0, 1 - (uses / tool.longevity))
                sell_price = math.floor((tool.cost / 2) * longevity_ratio)
                
                # Try to get coin icon
                coin_path = Path(__file__).parent.parent.parent / 'assets' / 'sprites' / 'objects' / 'coin.png'
                coin_size = 16
                text_offset = 0
                
                if coin_path.exists():
                    try:
                        orig_coin = pygame.image.load(str(coin_path)).convert_alpha()
                        scaled_coin = pygame.transform.smoothscale(orig_coin, (coin_size, coin_size))
                        # Center everything together
                        sell_text = self.font_small.render(f"Sell:   {sell_price}", True, WHITE)
                        total_width = sell_text.get_width() + coin_size + 2
                        start_x = sell_btn_x + (sell_btn_width - total_width) // 2
                        
                        surface.blit(self.font_small.render("Sell:", True, WHITE), (start_x, btn_y + 8))
                        surface.blit(scaled_coin, (start_x + self.font_small.size("Sell: ")[0], btn_y + 7))
                        surface.blit(self.font_small.render(str(sell_price), True, WHITE), (start_x + self.font_small.size("Sell: ")[0] + coin_size + 2, btn_y + 8))
                        text_offset = 1 # Skip normal text drawing
                    except: pass
                
                if not text_offset:
                    sell_txt_surface = self.font_small.render(f"Sell: ${sell_price}", True, WHITE)
                    surface.blit(sell_txt_surface, (sell_btn_x + (sell_btn_width - sell_txt_surface.get_width()) // 2, btn_y + 8))
                    
                self.buttons.append((sell_btn_rect, "sell", tool_key))
            
            list_y += item_height + 10
            
        # Close instruction
        close_text = "Press 'I' or 'ESC' to close"
        close_surface = self.font_small.render(close_text, True, CLOSE_TEXT)
        c_x = dialog_x + (dialog_width - close_surface.get_width()) // 2
        c_y = dialog_y + dialog_height - close_surface.get_height() - 20
        surface.blit(close_surface, (c_x, c_y))
        
        # Render shared components over the inventory UI
        self.toast.render(surface, internal_width, internal_height)
        self.confirm_dialog.render(surface, internal_width, internal_height)
