# Asset System Architecture Guide

This guide explains the modular asset management system for Weed Whacker, designed to support multiple player avatars, tools, weed types, objects, and easy extensibility.

## Overview

The asset system is built around **specialized managers** that each handle a specific category of game assets. This makes it easy to add new content without cluttering a single file.

## Directory Structure

```
weed_whacker/assets/
├── managers/                    # Asset manager modules
│   ├── __init__.py
│   ├── base_asset_manager.py   # Base class with common loading logic
│   ├── asset_manager.py        # Unified manager coordinating all types
│   ├── tile_manager.py         # Grass, unowned tiles, variations
│   ├── weed_manager.py         # Weed types and variations
│   ├── player_manager.py       # Player avatars and skins
│   ├── tool_manager.py         # Tools and equipment icons
│   └── object_manager.py       # Decorative objects, buildings
└── sprites/                     # Actual sprite PNG files
    ├── tiles/                   # grass_0.png, grass_1.png, etc.
    ├── weeds/                   # weed_basic.png, weed_thistle.png, etc.
    ├── players/                 # player_default.png, player_blue.png, etc.
    ├── tools/                   # scythe.png, hoe.png, etc.
    └── objects/                 # rock_small.png, tree.png, etc.
```

## Asset Manager Classes

### BaseAssetManager

**Location**: `weed_whacker/assets/managers/base_asset_manager.py`

Base class providing common sprite loading functionality:
- **Load from PNG**: Tries to load `{name}.png` from the asset subdirectory
- **Fallback generation**: If PNG doesn't exist, calls a generator function
- **Auto-scaling**: Scales loaded sprites to match tile size

**Key Methods**:
- `_load_or_generate(name, generator_func, size=None)`: Load or generate sprite
- `get_sprite(name)`: Retrieve sprite by name
- `render_sprite(surface, sprite_name, x, y)`: Render sprite to surface

### TileManager

**Location**: `weed_whacker/assets/managers/tile_manager.py`  
**Subdirectory**: `sprites/tiles/`

Manages terrain tiles:
- **Grass variations**: `grass_0`, `grass_1`, `grass_2` (color variations)
- **Unowned tiles**: `unowned`, `unowned_purchasable`

**Adding new tiles**:
```python
# In TileManager._load_tiles()
self.sprites['grass_autumn'] = self._load_or_generate(
    'grass_autumn',
    self._generate_grass_autumn
)
```

### WeedManager

**Location**: `weed_whacker/assets/managers/weed_manager.py`  
**Subdirectory**: `sprites/weeds/`

Manages weed types:
- **Current**: `weed_basic`
- **Ready to enable**: `weed_thistle`, `weed_dandelion` (commented out)

**Adding new weed types**:
```python
# 1. Uncomment in WeedManager._load_weeds()
self.sprites['weed_thistle'] = self._load_or_generate(
    'weed_thistle',
    lambda: self._generate_weed('thistle', 0)
)

# 2. Add generator method
def _draw_thistle_weed(self, surface, variation):
    # Draw thistle sprite logic
    pass
```

**Weed variations**: Each weed type can have multiple visual variations by passing a `variation` parameter.

### PlayerManager

**Location**: `weed_whacker/assets/managers/player_manager.py`  
**Subdirectory**: `sprites/players/`

Manages player avatars:
- **Current**: `player` (default blue avatar)
- **Ready to enable**: `player_blue`, `player_red` (commented out)

**Adding new avatars**:
```python
# 1. Add to color_map in _generate_player()
color_map = {
    'default': (64, 164, 223),
    'green': (50, 200, 50),
    'purple': (150, 50, 200)  # New avatar
}

# 2. Load in _load_players()
self.sprites['player_purple'] = self._load_or_generate(
    'player_purple',
    lambda: self._generate_player('purple')
)

# 3. To switch active player, update game_manager.py:
# Change 'player' sprite lookup to 'player_purple'
```

### ToolManager

**Location**: `weed_whacker/assets/managers/tool_manager.py`  
**Subdirectory**: `sprites/tools/`

Manages tool icons:
- **Current**: `scythe` (for UI cooldown bar)
- **Ready to enable**: `hoe`, `watering_can` (commented out)

**Icon sizes**: Tools use custom sizes (usually smaller than tiles) for UI display.

**Adding new tools**:
```python
# 1. Add to _load_tools()
icon_size = max(12, self.tile_size // 2)
self.sprites['shovel'] = self._load_or_generate(
    'shovel',
    self._generate_shovel,
    size=(icon_size, icon_size)
)

# 2. Add generator
def _generate_shovel(self):
    size = max(12, self.tile_size // 2)
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    # Draw shovel sprite
    return surface
```

### ObjectManager

**Location**: `weed_whacker/assets/managers/object_manager.py`  
**Subdirectory**: `sprites/objects/`

Manages decorative objects and buildings:
- **Ready to enable**: `rock_small`, `rock_large`, `tree`, `fence` (all commented out)

**Use cases**:
- Obstacles that block movement
- Decorative elements
- Buildings and structures
- Interactive objects (future)

**Adding objects**:
```python
# Uncomment in _load_objects()
self.sprites['tree'] = self._load_or_generate(
    'tree',
    self._generate_tree
)
```

### AssetManager (Unified)

**Location**: `weed_whacker/assets/managers/asset_manager.py`

Coordinates all specialized managers. This is what the game imports and uses.

**Initialization**:
```python
from weed_whacker.assets.managers.asset_manager import AssetManager

asset_manager = AssetManager(tile_size=64)
```

