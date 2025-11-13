"""Runtime configuration for the FPS prototype."""

from __future__ import annotations

import math

# --- Display configuration -------------------------------------------------
WIDTH = 960
HEIGHT = 540
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# --- Ray casting configuration ---------------------------------------------
FOV = math.pi / 3  # 60° field of view, similar to classic shooters
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2  # Number of rays to cast per frame
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# Projection constants used to size wall slices
DIST = NUM_RAYS / math.tan(HALF_FOV)
PROJ_COEFF = DIST * 70
SCALE = WIDTH // NUM_RAYS

# --- Player configuration ---------------------------------------------------
PLAYER_SPEED = 3.0  # units per second
PLAYER_ROT_SPEED = 0.0  # Mouse driven, so keyboard rotation disabled
PLAYER_RADIUS = 0.2

# --- Mouse configuration ----------------------------------------------------
MOUSE_SENSITIVITY = 0.0008
MOUSE_MAX_REL = 300

# --- Mini map ---------------------------------------------------------------
MINIMAP_SCALE = 8
MINIMAP_SIZE = 10  # How many tiles to display (square area)
MINIMAP_POSITION = (10, 10)

# --- Visual palette ---------------------------------------------------------
SKY_COLOR = (30, 30, 40)
FLOOR_COLOR = (40, 30, 20)
CROSSHAIR_COLOR = (240, 240, 240)
HUD_TEXT_COLOR = (200, 200, 200)

# Tile colors referenced by the ray caster. Values are RGB.
WALL_COLORS = {
    "1": (190, 190, 190),
    "2": (200, 120, 80),
    "3": (80, 160, 200),
    "4": (150, 90, 190),
}
DEFAULT_WALL_COLOR = (180, 180, 180)

# Weapon overlay configuration
WEAPON_COLOR = (220, 220, 220)
WEAPON_ACCENT_COLOR = (120, 180, 255)

__all__ = [
    "WIDTH",
    "HEIGHT",
    "HALF_WIDTH",
    "HALF_HEIGHT",
    "FPS",
    "FOV",
    "HALF_FOV",
    "NUM_RAYS",
    "DELTA_ANGLE",
    "MAX_DEPTH",
    "DIST",
    "PROJ_COEFF",
    "SCALE",
    "PLAYER_SPEED",
    "PLAYER_ROT_SPEED",
    "PLAYER_RADIUS",
    "MOUSE_SENSITIVITY",
    "MOUSE_MAX_REL",
    "MINIMAP_SCALE",
    "MINIMAP_SIZE",
    "MINIMAP_POSITION",
    "SKY_COLOR",
    "FLOOR_COLOR",
    "CROSSHAIR_COLOR",
    "HUD_TEXT_COLOR",
    "WALL_COLORS",
    "DEFAULT_WALL_COLOR",
    "WEAPON_COLOR",
    "WEAPON_ACCENT_COLOR",
]
