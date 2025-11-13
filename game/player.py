"""Player control and camera handling."""

from __future__ import annotations

import math
from typing import Tuple

import pygame

from . import settings


class Player:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.x = 3.5
        self.y = 3.5
        self.angle = math.pi / 4

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def pos(self) -> Tuple[float, float]:
        return self.x, self.y

    @property
    def dir(self) -> Tuple[float, float]:
        return math.cos(self.angle), math.sin(self.angle)

    # ------------------------------------------------------------------
    # Update loop
    # ------------------------------------------------------------------
    def update(self) -> None:
        self._handle_movement()

    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def _handle_movement(self) -> None:
        keys = pygame.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = settings.PLAYER_SPEED * self.game.delta_time
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_w]:
            dx += cos_a * speed
            dy += sin_a * speed
        if keys[pygame.K_s]:
            dx -= cos_a * speed
            dy -= sin_a * speed
        if keys[pygame.K_a]:
            dx += sin_a * speed
            dy -= cos_a * speed
        if keys[pygame.K_d]:
            dx -= sin_a * speed
            dy += cos_a * speed

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            dx *= 1.6
            dy *= 1.6

        self._move(dx, dy)

    def rotate(self, rel_x: float) -> None:
        self.angle += rel_x * settings.MOUSE_SENSITIVITY
        self.angle %= math.tau

    # ------------------------------------------------------------------
    # Collision handling
    # ------------------------------------------------------------------
    def _move(self, dx: float, dy: float) -> None:
        if dx:
            self._try_move(dx, 0.0)
        if dy:
            self._try_move(0.0, dy)

    def _try_move(self, dx: float, dy: float) -> None:
        new_x = self.x + dx
        new_y = self.y + dy
        radius = settings.PLAYER_RADIUS
        if not self.game.map.is_blocked(new_x, new_y, radius):
            self.x = new_x
            self.y = new_y

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------
    def draw_on_minimap(self, surface: pygame.Surface) -> None:
        tile_size = settings.MINIMAP_SCALE
        offset_x, offset_y = settings.MINIMAP_POSITION
        half_span = settings.MINIMAP_SIZE // 2
        frac_x = self.x - int(self.x)
        frac_y = self.y - int(self.y)
        px = offset_x + half_span * tile_size + frac_x * tile_size + tile_size / 2
        py = offset_y + half_span * tile_size + frac_y * tile_size + tile_size / 2
        pygame.draw.circle(surface, (200, 200, 0), (int(px), int(py)), 4)
        dir_x, dir_y = self.dir
        pygame.draw.line(
            surface,
            (200, 200, 0),
            (int(px), int(py)),
            (int(px + dir_x * 12), int(py + dir_y * 12)),
            2,
        )

