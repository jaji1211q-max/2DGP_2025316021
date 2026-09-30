from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from time import perf_counter

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


def clip_for_phase(phase: Phase) -> AnimationClip:
    if phase in (Phase.WALK_TO_CENTER, Phase.WALK_TO_LEFT):
        return WALK_CLIP
    if phase is Phase.JUMP:
        return JUMP_CLIP
    return ATTACK_CLIP


def advance_frame(state: AnimationState, delta_time: float) -> None:
    clip = clip_for_phase(state.phase)
    state.frame_elapsed += delta_time
    while state.frame_elapsed >= clip.frame_duration:
        state.frame_elapsed -= clip.frame_duration
        if state.phase in (Phase.WALK_TO_CENTER, Phase.WALK_TO_LEFT):
            state.frame_index = (state.frame_index + 1) % len(clip.frames)
        else:
            state.frame_index = min(state.frame_index + 1, len(clip.frames) - 1)


def move_toward(current: float, target: float, distance: float) -> float:
    if current < target:
        return min(current + distance, target)
    return max(current - distance, target)


def enter_phase(state: AnimationState, phase: Phase) -> None:
    state.phase = phase
    state.frame_index = 0
    state.frame_elapsed = 0.0
    state.action_elapsed = 0.0


def update_walk_to_center(state: AnimationState, delta_time: float) -> None:
    state.facing_right = True
    state.x = move_toward(state.x, CENTER_X, WALK_SPEED * delta_time)
    if state.x >= CENTER_X:
        enter_phase(state, Phase.JUMP)


def update_jump(state: AnimationState, delta_time: float) -> None:
    state.action_elapsed += delta_time
    progress = min(state.action_elapsed / JUMP_DURATION, 1.0)
    state.y = GROUND_Y + 180 * 4 * progress * (1 - progress)
    state.frame_index = min(int(progress * len(JUMP_CLIP.frames)), len(JUMP_CLIP.frames) - 1)
    if progress >= 1.0:
        state.y = GROUND_Y
        enter_phase(state, Phase.ATTACK)


def update_attack(state: AnimationState, delta_time: float) -> None:
    state.action_elapsed += delta_time
    state.frame_index = min(
        int(state.action_elapsed / ATTACK_CLIP.frame_duration),
        len(ATTACK_CLIP.frames) - 1,
    )
    if state.action_elapsed >= ATTACK_DURATION:
        enter_phase(state, Phase.WALK_TO_LEFT)


def update_walk_to_left(state: AnimationState, delta_time: float) -> None:
    state.facing_right = False
    state.x = move_toward(state.x, START_X, WALK_SPEED * delta_time)
    if state.x <= START_X:
        enter_phase(state, Phase.WALK_TO_CENTER)


def update_state(state: AnimationState, delta_time: float) -> None:
    if state.phase is Phase.WALK_TO_CENTER:
        update_walk_to_center(state, delta_time)
    elif state.phase is Phase.JUMP:
        update_jump(state, delta_time)
    elif state.phase is Phase.ATTACK:
        update_attack(state, delta_time)
    else:
        update_walk_to_left(state, delta_time)
    if state.phase in (Phase.WALK_TO_CENTER, Phase.WALK_TO_LEFT):
        advance_frame(state, delta_time)


def render(state: AnimationState, sprite_sheet, grass) -> None:
    draw_scene(grass)
    clip = clip_for_phase(state.phase)
    frame = clip.frames[state.frame_index]
    draw_frame(sprite_sheet, frame, state.x, state.y, state.facing_right)
    update_canvas()


def draw_scene(grass) -> None:
    clear_canvas()
    grass.draw(CANVAS_WIDTH // 2, 150, CANVAS_WIDTH, 100)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        grass = load_image(str(GRASS_PATH))
        validate_clips(sprite_sheet.w, sprite_sheet.h)
        state = AnimationState()
        last_time = perf_counter()
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT or (
                    event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                ):
                    running = False
            if not running:
                break

            current_time = perf_counter()
            delta_time = min(current_time - last_time, 0.05)
            last_time = current_time
            update_state(state, delta_time)
            render(state, sprite_sheet, grass)
            delay(0.01)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()