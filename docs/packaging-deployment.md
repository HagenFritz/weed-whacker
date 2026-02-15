# Packaging and Deployment Guide

This guide explains how to package Weed Whacker as a standalone executable for distribution on platforms like Steam.

## Overview

Python games need to be bundled into executables so players don't need Python installed. We use **PyInstaller** to create standalone executables that include Python, all dependencies (pygame), and game assets in a single distributable package.

## Prerequisites

Install PyInstaller as a development dependency:

```bash
uv add --dev pyinstaller
```

Or if you've already synced the project, PyInstaller is included in the dev dependencies.

## Building an Executable

### Basic Build (One-File Executable)

From the repository root, run:

```bash
uv run pyinstaller run.py --onefile --name "WeedWhacker"
```

This creates a single executable file in `dist/WeedWhacker` (or `dist/WeedWhacker.exe` on Windows).

**Flags explained:**
- `--onefile`: Bundles everything into a single executable
- `--name "WeedWhacker"`: Names the output file

### Including Game Assets

Since Weed Whacker uses sprites and potentially other assets, you need to include the `weed_whacker/assets` directory:

```bash
uv run pyinstaller run.py \
  --onefile \
  --name "WeedWhacker" \
  --add-data "weed_whacker/assets:weed_whacker/assets"
```

**Note:** On Windows, use semicolon instead of colon:
```bash
uv run pyinstaller run.py --onefile --name "WeedWhacker" --add-data "weed_whacker/assets;weed_whacker/assets"
```

### Recommended Build Configuration

For better organization and easier debugging, use a one-folder bundle during development:

```bash
uv run pyinstaller run.py \
  --onedir \
  --name "WeedWhacker" \
  --add-data "weed_whacker/assets:weed_whacker/assets" \
  --windowed
```

**Additional flags:**
- `--onedir`: Creates a folder with the executable and dependencies (easier to debug)
- `--windowed`: Hides the console window (use for final builds)

### Creating a Spec File (Advanced)

For complex builds, create a `.spec` file for reusable configuration:

```bash
uv run pyinstaller --name "WeedWhacker" run.py --add-data "weed_whacker/assets:weed_whacker/assets"
```

This generates `WeedWhacker.spec`. Edit it as needed, then build with:

```bash
uv run pyinstaller WeedWhacker.spec
```

## Distribution Structure

After building, your `dist/` folder will contain:

### One-File Build
```
dist/
└── WeedWhacker(.exe)    # Single executable
```

### One-Folder Build
```
dist/
└── WeedWhacker/
    ├── WeedWhacker(.exe)       # Main executable
    ├── _internal/              # Python runtime and dependencies
    └── weed_whacker/
        └── assets/             # Game assets
```

## Steam Deployment

### 1. Prepare Your Build

- Use `--onedir` for Steam (easier for Steam to manage files)
- Test the executable thoroughly on target platforms (Windows, macOS, Linux)
- Build separate executables for each platform (PyInstaller bundles are platform-specific)

### 2. Steam Requirements

To distribute on Steam, you need:

1. **Steamworks SDK** - Download from Steamworks partner site
2. **Steam App ID** - Obtained after Steam Direct submission ($100 fee)
3. **Steam Integration** (optional) - For achievements, cloud saves, etc.

### 3. Steam Depot Structure

Organize your build for Steam:

```
steam_build/
├── windows/
│   └── WeedWhacker/        # Windows build folder
├── macos/
│   └── WeedWhacker.app/    # macOS app bundle
├── linux/
│   └── WeedWhacker/        # Linux build folder
└── app_build_config.vdf    # Steam build configuration
```

### 4. Steamworks Configuration

Create `app_build_config.vdf`:

```vdf
"AppBuild"
{
    "AppID" "YOUR_APP_ID"
    "Desc" "Weed Whacker Build"
    "BuildOutput" "output"
    "ContentRoot" "."
    "SetLive" "default"
    
    "Depots"
    {
        "YOUR_DEPOT_ID_WINDOWS"
        {
            "FileMapping"
            {
                "LocalPath" "windows/*"
                "DepotPath" "."
                "Recursive" "1"
            }
        }
        
        "YOUR_DEPOT_ID_MAC"
        {
            "FileMapping"
            {
                "LocalPath" "macos/*"
                "DepotPath" "."
                "Recursive" "1"
            }
        }
        
        "YOUR_DEPOT_ID_LINUX"
        {
            "FileMapping"
            {
                "LocalPath" "linux/*"
                "DepotPath" "."
                "Recursive" "1"
            }
        }
    }
}
```

### 5. Upload to Steam

Use the Steamworks SDK's `steamcmd` tool:

```bash
steamcmd +login YOUR_USERNAME +run_app_build /path/to/app_build_config.vdf +quit
```

### 6. Steam Greenlight / Direct

- **Steam Direct**: Pay $100 fee and submit your game for review
- Complete store page with screenshots, description, videos
- Set pricing and release date
- Pass Steam's content review

## Platform-Specific Notes

### Windows
- Build on Windows or use Wine/CrossOver
- Include Visual C++ Redistributable if needed
- Test on Windows 10/11

### macOS
- Build on macOS
- Code sign and notarize the app (required for macOS 10.15+)
- Create `.app` bundle structure
- Test on both Intel and Apple Silicon Macs

### Linux
- Build on Linux
- Test on Ubuntu/Debian (most common)
- Consider AppImage or Flatpak for easier distribution

## Troubleshooting

### Missing Modules
If PyInstaller misses a module, add it explicitly:
```bash
--hidden-import=module_name
```

### Assets Not Loading
Ensure asset paths are relative and use the `--add-data` flag correctly. In code, use:
```python
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
```

### Large Executable Size
- Use `--onedir` instead of `--onefile`
- Exclude unnecessary modules with `--exclude-module`
- Consider UPX compression (built into PyInstaller)

## Testing Checklist

Before distributing:

- [ ] Test executable on clean system (no Python installed)
- [ ] Verify all assets load correctly
- [ ] Test on minimum system requirements
- [ ] Check for antivirus false positives
- [ ] Test all game features (movement, actions, UI)
- [ ] Verify save/load functionality (if applicable)
- [ ] Test on all target platforms

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [Steamworks Documentation](https://partner.steamgames.com/doc/home)
- [Steam Direct FAQ](https://partner.steamgames.com/doc/gettingstarted)
- [Pygame Bundling Guide](https://www.pygame.org/wiki/Executable)

## Quick Reference Commands

```bash
# Development build (fast, easy to debug)
uv run pyinstaller run.py --onedir --name "WeedWhacker" --add-data "weed_whacker/assets:weed_whacker/assets"

# Production build (single file, no console)
uv run pyinstaller run.py --onefile --windowed --name "WeedWhacker" --add-data "weed_whacker/assets:weed_whacker/assets"

# Clean previous builds
rm -rf build/ dist/ *.spec

# Test the executable
./dist/WeedWhacker/WeedWhacker  # or dist/WeedWhacker.exe on Windows
```
