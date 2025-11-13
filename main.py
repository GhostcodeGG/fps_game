"""Entry point for the FPS prototype."""

from __future__ import annotations

from game.game import Game


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
