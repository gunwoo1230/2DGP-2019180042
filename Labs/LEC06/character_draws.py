# 실습 과제 진행

import math
from pico2d import *

open_canvas(800,600)

character = load_image('character.png')

CIRCLE_CX, CIRCLE_CY = 400, 300
CIRCLE_R = 200

RECT_LEFT, RECT_RIGHT = 50, 750
RECT_BOTTOM, RECT_TOP = 100, 500

TRI_TOP = (400, 500)
TRI_RIGHT = (700, 100)
TRI_LEFT = (100, 100)

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.05)

def move_circle():
    print("원 이동")

    for degree in range(0, 360, 5):
        theta = math.radians(degree)
        x = CIRCLE_CX + CIRCLE_R * math.cos(theta)
        y = CIRCLE_CY + CIRCLE_R * math.sin(theta)
        draw_character(x, y)

def move_top():
    print("위 이동")

    for x in range(RECT_LEFT, RECT_RIGHT, 5):
        draw_character(x, RECT_TOP)

def move_right():
    print("오른쪽 이동")

    for y in range(RECT_TOP, RECT_BOTTOM, -5):
        draw_character(RECT_RIGHT, y)

def move_bottom():
    print("아래 이동")

    for x in range(RECT_RIGHT, RECT_LEFT, -5):
        draw_character(x, RECT_BOTTOM)

def move_left():
    print("왼쪽 이동")

    for y in range(RECT_BOTTOM, RECT_TOP, 5):
        draw_character(RECT_LEFT, y)


def move_rectangle():
    print("사각형 이동")

    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    for i in range(0, 100 + 1, 2):
        t = i / 100
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2
        draw_character(x, y)


def move_triangle_bottom():
    print("삼각형 아래 이동")

    move_line(TRI_RIGHT, TRI_LEFT)
    
    pass

def move_triangle_left():
    print("삼각형 왼쪽 이동")
    
    move_line(TRI_LEFT, TRI_TOP)

def move_triangle_right():
    print("삼각형 오른쪽 이동")

    move_line(TRI_TOP, TRI_RIGHT)

def move_triangle():
    print("삼각형 이동")

    move_triangle_bottom()
    move_triangle_left()
    move_triangle_right()
    pass

while True:
    #move_circle()
    #move_rectangle()
    move_triangle()
    break

close_canvas()