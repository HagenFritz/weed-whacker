# Display & Resolution Tuning Guide

This guide explains how to configure the game's display settings to achieve the perfect balance between sprite detail, viewport size, and window size.

## Understanding the Display System

Weed Whacker uses a **viewport-based** rendering system similar to Stardew Valley, which allows you to:
- Use high-resolution sprites (e.g., 64×64px tiles)
- See many tiles on screen at once
- Maintain crisp pixel-art rendering via integer scaling

### Key Concepts

1. **TILE_SIZE**: The pixel resolution of your sprite assets (16px, 32px, 64px, etc.)
2. **VIEWPORT**: How many tiles fit on screen (width × height in tiles)
3. **SCALE_FACTOR**: Integer multiplier for the final window size

## Configuration (`weed_whacker/config.py`)

```python
# Tile size in pixels (asset resolution)
TILE_SIZE = 16

# Viewport settings (how many tiles fit on screen)
VIEWPORT_WIDTH_TILES = 20   # Number of tiles visible horizontally
VIEWPORT_HEIGHT_TILES = 15  # Number of tiles visible vertically

# Window scale factor (scales up internal resolution for crisp pixels)
SCALE_FACTOR = 3  # Final window will be INTERNAL_WIDTH * SCALE_FACTOR
```

### How It Works

**Internal Resolution** = `VIEWPORT_WIDTH_TILES × TILE_SIZE` by `VIEWPORT_HEIGHT_TILES × TILE_SIZE`
- Example: 20 tiles × 16px = 320px wide, 15 tiles × 16px = 240px tall

**Window Size** = `INTERNAL_WIDTH × SCALE_FACTOR` by `INTERNAL_HEIGHT × SCALE_FACTOR`
- Example: 320px × 3 = 960px wide, 240px × 3 = 720px tall

## Common Scenarios

### Scenario 1: More Detail, Same Viewport
**Goal**: Use 64×64px sprites but see the same number of tiles

```python
TILE_SIZE = 64
VIEWPORT_WIDTH_TILES = 20
VIEWPORT_HEIGHT_TILES = 15
SCALE_FACTOR = 1  # Reduce scale to keep window reasonable
```
- Internal: 1280×960px
- Window: 1280×960px (no scaling needed with high-res sprites)

### Scenario 2: Classic Pixel Art (Current)
**Goal**: Retro 16×16px sprites, medium viewport, crisp scaling

```python
TILE_SIZE = 16
VIEWPORT_WIDTH_TILES = 20
VIEWPORT_HEIGHT_TILES = 15
SCALE_FACTOR = 3
```
- Internal: 320×240px
- Window: 960×720px

### Scenario 3: HD Pixel Art
**Goal**: 32×32px sprites, large viewport for strategy view

```python
TILE_SIZE = 32
VIEWPORT_WIDTH_TILES = 30
VIEWPORT_HEIGHT_TILES = 20
SCALE_FACTOR = 1
```
- Internal: 960×640px
- Window: 960×640px

### Scenario 4: Stardew Valley Style
**Goal**: Detailed sprites, comfortable viewport, crisp pixels

```python
TILE_SIZE = 32
VIEWPORT_WIDTH_TILES = 20
VIEWPORT_HEIGHT_TILES = 15
SCALE_FACTOR = 2
```
- Internal: 640×480px
- Window: 1280×960px

## Fine-Tuning Tips

### If tiles look too big:
1. **Reduce TILE_SIZE** (e.g., 64 → 32 → 16)
2. **Increase VIEWPORT_*_TILES** (e.g., 15 → 20 → 25)

### If you see too few tiles:
1. **Increase VIEWPORT_*_TILES**
2. **Reduce TILE_SIZE** (allows more tiles to fit)

### If window is too small:
1. **Increase SCALE_FACTOR** (2 → 3 → 4)

### If window is too large:
1. **Decrease SCALE_FACTOR** (3 → 2 → 1)
2. **Reduce VIEWPORT_*_TILES**

### If pixels look blurry:
- Ensure `SCALE_FACTOR` is an **integer** (1, 2, 3, 4...)
- Never use fractional scaling (1.5, 2.5) - this causes blur

## Creating Sprites for Different Resolutions

### For TILE_SIZE = 16
- Create sprites at 16×16px
- Low detail, classic retro style
- Fast to create and iterate

### For TILE_SIZE = 32
- Create sprites at 32×32px
- Medium detail, Stardew Valley-like
- Good balance of detail and performance

### For TILE_SIZE = 64
- Create sprites at 64×64px
- High detail, modern pixel art
- Requires more artistic effort

**Important**: All your sprites must match `TILE_SIZE`. If you change it, regenerate or rescale all sprite assets.

## Recommended Presets

### Preset 1: Classic Retro
```python
TILE_SIZE = 16
VIEWPORT_WIDTH_TILES = 20
VIEWPORT_HEIGHT_TILES = 15
SCALE_FACTOR = 3
```
**Best for**: Quick prototyping, retro aesthetic, simple sprites

### Preset 2: Modern Indie (Recommended)
```python
TILE_SIZE = 32
VIEWPORT_WIDTH_TILES = 20
VIEWPORT_HEIGHT_TILES = 15
SCALE_FACTOR = 2
```
**Best for**: Polished indie game, detailed sprites, comfortable play

### Preset 3: HD Strategy
```python
TILE_SIZE = 32
VIEWPORT_WIDTH_TILES = 30
VIEWPORT_HEIGHT_TILES = 20
SCALE_FACTOR = 1
```
**Best for**: Wide view, strategy gameplay, large monitors

### Preset 4: High-Res Detail
```python
TILE_SIZE = 64
VIEWPORT_WIDTH_TILES = 15
VIEWPORT_HEIGHT_TILES = 12
SCALE_FACTOR = 1
```
**Best for**: Showcasing detailed pixel art, close-up gameplay

## Testing Your Settings

After changing `config.py`:
1. Run the game: `uv run python run.py`
2. Check if you can see enough of the world
3. Verify sprites look crisp (not blurry)
4. Ensure window fits your screen comfortably
5. Test on different monitor sizes if possible

## Troubleshooting

**Problem**: Changed TILE_SIZE but tiles still look the same size
- **Solution**: Also adjust VIEWPORT_*_TILES or SCALE_FACTOR

**Problem**: Sprites are blurry after scaling
- **Solution**: Use integer SCALE_FACTOR only (never 1.5, 2.7, etc.)

**Problem**: Window doesn't fit on my screen
- **Solution**: Reduce SCALE_FACTOR or reduce VIEWPORT_*_TILES

**Problem**: Can't see enough of the game world
- **Solution**: Increase VIEWPORT_*_TILES (shows more tiles at once)

## Advanced: Dynamic Resolution (Future Feature)

Future versions may support:
- In-game zoom controls
- Resolution presets menu
- Window resize with automatic viewport adjustment

For now, all changes require editing `config.py` and restarting the game.