**Accessing sprites**:
```python
# Automatically searches all managers
sprite = asset_manager.get_sprite('weed_basic')  # Finds in WeedManager
sprite = asset_manager.get_sprite('player')      # Finds in PlayerManager

# Or render directly
asset_manager.render_sprite(surface, 'grass_0', x, y)
```

## Creating Custom Sprites

### Option 1: Create PNG Files

1. Create your sprite as a PNG file
2. Save to the appropriate subdirectory:
   - Tiles → `assets/sprites/tiles/`
   - Weeds → `assets/sprites/weeds/`
   - Players → `assets/sprites/players/`
   - Tools → `assets/sprites/tools/`
   - Objects → `assets/sprites/objects/`
3. Name it exactly as referenced in code (e.g., `weed_basic.png`)
4. The manager will auto-load and scale it

**Recommended tools**:
- Aseprite (pixel art editor)
- GIMP (free image editor)
- Piskel (online pixel art tool)

### Option 2: Programmatic Generation

If no PNG exists, the manager generates sprites programmatically (useful for prototyping).

**Example: Add a new weed type**:

```python
# In WeedManager
def _draw_clover_weed(self, surface, variation):
    """Draw a clover weed sprite (three-leaf pattern)"""
    clover_color = (40, 120, 40)
    center_x = self.tile_size // 2
    center_y = self.tile_size // 2
    radius = max(2, self.tile_size // 8)
    
    # Draw three circles in clover pattern
    positions = [
        (center_x - radius, center_y),
        (center_x + radius, center_y),
        (center_x, center_y - radius)
    ]
    
    for pos in positions:
        pygame.draw.circle(surface, clover_color, pos, radius)
```

## Usage in Game Code

### In Renderers

**GridRenderer** and **PlayerRenderer** receive an `AssetManager` instance:

```python
# Example: GridRenderer
class GridRenderer:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
    
    def render(self, surface, grid, tile_size, camera_offset):
        # Render grass
        self.asset_manager.render_sprite(surface, 'grass_0', x, y)
        
        # Render weed
        self.asset_manager.render_sprite(surface, 'weed_basic', x, y)
```

### In Game Manager

**game_manager.py** initializes the unified AssetManager:

```python
from ..assets.managers.asset_manager import AssetManager

class Game:
    def __init__(self):
        self.asset_manager = AssetManager(TILE_SIZE)
        
        # Pass to renderers
        self.grid_renderer = GridRenderer(self.asset_manager)
        self.player_renderer = PlayerRenderer(self.asset_manager)
```

## Extending the System

### Adding a New Asset Category

If you need a completely new category (e.g., "effects" for particle effects):

1. **Create manager**: `weed_whacker/assets/managers/effect_manager.py`

```python
from .base_asset_manager import BaseAssetManager

class EffectManager(BaseAssetManager):
    def __init__(self, tile_size):
        super().__init__(tile_size, 'effects')
        self._load_effects()
    
    def _load_effects(self):
        self.sprites['smoke'] = self._load_or_generate(
            'smoke',
            self._generate_smoke
        )
    
    def _generate_smoke(self):
        # Generate smoke sprite
        pass
```

2. **Register in AssetManager**: `asset_manager.py`

```python
from .effect_manager import EffectManager

class AssetManager:
    def __init__(self, tile_size):
        # ... existing managers
        self.effects = EffectManager(tile_size)
    
    def get_sprite(self, sprite_name):
        for manager in [self.tiles, self.weeds, self.players, 
                        self.tools, self.objects, self.effects]:  # Add here
            sprite = manager.get_sprite(sprite_name)
            if sprite:
                return sprite
        return None
```

3. **Create subdirectory**: `assets/sprites/effects/`

### Adding Sprite Variations

To add multiple variations of the same sprite:

```python
# In WeedManager._load_weeds()
for i in range(3):  # 3 variations
    self.sprites[f'weed_basic_var{i}'] = self._load_or_generate(
        f'weed_basic_var{i}',
        lambda variation=i: self._generate_weed('basic', variation)
    )
```

Then use variations in game logic:
```python
# Random variation
variation = random.randint(0, 2)
asset_manager.render_sprite(surface, f'weed_basic_var{variation}', x, y)
```

## Best Practices

1. **PNG > Generation**: Always prefer PNG sprites for final art (better quality, easier to edit)
2. **Consistent naming**: Use snake_case for sprite names (`weed_thistle`, not `WeedThistle`)
3. **Keep managers focused**: One manager per asset category
4. **Document generators**: Comment what each programmatic sprite generator creates
5. **Test at multiple sizes**: Your sprites should work with different `TILE_SIZE` values
6. **Use transparency**: Most sprites should use `pygame.SRCALPHA` for transparent backgrounds
7. **Version control sprites**: Commit PNG files to git for team collaboration

## Troubleshooting

**Sprite not loading**:
1. Check PNG filename matches exactly (case-sensitive)
2. Verify PNG is in correct subdirectory
3. Check manager is loading that sprite name
4. Ensure AssetManager includes that manager

**Sprite looks wrong**:
1. Check PNG resolution (should match or be larger than `TILE_SIZE`)
2. Verify sprite has transparency if needed
3. Test generator function if using programmatic sprites

**Performance issues**:
1. Pre-load all sprites at startup (already done in managers)
2. Don't reload sprites every frame
3. Consider sprite sheets for many small sprites (future optimization)

## Future Enhancements

Ideas for extending the asset system:

- **Animation support**: Multi-frame sprites with timing
- **Sprite sheets**: Pack multiple sprites into one image for efficiency
- **Dynamic loading**: Load sprites on-demand instead of all at startup
- **Asset caching**: Save generated sprites to disk for faster startup
- **Mod support**: Allow users to drop PNG files to customize sprites
- **Palette swapping**: Recolor sprites programmatically (e.g., for team colors)
