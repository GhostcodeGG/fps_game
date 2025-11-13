"""Ray casting renderer for the pseudo-3D scene."""

from __future__ import annotations

import math
from typing import List, Tuple

import pygame

from . import settings

RayResult = Tuple[float, float, Tuple[int, int, int]]


class RayCasting:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.ray_casting_result: List[RayResult] = []

    def update(self) -> None:
        self.ray_casting_result = []
        start_angle = self.game.player.angle - settings.HALF_FOV
        angle = start_angle
        for _ in range(settings.NUM_RAYS):
            depth, tile_id, side = self._cast_single_ray(angle)
            depth = max(depth, 0.0001)
            depth *= math.cos(self.game.player.angle - angle)
            proj_height = settings.PROJ_COEFF / depth
            color = self.game.map.tile_color(tile_id, dim=bool(side), depth=depth)
            self.ray_casting_result.append((depth, proj_height, color))
            angle += settings.DELTA_ANGLE

    def draw(self, surface: pygame.Surface) -> None:
        for ray, (depth, proj_height, color) in enumerate(self.ray_casting_result):
            column = ray * settings.SCALE
            height = min(int(proj_height), settings.HEIGHT * 2)
            offset = settings.HALF_HEIGHT - height // 2
            pygame.draw.rect(
                surface,
                color,
                (column, offset, settings.SCALE, height),
            )

    # ------------------------------------------------------------------
    # Core ray casting routine
    # ------------------------------------------------------------------
    def _cast_single_ray(self, angle: float) -> Tuple[float, str, int]:
        sin_a = math.sin(angle) or 1e-6
        cos_a = math.cos(angle) or 1e-6

        ox, oy = self.game.player.pos
        x_map = int(ox)
        y_map = int(oy)

        delta_dist_x = abs(1 / cos_a)
        delta_dist_y = abs(1 / sin_a)

        if cos_a < 0:
            step_x = -1
            side_dist_x = (ox - x_map) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (x_map + 1.0 - ox) * delta_dist_x

        if sin_a < 0:
            step_y = -1
            side_dist_y = (oy - y_map) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (y_map + 1.0 - oy) * delta_dist_y

        tile_id = "1"
        side = 0
        for _ in range(settings.MAX_DEPTH * 5):
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                x_map += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                y_map += step_y
                side = 1
            if (x_map, y_map) in self.game.map.world_map:
                tile_id = self.game.map.world_map[(x_map, y_map)]
                if side == 0:
                    depth = (x_map - ox + (1 - step_x) / 2) / cos_a
                else:
                    depth = (y_map - oy + (1 - step_y) / 2) / sin_a
                return abs(depth), tile_id, side

        return float(settings.MAX_DEPTH), tile_id, side

