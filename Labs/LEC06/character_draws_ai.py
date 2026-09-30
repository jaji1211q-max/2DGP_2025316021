import math
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DELAY = 0.01
running = True
boy = None


def draw_boy(x, y):
    global running

    for event in get_events():
        if event.type == SDL_QUIT or (
            event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
        ):
            running = False

    if not running:
        return

    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)


def move_segment(start, end, steps=60):
    start_x, start_y = start
    end_x, end_y = end

    for step in range(steps + 1):
        ratio = step / steps
        x = start_x + (end_x - start_x) * ratio
        y = start_y + (end_y - start_y) * ratio
        draw_boy(x, y)


def move_circle():
    center_x = CANVAS_WIDTH / 2
    center_y = CANVAS_HEIGHT / 2
    radius = 200

    for degree in range(0, 360, 5):
        theta = math.radians(degree)
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        draw_boy(x, y)


def move_rectangle():
    corners = ((100, 100), (100, 500), (600, 500), (600, 100), (100, 100))
    for start, end in zip(corners, corners[1:]):
        move_segment(start, end, steps=80)


def move_triangle():
    corners = ((400, 400), (100, 100), (400, 100), (400, 400))
    for start, end in zip(corners, corners[1:]):
        move_segment(start, end)


def main():
    global boy, running

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        boy = load_image(str(Path(__file__).with_name("character.png")))

        while running:
            move_circle()
            move_rectangle()
            move_triangle()
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
