# Weed Whacker

A top-down, pixel-art, tile-based game built in Python using Pygame. Manage your plot of land by cutting weeds to keep it clear and earning money from clear tiles. Use your earnings to expand your territory!

## Installation

1. Ensure you have Python 3.8+ installed
2. Install [uv](https://docs.astral.sh/uv/) (fast Python package manager):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or: pip install uv
```
3. Sync dependencies (creates `.venv` automatically):
```bash
uv sync
```

## Running the Game

```bash
uv run python run.py
```

Or using the module directly:
```bash
uv run python -m weed_whacker.main
```

Or via the installed script:
```bash
uv run weed-whacker
```

## Dependency & Packaging Notes

- **Package manager:** Uses `uv` for fast, reliable dependency management with automatic virtual environment handling.
- **Dependencies:** Defined in `pyproject.toml` with exact versions locked in `uv.lock` for reproducible builds.
- **Virtual environment:** `uv sync` automatically creates `.venv` in the repo root. Do not commit it.
- **Adding dependencies:** Use `uv add <package>` to add runtime deps or `uv add --dev <package>` for dev-only deps.
- **Sharing source:** Include `pyproject.toml` and `uv.lock`. Recipients run `uv sync` to install.
- **Building executables:** See `docs/packaging-deployment.md` for PyInstaller bundling and Steam deployment.

## Controls

| Action | Key |
|--------|-----|
| Move up | W or Up Arrow |
| Move down | S or Down Arrow |
| Move left | A or Left Arrow |
| Move right | D or Right Arrow |
| Chop weed | Spacebar or Left Mouse Click |
| Buy tile | B (when on border facing unowned tile) |

## Game Mechanics

- **Income**: Earn $1 per second for each clear grass tile
- **Weeds**: Spawn randomly every 5 seconds on grass tiles
- **Chopping**: Stand on a weed tile and press spacebar to clear it (1 second cooldown)
- **Expansion**: Purchase adjacent unowned tiles to expand your plot
  - First tile costs $10, each additional tile costs $1 more

## Project Structure

```
weed-whacker/               # Repository root
├── run.py                  # Game launcher script
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # Locked dependency versions
├── weed_whacker/           # Main package
│   ├── __init__.py
│   ├── main.py             # Entry point, game loop
│   ├── config.py           # All tunable constants
│   ├── assets/
│   │   ├── sprites/        # Player, weed, tile sprites
│   │   └── sounds/         # Sound effects (future)
│   └── src/
│       ├── __init__.py
│       ├── game.py         # Main game state and loop logic
│       ├── grid.py         # Grid/tile management
│       ├── player.py       # Player movement and actions
│       ├── economy.py      # Income, money, purchasing
│       └── ui.py           # HUD rendering
└── docs/
    └── spec-v1.md          # Design specification
```

## Configuration

All game parameters can be tuned in [weed_whacker/config.py](weed_whacker/config.py), including:
- Display resolution and scaling
- Grid sizes
- Movement and action cooldowns
- Weed spawn rate
- Income rates
- Tile costs

## Development

See [docs/spec-v1.md](docs/spec-v1.md) for the full design specification
