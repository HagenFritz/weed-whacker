"""
Weed Whacker - Main Entry Point
"""

import pygame
import sys
from .src.game import Game
from .config import INTERNAL_WIDTH, INTERNAL_HEIGHT, SCALE_FACTOR


def main():
    """Initialize Pygame and start the game loop"""
    pygame.init()

    # Create window with scaled resolution
    window_width = INTERNAL_WIDTH * SCALE_FACTOR
    window_height = INTERNAL_HEIGHT * SCALE_FACTOR
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Weed Whacker")

    # Create internal surface for pixel-perfect rendering
    internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))

    # Initialize game
    game = Game()
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        dt = clock.tick(60)  # 60 FPS, returns milliseconds since last frame

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        # Update game state
        game.update(dt)

        # Render to internal surface
        game.render(internal_surface)

        # Scale up to window
        pygame.transform.scale(internal_surface, (window_width, window_height), screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
