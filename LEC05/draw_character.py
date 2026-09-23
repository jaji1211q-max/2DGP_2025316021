import math
from pico2d import *

def move_circle():
   for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        clear_canvas()
        boy.draw(x, y)
        update_canvas()
        delay(0.01)


def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()

def move_triangle():
    pass


open_canvas(800, 600)
boy = load_image('character.png')

move_circle()

