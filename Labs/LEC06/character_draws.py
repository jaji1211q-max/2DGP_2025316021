# 실습 과제 진행
import math
from pico2d import *

def move_circle():
   for degree in range(0,360,10):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        draw_boy(x, y)

def move_rectangle():
   # move_top()
   # move_right()
    move_bottom()
    move_left()

def move_top():
    for y in range(200, 500, 5):
        draw_boy(100, y)
    pass

def move_right():
    for x in range(100,600,5):
        draw_boy(x, 500)
    pass

def move_bottom():
    for y in range(500,100,-5):
        draw_boy(600, y)
    pass

def move_left():
    print("left")
    pass

def move_triangle():
    pass

def draw_boy(x,y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.01)
    


open_canvas(800, 600)
boy = load_image('character.png')

while True:
    #move_circle()
    move_rectangle()
    move_triangle()

