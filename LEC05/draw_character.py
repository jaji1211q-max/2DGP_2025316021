def move_circle():
    pass

def move_rectangle():
    pass

def move_triangle():
    pass


from pico2d import *

open_canvas(800, 600)
boy = load_image('character.png')

clear_canvas()
boy.draw(400, 300)
update_canvas()
delay(1)
close_canvas()

