"""
Weed Whacker - Toast Component
A temporary message popup that appears on screen and fades out
"""

import pygame # type: ignore
import time
from ...constants.colors import PANEL_BG, PANEL_BORDER, UI_TEXT

class Toast:
    """A temporary message popup that appears on screen and fades out"""
    
    def __init__(self):
        self.message = ""
        self.active = False
        self.duration = 0
        self.start_time = 0
        self.font = None
        self._init_fonts()
        
    def _init_fonts(self):
        if not hasattr(pygame.font, '_initialized') or not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        
    def show(self, message, duration=3.0):
        """Show a toast message
        
        Args:
            message: Text to display
            duration: Time in seconds to show the toast
        """
        self.message = message
        self.active = True
        self.duration = duration
        self.start_time = time.time()
        
    def update(self):
        """Update toast state. Call this every frame."""
        if not self.active:
            return
            
        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            self.active = False
            
    def render(self, surface, internal_width, internal_height):
        """Render the toast if active"""
        if not self.active:
            return
            
        elapsed = time.time() - self.start_time
        
        # Calculate alpha for fade out (last 0.5 seconds)
        alpha = 255
        fade_duration = 0.5
        time_left = self.duration - elapsed
        if time_left < fade_duration:
            alpha = max(0, min(255, int(255 * (time_left / fade_duration))))
            
        text_surface = self.font.render(self.message, True, UI_TEXT)
        text_rect = text_surface.get_rect()
        
        # Background padding
        padding_x = 20
        padding_y = 10
        
        bg_width = text_rect.width + padding_x * 2
        bg_height = text_rect.height + padding_y * 2
        bg_x = (internal_width - bg_width) // 2
        bg_y = internal_height - bg_height - 40 # 40 pixels from bottom
        
        # Create a surface with alpha support for fading
        toast_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        
        # Determine background alpha - if PANEL_BG has an alpha component, use that as the base
        base_bg_alpha = PANEL_BG[3] if len(PANEL_BG) > 3 else 255
        bg_alpha = int((base_bg_alpha / 255.0) * alpha)
        
        # Draw background and border
        # Fix invalid color issue by only taking the first 3 elements (RGB) and supplying alpha separately 
        # or relying on the surface's alpha handling. Since it's SRCALPHA, we pass an RGBA tuple.
        bg_color = (*PANEL_BG[:3], bg_alpha)
        pygame.draw.rect(toast_surface, bg_color, (0, 0, bg_width, bg_height), border_radius=8)
        
        border_color = (*PANEL_BORDER[:3], alpha)
        pygame.draw.rect(toast_surface, border_color, (0, 0, bg_width, bg_height), 2, border_radius=8)
        
        # Draw text
        text_surface.set_alpha(alpha)
        toast_surface.blit(text_surface, (padding_x, padding_y))
        
        # Blit to screen
        surface.blit(toast_surface, (bg_x, bg_y))
