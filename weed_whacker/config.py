"""
Weed Whacker - Game Configuration
All tunable constants for easy balancing
"""

# Display settings
# Tile size in pixels (asset resolution)
TILE_SIZE = 64

# Viewport settings (how many tiles fit on screen)
VIEWPORT_WIDTH_TILES = 20  # Number of tiles visible horizontally
VIEWPORT_HEIGHT_TILES = 15  # Number of tiles visible vertically

# Calculated internal resolution based on viewport
INTERNAL_WIDTH = VIEWPORT_WIDTH_TILES * TILE_SIZE
INTERNAL_HEIGHT = VIEWPORT_HEIGHT_TILES * TILE_SIZE

# Window scale factor (scales up internal resolution for crisp pixels)
SCALE_FACTOR = 1  # Final window will be INTERNAL_WIDTH * SCALE_FACTOR

# Grid settings
STARTING_GRID_SIZE = 5
WORLD_GRID_SIZE = 30

# Player settings
PLAYER_MOVE_COOLDOWN = 150      # ms
CHOP_COOLDOWN = 1000            # ms

# Weed spawning
WEED_SPAWN_INTERVAL = 5000      # ms

# Economy
INCOME_PER_TILE_PER_SECOND = 0.01  # dollars
TILE_BASE_COST = 10             # first tile costs this
TILE_COST_INCREMENT = 1         # each subsequent tile costs this much more
