"""
Weed Whacker - HUD and UI Rendering
"""

import pygame


class UI:
    """Handles HUD rendering and display"""

    def __init__(self):
        """Initialize UI"""
        self.font = None
        self._init_font()

    def _init_font(self):
        """Initialize font for rendering text"""
        try:
            # Try to use a pixel-style font
            self.font = pygame.font.Font(None, 16)  # Default pygame font
        except Exception:
            self.font = pygame.font.Font(None, 16)

    def render(self, surface, money, income_rate, owned_tiles, weed_count, chop_cooldown_percent):
        """Render the HUD

        Args:
            surface: Pygame surface to render to
            money: Current money (integer)
            income_rate: Income per second
            owned_tiles: Total owned tiles
            weed_count: Number of tiles with weeds
            chop_cooldown_percent: Chop cooldown progress (0.0 to 1.0)
        """
        # Draw HUD background bar at top
        hud_height = 30
        pygame.draw.rect(surface, (40, 40, 40), (0, 0, surface.get_width(), hud_height))

        # Render text elements
        y_pos = 5
        x_offset = 5

        # Money
        money_text = f"Money: ${money}"
        self._draw_text(surface, money_text, x_offset, y_pos, (255, 215, 0))
        x_offset += 100

        # Income rate
        income_text = f"Income: ${income_rate}/s"
        self._draw_text(surface, income_text, x_offset, y_pos, (144, 238, 144))
        x_offset += 100

        # Tile count
        tiles_text = f"Tiles: {owned_tiles} ({weed_count} weeds)"
        self._draw_text(surface, tiles_text, x_offset, y_pos, (200, 200, 200))

    def render_chop_cooldown(self, surface, x, y, cooldown_percent):
        """Render chop cooldown indicator

        Args:
            surface: Pygame surface to render to
            x, y: Position to render at
            cooldown_percent: Cooldown progress (0.0 = ready, 1.0 = just used)
        """
        bar_width = 12
        bar_height = 2

        # Background (empty bar)
        pygame.draw.rect(surface, (100, 100, 100), (x, y, bar_width, bar_height))

        # Fill (cooldown progress - fills up as it recovers)
        fill_width = int(bar_width * (1.0 - cooldown_percent))
        if fill_width > 0:
            pygame.draw.rect(surface, (0, 255, 0), (x, y, fill_width, bar_height))

    def render_purchase_prompt(self, surface, cost, x, y):
        """Render tile purchase cost prompt

        Args:
            surface: Pygame surface to render to
            cost: Cost of the tile
            x, y: Screen position to render at
        """
        prompt_text = f"${cost} (B to buy)"
        self._draw_text(surface, prompt_text, x, y, (255, 255, 0))

    def _draw_text(self, surface, text, x, y, color=(255, 255, 255)):
        """Draw text at position

        Args:
            surface: Pygame surface to render to
            text: Text string to render
            x, y: Position
            color: RGB color tuple
        """
        text_surface = self.font.render(text, True, color)
        surface.blit(text_surface, (x, y))
