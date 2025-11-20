# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Codex FPS Prototype is a lightweight first-person shooter built from scratch using pygame and classic ray casting techniques. Inspired by early 3D shooters like Doom and Quake, it provides smooth mouse-look, WASD movement, collision detection, and a real-time pseudo-3D renderer—all with an approachable codebase for experimentation.

## Commands

### Installation

Create virtual environment and install pygame:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Game

Start the prototype:
```bash
python main.py
```

Controls:
- W/S: Move forward/backward
- A/D: Strafe left/right
- Mouse: Look around (cursor is locked)
- Shift: Sprint
- Esc: Quit

## Architecture

### Module Organization

The game follows a clean separation of rendering, simulation, and input:

- **main.py**: Entry point that initializes and starts the Game instance
- **game.py**: Main loop orchestration (event handling, update, draw)
- **player.py**: Player movement, rotation, and collision handling
- **raycasting.py**: DDA-based ray casting renderer that creates the 3D view
- **map.py**: World map storage, collision queries, and mini-map rendering
- **settings.py**: Centralized configuration for screen size, FOV, colors, speeds, etc.

### Game Loop Structure

The main loop in `game.py` runs at a fixed FPS (60 by default) with three stages:

1. **Event Handling**: Process pygame events (quit, escape) and mouse movement for camera rotation
2. **Update**: Advance delta time, update player position/collision, update ray casting results
3. **Draw**: Render sky/floor, ray cast walls, mini-map, crosshair, weapon overlay, and HUD

Delta time is calculated via `clock.tick(FPS)` and passed to movement calculations for frame-rate independence.

### Ray Casting Renderer

The raycasting module implements a DDA (Digital Differential Analyzer) algorithm to cast rays from the player's position:

**Ray Casting Process**:
1. For each vertical strip of the screen, cast one ray from the player's eye
2. Step through the grid using DDA until hitting a wall tile
3. Calculate perpendicular wall distance to avoid fish-eye distortion: `depth *= cos(player.angle - ray_angle)`
4. Project wall height: `proj_height = PROJ_COEFF / depth`
5. Apply lighting falloff based on depth and wall orientation (horizontal vs vertical)
6. Draw vertical strip with calculated height and color

**Key Details**:
- `NUM_RAYS` determines horizontal resolution (one ray per vertical strip)
- `DELTA_ANGLE = FOV / NUM_RAYS` calculates angular step between rays
- `PROJ_COEFF` is pre-calculated as `SCREEN_DISTANCE * TILE_SIZE` for projection
- Wall colors are dimmed based on depth and side (creates depth perception and wall shading)
- The `side` flag (0 or 1) indicates whether a horizontal or vertical wall face was hit

### Player Movement and Collision

Player position is stored as float coordinates (x, y) with an angle in radians.

**Movement System**:
1. Poll keyboard for WASD input
2. Calculate movement vector based on player's facing angle (cos/sin)
3. Apply sprint multiplier if Shift is held (1.6x speed)
4. Attempt movement along each axis separately to allow wall sliding

**Collision Detection**:
- Movement is split into X and Y components, tested independently
- `_try_move(dx, dy)` checks if the new position would collide with a wall tile
- Collision uses the map's `world_map` dictionary: if `(int(x), int(y))` exists, it's a wall
- Separate axis testing allows sliding along walls when moving diagonally

**Camera Control**:
- Mouse movement is captured via `pygame.mouse.get_rel()`
- Relative X movement is clamped to `MOUSE_MAX_REL` to prevent overly sensitive turning
- Angle is updated with `MOUSE_SENSITIVITY` multiplier and wrapped to [0, 2π]

### Map Representation

The world is stored as a sparse dictionary `world_map: Dict[Tuple[int, int], str]` where:
- Keys are (x, y) integer grid coordinates
- Values are tile IDs (e.g., "1", "2") that map to colors via `TILE_COLORS`

**Mini-Map**:
- Rendered in the corner showing top-down view of the map
- Player position is marked with a colored square
- Walls are drawn as small rectangles at scaled coordinates

This sparse representation allows easy editing and efficient collision checks.

### Settings and Configuration

All tunable parameters are centralized in `settings.py`:

**Display**: WIDTH, HEIGHT, FPS, HALF_WIDTH, HALF_HEIGHT
**Ray Casting**: FOV, HALF_FOV, NUM_RAYS, DELTA_ANGLE, MAX_DEPTH, PROJ_COEFF
**Player**: PLAYER_SPEED, MOUSE_SENSITIVITY, MOUSE_MAX_REL
**Colors**: SKY_COLOR, FLOOR_COLOR, TILE_COLORS, CROSSHAIR_COLOR

Adjust these values to change game feel, performance, and aesthetics.

## Important Conventions

- Coordinates use a top-left origin: X increases rightward, Y increases downward
- Angles are in radians with 0 pointing right (east), increasing counter-clockwise
- The ray caster uses perpendicular distance correction to prevent fish-eye warping
- Movement is frame-rate independent via `delta_time` multiplier
- Mouse is grabbed and hidden when the game starts (use Esc to release)
- Wall shading uses both depth-based dimming and side-based dimming (horizontal walls are darker)
- The renderer draws sky (top half) and floor (bottom half) as solid colors before casting walls
