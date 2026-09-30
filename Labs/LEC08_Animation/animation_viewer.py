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
JUMP_CLIP = AnimationClip(
    frames=tuple(SpriteFrame(left, 96) for left in (160, 192, 224)),
    frame_duration=0.12,
)
ATTACK_CLIP = AnimationClip(
    frames=tuple(SpriteFrame(left, 144) for left in (0, 32, 64, 96, 128)),
    frame_duration=0.10,
)


def validate_clips(sheet_width: int, sheet_height: int) -> None:
    for clip in (WALK_CLIP, JUMP_CLIP, ATTACK_CLIP):
        for frame in clip.frames:
            if (
                frame.left < 0
                or frame.top < 0
                or frame.left + frame.width > sheet_width
                or frame.top + frame.height > sheet_height
            ):
                raise ValueError(f"Sprite frame is outside the sheet: {frame}")


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        validate_clips(sprite_sheet.w, sprite_sheet.h)
        clear_canvas()
        sprite_sheet.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        update_canvas()
        delay(0.5)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()