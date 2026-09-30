from dataclasses import dataclass
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
SPRITE_PATH = Path(__file__).with_name("sprites_fullsize.png")
FRAME_WIDTH = 32
FRAME_HEIGHT = 48


@dataclass(frozen=True)
class SpriteFrame:
    left: int
    top: int
    width: int = FRAME_WIDTH
    height: int = FRAME_HEIGHT

    def bottom_origin(self, sheet_height: int) -> int:
        return sheet_height - self.top - self.height


@dataclass(frozen=True)
class AnimationClip:
    frames: tuple[SpriteFrame, ...]
    frame_duration: float


WALK_CLIP = AnimationClip(
    frames=tuple(SpriteFrame(left, 0) for left in range(0, 512, FRAME_WIDTH)),
    frame_duration=0.08,
)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        clear_canvas()
        sprite_sheet.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        update_canvas()
        delay(0.5)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()