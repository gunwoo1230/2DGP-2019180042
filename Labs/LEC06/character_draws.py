# 실습 과제 진행

import math
from pico2d import *

open_canvas(800,600)

character = load_image('character.png')

CIRCLE_CX, CIRCLE_CY = 400, 300
CIRCLE_R = 200

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.05)

def move_circle():
    print("원 이동")

    for degree in range(0, 360, 5):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        draw_character(x, y)
        
def move_top():
    print("위 이동")

    for x in range(50, 750, 5):
        draw_character(x, 500)

def move_right():
    print("오른쪽 이동")

    for x in range(500, 100, -5):
        draw_character(750, x)

def move_bottom():
    print("아래 이동")

    for x in range(750, 50, -5):
        draw_character(x, 100)

def move_left():
    print("왼쪽 이동")
    
    for x in range(100, 500, 5):
        draw_character(50, x)


def move_rectangle():
    print("사각형 이동")

    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_triangle_bottom():
    print("삼각형 아래 이동")

    x1, y1 = 700, 100
    x2, y2 = 100, 100
    
    for i in range(0, 100 + 1, 2):
        t = i / 100
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2
        draw_character(x, y)
    
    pass

def move_triangle_left():
    print("삼각형 왼쪽 이동")
    
    x1, y1 = 100, 100
    x2, y2 = 400, 500

    for i in range(0, 100 + 1, 2):
        t = i / 100
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2
        draw_character(x, y)
    pass

def move_triangle_right():
    print("삼각형 오른쪽 이동")

    x1, y1 = 400, 500
    x2, y2 = 700, 100

    for i in range(0, 100 + 1, 2):
        t = i / 100
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2
        draw_character(x, y)
    pass

def move_triangle():
    print("삼각형 이동")

    move_triangle_bottom()
    move_triangle_left()
    move_triangle_right()
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    break

close_canvas()