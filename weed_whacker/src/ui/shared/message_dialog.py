"""
Weed Whacker - Message Dialog Component
A modal dialog that displays a message to the user with an OK button.
"""

import pygame # type: ignore
from ...constants.colors import PANEL_BG, PANEL_BORDER, UI_TEXT, UI_TEXT_SHADOW, WHITE

class MessageDialog:
    """A modal dialog displaying a message to the user"""
    
    def __init__(self):
        self.active = False
        self.title = ""
        self.message = ""
        self.on_close = None
        self.font_large = None
        self.font = None
        self.button_rect = None
        self._init_fonts()
        
    def _init_fonts(self):
        if not hasattr(pygame.font, '_initialized') or not pygame.font.get_init():
            pygame.font.init()
        self.font_large = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 24)
        
    def show(self, title, message, on_close_callback=None):
        """Show the message dialog
        
        Args:
            title: Dialog title
            message: Text to display
            on_close_callback: Optional function to call when dismissed
        """
        self.title = title
        self.message = message
        self.on_close = on_close_callback
        self.active = True
        
    def close(self):
        self.active = False
        if self.on_close:
            self.on_close()
        self.on_close = None
        self.button_rect = None
        
    def handle_click(self, mouse_pos):
        """Handle mouse clicks when dialog is open. Returns True if handled."""
        if not self.active:
            return False
            
        if self.button_rect and self.button_rect.collidepoint(mouse_pos):
            self.close()
            return True
            
        return True # Always consume clicks when active to prevent clicking behind
        
    def render(self, surface, internal_width, internal_height):
        """Render the message dialog if active"""
        if not self.active:
            return
            
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
        title_surface = self.font_large.render(self.title, True, UI_TEXT)
        title_x = dialog_x + (dialog_width - title_surface.get_width()) // 2
        title_y = dialog_y + 20
        surface.blit(self.font_large.render(self.title, True, UI_TEXT_SHADOW), (title_x + 2, title_y + 2))
        surface.blit(title_surface, (title_x, title_y))
        
        # Message
        msg_surface = self.font.render(self.message, True, UI_TEXT)
        msg_x = dialog_x + (dialog_width - msg_surface.get_width()) // 2
        msg_y = dialog_y + 80
        surface.blit(msg_surface, (msg_x, msg_y))
        
        # OK Button
        mouse_pos = pygame.mouse.get_pos()
        btn_width = 100
        btn_height = 36
        btn_x = dialog_x + (dialog_width - btn_width) // 2
        btn_y = dialog_y + dialog_height - btn_height - 20
        
        self.button_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        btn_hover = self.button_rect.collidepoint(mouse_pos)
        btn_color = (80, 150, 80) if btn_hover else (50, 120, 50)
        
        pygame.draw.rect(surface, btn_color, self.button_rect, border_radius=4)
        pygame.draw.rect(surface, WHITE, self.button_rect, 1, border_radius=4)
        btn_text = self.font.render("OK", True, WHITE)
        surface.blit(btn_text, (btn_x + (btn_width - btn_text.get_width()) // 2, btn_y + 8))
