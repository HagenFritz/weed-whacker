# Sprite Creation Guide for Weed Whacker

## Current Setup

Your game now has a **sprite management system** with automatic fallback:
- **Programmatic sprites**: Currently used (colored squares, simple shapes)
- **File-based sprites**: Drop PNG files in `weed_whacker/assets/sprites/` to override
- **Automatic loading**: The `SpriteManager` tries to load PNGs first, falls back to generated sprites

## Sprite Requirements

All sprites should be **16×16 pixels** to match your tile size.

### Needed Sprites

1. **`player.png`** - Player character
2. **`grass.png`** - Clear grass tile
3. **`weed.png`** - Grass tile with weed
4. **`unowned.png`** - Unowned dark tile
5. **`unowned_purchasable.png`** - Purchasable unowned tile with highlight

## Option 1: Manual Pixel Art (Beginner-Friendly)

### Recommended Free Tools

1. **[Piskel](https://www.piskelapp.com/)** (Web-based, no install)
   - Free, intuitive
   - Export as PNG
   - Built-in animation support (for future)

2. **[Aseprite](https://www.aseprite.org/)** ($20, or compile free)
   - Industry standard for pixel art
   - Powerful animation tools
   - Best for serious pixel art

3. **[GIMP](https://www.gimp.org/)** (Free)
   - General purpose, can do pixel art
   - Set grid to 16×16 and zoom way in

### Quick Start with Piskel

1. Go to https://www.piskelapp.com/
2. Set canvas size to 16×16 (Resize tool)
3. Zoom in (bottom right, 800%+)
4. Turn on grid (View → Show grid)
5. Draw your sprite pixel by pixel
6. Export as PNG (`File → Export`)
7. Save to `weed_whacker/assets/sprites/player.png`

### Tips for 16×16 Pixel Art

- **Keep it simple**: At 16×16, every pixel counts
- **Limit colors**: 3-5 colors per sprite looks cohesive
- **Use outlines**: Dark 1-pixel border helps sprites pop
- **Center important features**: Eyes, stems, etc.
- **Test in-game**: Drop sprite in folder and run game

## Option 2: AI Image Generation

### Recommended AI Tools

1. **[DALL-E 3](https://openai.com/dall-e-3)** (via ChatGPT Plus)
   - High quality
   - Good at following pixel art instructions
   - $20/month

2. **[Midjourney](https://www.midjourney.com/)**
   - Excellent pixel art style
   - Community-driven
   - $10/month basic

3. **[Stable Diffusion](https://stablediffusion.fr/)** (Free, open source)
   - Locally run (privacy)
   - Various pixel art models available
   - Steeper learning curve

4. **[Bing Image Creator](https://www.bing.com/images/create)** (Free)
   - Uses DALL-E 3
   - Limited daily credits
   - No account needed

### AI Prompting Guide

**General Formula:**
```
[subject], pixel art, 16x16, top-down view, [color palette], simple, clean, game sprite, transparent background
```

### Specific Prompts for Your Game

#### Player Character
```
Small farmer character, pixel art, 16x16, top-down view, blue overalls, simple design, 
game sprite, transparent background, retro style, stardew valley inspired
```

**Alternative:**
```
Top-down pixel art character sprite, 16x16 pixels, farmer with hat, blue and brown colors, 
simple clean design, game asset, transparent background
```

#### Grass Tile
```
Grass texture tile, pixel art, 16x16, top-down view, bright green, simple repeating pattern, 
game tile, seamless, vibrant, stardew valley style
```

#### Weed Sprite (on grass)
```
Small weed plant on grass, pixel art, 16x16, top-down view, dark green and brown, 
simple design, game sprite, lawn weed, transparent background
```

**Alternative:**
```
Dandelion or thistle weed, pixel art, 16x16 pixels, top-down perspective, 
green grass background, simple retro game art
```

#### Dark Unowned Tile
```
Dark dirt or stone ground tile, pixel art, 16x16, top-down view, dark gray, 
simple texture, game tile, seamless pattern
```

### Tips for AI Generation

1. **Multiple attempts**: Generate 4-10 variations, pick the best
2. **Be specific**: Mention "16x16", "top-down", "pixel art" every time
3. **Reference games**: "Stardew Valley style" or "Minecraft-like" helps
4. **Post-process**: AI may generate larger images - resize to 16×16 in GIMP/Piskel
5. **Clean up**: Remove backgrounds, adjust colors if needed

### Post-Processing AI Sprites

AI often generates at higher resolution. To resize:

1. **In GIMP:**
   - `Image → Scale Image`
   - Set to 16×16 pixels
   - Interpolation: `None` (keeps pixels crisp)
   - `Layer → Transparency → Add Alpha Channel`
   - Use `Select → By Color` to remove backgrounds
   - `File → Export As` → PNG

2. **In Piskel:**
   - Import the AI image
   - Resize to 16×16
   - Clean up manually
   - Export PNG

## Option 3: Free Pixel Art Assets

### Asset Libraries

1. **[OpenGameArt.org](https://opengameart.org/)**
   - Filter: "Pixel Art" + "Top-Down"
   - License: Check CC0 or CC-BY for free use

2. **[itch.io Asset Packs](https://itch.io/game-assets/free/tag-pixel-art)**
   - Many free packs
   - Search "top-down" + "farming" or "garden"

3. **[Kenney Assets](https://www.kenney.nl/assets)**
   - High-quality free assets
   - Consistent style
   - Usually 16×16 or easily resizable

### Using Existing Assets

1. Download asset pack
2. Find sprites that fit (player, grass, etc.)
3. Resize to 16×16 if needed
4. Rename to match system: `player.png`, `grass.png`, etc.
5. Copy to `weed_whacker/assets/sprites/`

## Testing Your Sprites

1. **Drop PNGs in folder:**
   ```
   weed_whacker/assets/sprites/
   ├── player.png
   ├── grass.png
   ├── weed.png
   ├── unowned.png
   └── unowned_purchasable.png
   ```

2. **Run the game:**
   ```bash
   uv run python run.py
   ```

3. **See them in action:** Sprites load automatically!

4. **If sprite doesn't appear:**
   - Check filename matches exactly (case-sensitive)
   - Verify it's 16×16 pixels (or will be auto-scaled)
   - Ensure it's PNG format
   - Check terminal for loading errors

## Recommended Workflow

### For Quick Iteration
1. Start with programmatic sprites (current)
2. Create 1-2 sprites manually in Piskel
3. Test in-game to see if you like the style
4. Generate rest with AI or continue manually

### For Best Quality
1. Use AI to generate initial concepts (larger size)
2. Resize and clean up in Piskel/Aseprite
3. Manually touch up pixels for consistency
4. Test in-game frequently

### For Free/No-Hassle
1. Browse OpenGameArt or Kenney
2. Find a cohesive tileset pack
3. Extract needed sprites
4. Resize and rename as needed

## Color Palette Recommendations

For a cohesive look, stick to a limited palette:

**Nature Theme (Current):**
- Grass: `#228B22` (Forest Green)
- Dirt/Unowned: `#3C2415` (Dark Brown)
- Player: `#4169E1` (Royal Blue)
- Weed: `#556B2F` (Dark Olive Green)

**Vibrant Theme:**
- Grass: `#7EC850` (Light Green)
- Dirt: `#8B4513` (Saddle Brown)
- Player: `#FF6B6B` (Coral Red)
- Weed: `#4A7C59` (Sea Green)

## Next Steps

1. **Start simple:** Try Piskel for player sprite first
2. **Test immediately:** Drop `player.png` in sprites folder and run game
3. **Iterate:** If you like it, continue with grass and weed
4. **AI assist:** Use AI for complex sprites, touch up manually
5. **Share:** Once you have a set you like, they're ready for distribution!

## Future Enhancements

Consider adding later:
- **Animations:** Player walking cycles (4 frames per direction)
- **Particle effects:** Chopping animation, money pop-ups
- **UI sprites:** Icons for money, tiles, etc.
- **Sound effects:** Match new visual style with audio
- **Tile variations:** Multiple grass textures for variety

---

**Remember:** The game works great with programmatic sprites. Only add custom sprites when you're ready to polish the aesthetic!
