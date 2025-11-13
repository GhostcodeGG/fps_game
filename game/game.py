"""Main game loop and orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pygame

from . import settings
from .map import GameMap
from .player import Player
from .raycasting import RayCasting


@dataclass
class HUDStats:
    fps: float = 0.0
    position: Tuple[float, float] = (0.0, 0.0)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Codex FPS Prototype")
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.map = GameMap()
        self.player = Player(self)
        self.raycasting = RayCasting(self)
        self.hud = HUDStats()

    # ------------------------------------------------------------------
    # Game loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        while True:
            self._handle_events()
            self._update()
            self._draw()

    # ------------------------------------------------------------------
    # Core update stages
    # ------------------------------------------------------------------
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._shutdown()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._shutdown()

        rel = pygame.mouse.get_rel()
        rel_x = max(-settings.MOUSE_MAX_REL, min(settings.MOUSE_MAX_REL, rel[0]))
        if rel_x:
            self.player.rotate(rel_x)

    def _update(self) -> None:
        self.delta_time = self.clock.tick(settings.FPS) / 1000.0
        self.player.update()
        self.raycasting.update()
        self._update_hud()

    def _draw(self) -> None:
        self.screen.fill(settings.SKY_COLOR)
        pygame.draw.rect(
            self.screen,
            settings.FLOOR_COLOR,
            (0, settings.HALF_HEIGHT, settings.WIDTH, settings.HALF_HEIGHT),
        )
        self.raycasting.draw(self.screen)
        self.map.draw_minimap(self.screen, self.player.pos)
        self.player.draw_on_minimap(self.screen)
        self._draw_crosshair()
        self._draw_weapon_overlay()
        self._draw_hud()
        pygame.display.flip()

    # ------------------------------------------------------------------
    # HUD helpers
    # ------------------------------------------------------------------
    def _update_hud(self) -> None:
        fps = self.clock.get_fps()
        self.hud = HUDStats(
            fps=fps,
            position=self.player.pos,
        )

    def _draw_crosshair(self) -> None:
        center = (settings.HALF_WIDTH, settings.HALF_HEIGHT)
        pygame.draw.line(
            self.screen,
            settings.CROSSHAIR_COLOR,
            (center[0] - 10, center[1]),
            (center[0] + 10, center[1]),
            2,
        )
        pygame.draw.line(
            self.screen,
            settings.CROSSHAIR_COLOR,
            (center[0], center[1] - 10),
            (center[0], center[1] + 10),
            2,
        )

    def _draw_weapon_overlay(self) -> None:
        width = 180
        height = 100
        rect = pygame.Rect(
            settings.HALF_WIDTH - width // 2,
            settings.HEIGHT - height - 20,
            width,
            height,
        )
        pygame.draw.rect(self.screen, settings.WEAPON_COLOR, rect, border_radius=12)
        inner_rect = rect.inflate(-60, -60)
        pygame.draw.rect(self.screen, settings.WEAPON_ACCENT_COLOR, inner_rect, border_radius=8)

    def _draw_hud(self) -> None:
        font = pygame.font.SysFont("consolas", 18)
        fps_text = font.render(f"FPS: {self.hud.fps:05.1f}", True, settings.HUD_TEXT_COLOR)
        pos_x, pos_y = self.hud.position
        pos_text = font.render(
            f"Pos: {pos_x:04.2f}, {pos_y:04.2f}",
            True,
            settings.HUD_TEXT_COLOR,
        )
        self.screen.blit(fps_text, (20, settings.HEIGHT - 60))
        self.screen.blit(pos_text, (20, settings.HEIGHT - 36))

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------
    def _shutdown(self) -> None:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        pygame.quit()
        raise SystemExit


__all__ = ["Game"]

