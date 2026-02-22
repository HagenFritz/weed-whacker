"""
Weed Whacker - Confirm Dialog Component
A modal dialog asking the user to confirm or cancel an action
"""

import pygame # type: ignore
from ...constants.colors import PANEL_BG, PANEL_BORDER, UI_TEXT, UI_TEXT_SHADOW, WHITE

class ConfirmDialog:
    """A modal dialog asking the user to confirm or cancel an action"""
    
    def __init__(self):
        self.active = False
        self.message = ""
        self.on_confirm = None
        self.font_large = None
        self.font = None
        self.buttons = []
        self._init_fonts()
        
    def _init_fonts(self):
        if not hasattr(pygame.font, '_initialized') or not pygame.font.get_init():
            pygame.font.init()
        self.font_large = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 24)
        
    def show(self, message, on_confirm_callback):
        """Show the confirm dialog
        
        Args:
            message: Text to display asking for confirmation
            on_confirm_callback: Function to call if user confirms
        """
        self.message = message
        self.on_confirm = on_confirm_callback
        self.active = True
        
    def close(self):
        self.active = False
        self.on_confirm = None
        self.buttons.clear()
        
    def handle_click(self, mouse_pos):
        """Handle mouse clicks when dialog is open. Returns True if handled."""
        if not self.active:
            return False
            
        for rect, action in self.buttons:
            if rect.collidepoint(mouse_pos):
                if action == "confirm" and self.on_confirm:
                    self.on_confirm()
                self.close()
                return True
                
        return True # Always consume clicks when active to prevent clicking behind
        
    def render(self, surface, internal_width, internal_height):
        """Render the confirm dialog if active"""
        if not self.active:
            return
            
        self.buttons.clear()
            
        dialog_width = 400
        dialog_height = 200
        dialog_x = (internal_width - dialog_width) // 2
        dialog_y = (internal_height - dialog_height) // 2
        
        # Semi-transparent overlay to dim background further
        overlay = pygame.Surface((internal_width, internal_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Dialog Background
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        
        # Determine background color safely for SRCALPHA surface
        bg_alpha = PANEL_BG[3] if len(PANEL_BG) > 3 else 255
        bg_color = (*PANEL_BG[:3], bg_alpha)
        dialog_surface.fill(bg_color)
        
        surface.blit(dialog_surface, (dialog_x, dialog_y))
        
        border_color = PANEL_BORDER[:3]
        pygame.draw.rect(surface, border_color, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=8)
        
        # Title
        title_text = "Confirm"
        title_surface = self.font_large.render(title_text, True, UI_TEXT)
        title_x = dialog_x + (dialog_width - title_surface.get_width()) // 2
        title_y = dialog_y + 20
        surface.blit(self.font_large.render(title_text, True, UI_TEXT_SHADOW), (title_x + 2, title_y + 2))
        surface.blit(title_surface, (title_x, title_y))
        
        # Message
        msg_surface = self.font.render(self.message, True, UI_TEXT)
        msg_x = dialog_x + (dialog_width - msg_surface.get_width()) // 2
        msg_y = dialog_y + 80
        surface.blit(msg_surface, (msg_x, msg_y))
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        btn_width = 100
        btn_height = 36
        btn_y = dialog_y + dialog_height - btn_height - 20
        
        # Cancel Button (Left)
        cancel_x = dialog_x + (dialog_width // 2) - btn_width - 10
        cancel_rect = pygame.Rect(cancel_x, btn_y, btn_width, btn_height)
        cancel_hover = cancel_rect.collidepoint(mouse_pos)
        cancel_color = (150, 80, 80) if cancel_hover else (120, 50, 50)
        
        pygame.draw.rect(surface, cancel_color, cancel_rect, border_radius=4)
        pygame.draw.rect(surface, WHITE, cancel_rect, 1, border_radius=4)
        c_text = self.font.render("Cancel", True, WHITE)
        surface.blit(c_text, (cancel_x + (btn_width - c_text.get_width()) // 2, btn_y + 8))
        self.buttons.append((cancel_rect, "cancel"))
        
        # Confirm Button (Right)
        confirm_x = dialog_x + (dialog_width // 2) + 10
        confirm_rect = pygame.Rect(confirm_x, btn_y, btn_width, btn_height)
        confirm_hover = confirm_rect.collidepoint(mouse_pos)
        confirm_color = (80, 150, 80) if confirm_hover else (50, 120, 50)
        
        pygame.draw.rect(surface, confirm_color, confirm_rect, border_radius=4)
        pygame.draw.rect(surface, WHITE, confirm_rect, 1, border_radius=4)
        co_text = self.font.render("Confirm", True, WHITE)
        surface.blit(co_text, (confirm_x + (btn_width - co_text.get_width()) // 2, btn_y + 8))
        self.buttons.append((confirm_rect, "confirm"))
