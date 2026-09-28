# 실습 과제 진행

import math
from pico2d import *

open_canvas(800,600)

character = load_image('character.png')

def move_top():
    print("위 이동")

    for x in range(50, 750, 5):
        clear_canvas()
        character.draw(x, 500)
        update_canvas()
        delay(0.05)

def move_right():
    print("오른쪽 이동")
    pass

def move_bottom():
    print("아래 이동")
    pass

def move_left():
    print("왼쪽 이동")
    pass

def move_circle():
    print("원 이동")

    for degree in range(0, 360, 5):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.05)

def move_rectangle():
    print("사각형 이동")

    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_triangle():
    print("삼각형 이동")
    pass

while True:
    #move_circle()
    move_rectangle()
    move_triangle()
    break

close_canvas()