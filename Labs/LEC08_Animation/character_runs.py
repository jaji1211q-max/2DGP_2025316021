from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

# fill here

def run_left():
    frame_x = 0
    frame_y = 0
    for x in range(800,5,-5):
        clear_canvas()
        grass.draw(400,30)
        character.clip_draw(
            frame_x * 100, 0,
            100, 100,
            x, 100,
            100, 100
        )
        update_canvas()
    
        frame_x = (frame_x + 1) % 8
        delay(0.01)

def stay_left():
    stay_x = 0
    stay_y = 2
    y = 0
    while y < 50:
        clear_canvas()
        grass.draw(400,30)
        character.clip_draw(
            stay_x*100,stay_y*100,
            100,100,
            10,100
            ,100,100
        )
        update_canvas()
        stay_x = (stay_x + 1)%8
        y += 1
        delay(0.01)
       


run_left()
stay_left()
    


close_canvas()
