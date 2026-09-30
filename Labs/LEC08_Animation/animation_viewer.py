from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
SPRITE_PATH = Path(__file__).with_name("sprites_fullsize.png")
GRASS_PATH = Path(__file__).with_name("grass.png")
FRAME_WIDTH = 32
FRAME_HEIGHT = 48
SPRITE_SCALE = 8
START_X = 120.0
CENTER_X = CANVAS_WIDTH / 2
GROUND_Y = 400.0
WALK_SPEED = 240.0
JUMP_DURATION = 0.9
ATTACK_DURATION = len(ATTACK_CLIP.frames) * ATTACK_CLIP.frame_duration


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


class Phase(Enum):
    WALK_TO_CENTER = auto()
    JUMP = auto()
    ATTACK = auto()
    WALK_TO_LEFT = auto()


@dataclass
class AnimationState:
    phase: Phase = Phase.WALK_TO_CENTER
    x: float = START_X
    y: float = GROUND_Y
    facing_right: bool = True
    frame_index: int = 0
    frame_elapsed: float = 0.0
    action_elapsed: float = 0.0


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


def draw_frame(
    sprite_sheet,
    frame: SpriteFrame,
    x: float,
    y: float,
    facing_right: bool = True,
) -> None:
    flip = "" if facing_right else "h"
    sprite_sheet.clip_composite_draw(
        frame.left,
        frame.bottom_origin(sprite_sheet.h),
        frame.width,
        frame.height,
        0,
        flip,
        x,
        y,
        frame.width * SPRITE_SCALE,
        frame.height * SPRITE_SCALE,
    )


def draw_scene(grass) -> None:
    clear_canvas()
    grass.draw(CANVAS_WIDTH // 2, 150, CANVAS_WIDTH, 100)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        grass = load_image(str(GRASS_PATH))
        validate_clips(sprite_sheet.w, sprite_sheet.h)
        draw_scene(grass)
        draw_frame(
            sprite_sheet,
            WALK_CLIP.frames[0],
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2,
        )
        update_canvas()
        delay(0.5)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()