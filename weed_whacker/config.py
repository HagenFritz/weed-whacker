"""
Weed Whacker - Game Configuration
All tunable constants for easy balancing
"""

# Display settings
TILE_SIZE = 16
INTERNAL_WIDTH = 320
INTERNAL_HEIGHT = 240
SCALE_FACTOR = 3

# Grid settings
STARTING_GRID_SIZE = 5
WORLD_GRID_SIZE = 30

# Player settings
PLAYER_MOVE_COOLDOWN = 150      # ms
CHOP_COOLDOWN = 1000            # ms

# Weed spawning
WEED_SPAWN_INTERVAL = 5000      # ms

# Economy
INCOME_PER_TILE_PER_SECOND = 1  # dollars
TILE_BASE_COST = 10             # first tile costs this
TILE_COST_INCREMENT = 1         # each subsequent tile costs this much more
