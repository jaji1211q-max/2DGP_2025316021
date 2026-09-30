from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
SPRITE_PATH = Path(__file__).with_name("sprites_fullsize.png")


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