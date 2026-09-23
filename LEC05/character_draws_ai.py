import math

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DELAY = 0.01


def draw_character(x, y):
	clear_canvas()
	character.draw(x, y)
	update_canvas()
	delay(FRAME_DELAY)


def move_circle():
	center_x, center_y = 400, 330
	radius_x, radius_y = 240, 170

	for degree in range(360):
		angle = math.radians(degree)
		x = center_x + radius_x * math.cos(angle)
		y = center_y + radius_y * math.sin(angle)
		draw_character(x, y)


def move_rectangle():
	left, right = 90, 710
	bottom, top = 100, 500
	step = 5

	for x in range(left, right + 1, step):
		draw_character(x, top)
	for y in range(top, bottom - 1, -step):
		draw_character(right, y)
	for x in range(right, left - 1, -step):
		draw_character(x, bottom)
	for y in range(bottom, top + 1, step):
		draw_character(left, y)


def move_triangle():
	points = ((140, 120), (660, 120), (400, 500), (140, 120))

	for start, end in zip(points, points[1:]):
		move_line(start, end)


def move_line(start, end):
	start_x, start_y = start
	end_x, end_y = end
	distance = math.hypot(end_x - start_x, end_y - start_y)
	steps = max(1, int(distance / 5))

	for step in range(steps + 1):
		progress = step / steps
		x = start_x + (end_x - start_x) * progress
		y = start_y + (end_y - start_y) * progress
		draw_character(x, y)


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
character = load_image('character.png')

while True:
	move_circle()
	move_rectangle()
	move_triangle()


close_canvas()
