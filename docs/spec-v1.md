---

**Weed Whacker — Design Spec v1**

---

**Overview:**
A top-down, pixel-art, tile-based game built in Python using Pygame. The player manages a plot of land, cutting weeds to keep it clear and earning money from clear tiles. Money is used to expand the plot.

---

**Display and Rendering:**

- Internal pixel resolution: 320×240 (scaled up to a larger window, something like 960×720 or whatever looks good)
- Each tile is 16×16 pixels at internal resolution
- Top-down 2D view
- The grid should be centered on screen with room around the edges for a simple UI showing money, income rate, and tile count
- Camera: fixed for now since the starting grid is small. We can add scrolling later when plots get large enough to warrant it. Design the rendering so that adding a camera offset later is easy.

---

**Grid and Tiles:**

- Starting plot: 5×5 tiles
- Each tile has a type:
  - `GRASS` — clear, earnable tile. Rendered as a green square with a subtle pixel texture or color variation so it doesn't look flat.
  - `WEED` — a tile with a weed on it. Rendered as grass with a weed sprite on top (simple pixel plant shape). Does not generate income.
  - `UNOWNED` — not part of the plot. Rendered darker or grayed out. Tiles adjacent to the plot border should have some visual indicator that they're purchasable (subtle highlight or border).
- The world grid should be larger than the starting 5×5 (maybe 30×30 or more) so there's room to expand in any direction. Unowned tiles fill the rest.

---

**Player:**

- Represented by a simple pixel character sprite (even a colored square is fine for v1)
- Moves tile-to-tile, not free movement. Press a direction and the player moves one tile in that direction.
- Movement has a small cooldown/delay between steps so it feels deliberate, not instant. Something like 150ms between moves. Tunable.
- The player can only walk on tiles they own (GRASS, WEED). They cannot walk onto UNOWNED tiles.
- **Chopping:** When the player is standing on a WEED tile and presses the action key (spacebar or left mouse click), the weed is cut and the tile becomes GRASS. There is a 1 second cooldown after chopping before the player can chop again. The cooldown should be visually indicated — a small cooldown bar near the player or in the HUD that fills up over the cooldown duration, showing when the player can chop again.
- The player starts in the center of the 5×5 grid.

---

**Weed Spawning:**

- Every 5 seconds (tunable), one weed spawns on a random GRASS tile.
- If there are no valid GRASS tiles to spawn on (all weeds), the spawn is skipped that cycle.
- Weeds only spawn on GRASS tiles within the owned plot. Never on UNOWNED.

---

**Income System:**

- Income ticks every second (or continuously, updating the display every frame for a smooth counter).
- Income per tick = (number of GRASS tiles) × $1 per second. Only clear grass counts — not WEED tiles, not UNOWNED.
- Money is stored as a float internally for smooth accumulation but displayed as a whole number (floored) in the UI.

---

**Buying Tiles:**

- The player can purchase any UNOWNED tile that is directly adjacent (up/down/left/right, not diagonal) to an existing owned tile.
- To purchase: the player navigates to the edge of their plot, faces or selects the adjacent unowned tile (pressing the movement key toward an unowned tile while on the border, then confirming with B or Enter). Show the cost before confirming.
- **Cost formula:** First additional tile (tile 26, since you start with 25) costs a base price. Each tile after that costs $1 more. So if the base price is $10: tile 26 = $10, tile 27 = $11, tile 28 = $12, and so on. The base price and increment are tunable.
- Newly purchased tiles start as GRASS (clear).

---

**UI / HUD:**

- Display the following, updated in real time:
  - **Money:** Current balance (whole number)
  - **Income rate:** Current $/sec
  - **Tile count:** Owned tiles (e.g., "Tiles: 25") and how many currently have weeds
  - **Chop cooldown indicator:** A small bar or visual element that shows the cooldown progress. When full/ready, the player can chop. When depleted/filling, they're waiting. This could be near the player character or in a fixed HUD position.
- Keep the UI simple — small pixel font text in a bar along the top or bottom of the screen.
- When the player is on a border tile facing an unowned tile, show the purchase cost somewhere visible (near the tile or in the HUD).

---

**Controls:**

| Action | Key |
|---|---|
| Move up | W or Up Arrow |
| Move down | S or Down Arrow |
| Move left | A or Left Arrow |
| Move right | D or Right Arrow |
| Chop weed | Spacebar or Left Mouse Click |
| Buy tile | B (when on border facing unowned tile) |

---

**Tunable Constants (keep these in one place, like a `config.py`):**

```
TILE_SIZE = 16
INTERNAL_WIDTH = 320
INTERNAL_HEIGHT = 240
SCALE_FACTOR = 3

STARTING_GRID_SIZE = 5
WORLD_GRID_SIZE = 30

PLAYER_MOVE_COOLDOWN = 150      # ms
CHOP_COOLDOWN = 1000            # ms

WEED_SPAWN_INTERVAL = 5000      # ms
INCOME_PER_TILE_PER_SECOND = 1  # dollars

TILE_BASE_COST = 10             # first tile costs this
TILE_COST_INCREMENT = 1         # each subsequent tile costs this much more
```

---

**Project Structure:**

```
weed-whacker/            # Project root and repository
├── main.py              # Entry point, game loop
├── config.py            # All tunable constants
├── assets/
│   ├── sprites/         # Player, weed, tile sprites
│   └── sounds/          # (empty for now, but ready)
├── src/
│   ├── game.py          # Main game state and loop logic
│   ├── grid.py          # Grid/tile management
│   ├── player.py        # Player movement and actions
│   ├── economy.py       # Income, money, purchasing
│   └── ui.py            # HUD rendering
├── docs/
├── README.md
└── requirements.txt     # pygame
```

---

**Build order suggestion (for Claude Code):**

1. Set up Pygame window with scaling, render the 5×5 grid of green tiles surrounded by dark unowned tiles
2. Add the player sprite and tile-to-tile movement with cooldown
3. Add weed spawning on a timer and the chop mechanic with cooldown indicator
4. Add the income system
5. Add tile purchasing
6. Polish the UI/HUD
