"""World map and helper routines for collision and mini-map rendering."""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

import pygame

from . import settings

GridPoint = Tuple[int, int]


class GameMap:
    """Stores the tile-based layout of the level."""

    #: Legend used when parsing the string based map layout
    LEGEND = {
        "#": "1",
        "@": "2",
        "%": "3",
        "*": "4",
    }

    def __init__(self) -> None:
        self.world_map: Dict[GridPoint, str] = {}
        self._build_map()

    def _build_map(self) -> None:
        layout = [
            "################",
            "#..............#",
            "#..@......%....#",
            "#..............#",
            "#......####....#",
            "#......#..#....#",
            "#..*...#..#....#",
            "#......####....#",
            "#..............#",
            "#....%.....@...#",
            "#..............#",
            "################",
        ]

        for y, row in enumerate(layout):
            for x, char in enumerate(row):
                if char == ".":
                    continue
                self.world_map[(x, y)] = self.LEGEND.get(char, "1")

    # ------------------------------------------------------------------
    # Collision helpers
    # ------------------------------------------------------------------
    def is_wall(self, x: float, y: float) -> bool:
        """Return ``True`` if the coordinate is blocked by a wall."""

        return (int(x), int(y)) in self.world_map

    def surrounding_tiles(self, x: float, y: float, radius: float) -> Iterable[GridPoint]:
        """Yield tiles in the collision envelope for ``(x, y)``."""

        min_x = int(x - radius)
        max_x = int(x + radius)
        min_y = int(y - radius)
        max_y = int(y + radius)
        for tile_y in range(min_y, max_y + 1):
            for tile_x in range(min_x, max_x + 1):
                yield tile_x, tile_y

    def is_blocked(self, x: float, y: float, radius: float) -> bool:
        """Return ``True`` if any tile in the envelope is solid."""

        for tile in self.surrounding_tiles(x, y, radius):
            if tile in self.world_map:
                return True
        return False

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------
    def tile_color(self, tile_id: str, *, dim: bool = False, depth: float | None = None) -> Tuple[int, int, int]:
        """Return an RGB color for ``tile_id`` with optional shading."""

        base_color = settings.WALL_COLORS.get(tile_id, settings.DEFAULT_WALL_COLOR)
        shade = 0.6 if dim else 1.0
        if depth is not None:
            shade *= max(0.2, 1.0 / (1.0 + depth * 0.15))
        return tuple(int(component * shade) for component in base_color)

    def draw_minimap(self, surface: pygame.Surface, player_pos: Tuple[float, float]) -> None:
        """Render the top-down map in the top-left corner."""

        tile_size = settings.MINIMAP_SCALE
        offset_x, offset_y = settings.MINIMAP_POSITION
        max_tiles = settings.MINIMAP_SIZE

        px, py = player_pos
        center_x = int(px)
        center_y = int(py)

        half_span = max_tiles // 2
        size = tile_size * (2 * half_span + 1)
        bg_rect = pygame.Rect(offset_x - 4, offset_y - 4, size + 8, size + 8)
        pygame.draw.rect(surface, (8, 8, 8), bg_rect, border_radius=6)
        for tile_y in range(center_y - half_span, center_y + half_span + 1):
            for tile_x in range(center_x - half_span, center_x + half_span + 1):
                rect = pygame.Rect(
                    offset_x + (tile_x - center_x + half_span) * tile_size,
                    offset_y + (tile_y - center_y + half_span) * tile_size,
                    tile_size,
                    tile_size,
                )
                if (tile_x, tile_y) in self.world_map:
                    pygame.draw.rect(surface, (120, 120, 120), rect)
                else:
                    pygame.draw.rect(surface, (30, 30, 30), rect)
        border_rect = pygame.Rect(offset_x - 4, offset_y - 4, size + 8, size + 8)
        pygame.draw.rect(surface, (160, 160, 160), border_rect, width=1, border_radius=6)

