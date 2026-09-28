# 실습6. 원 -> 사각형 -> 삼각형 운동 (끊김 없는 버전)

import math
from pico2d import *

WIDTH, HEIGHT = 800, 600
SPEED = 5            # 한 프레임에 움직이는 거리(px)
FRAME_TIME = 0.01

CIRCLE_CX, CIRCLE_CY = 400, 300
CIRCLE_R = 200

RECT_LEFT, RECT_RIGHT = 50, 750
RECT_BOTTOM, RECT_TOP = 100, 500

TRI_TOP = (400, 500)
TRI_RIGHT = (700, 100)
TRI_LEFT = (100, 100)

# 원의 맨 아래 점. 사각형 밑변과 삼각형 밑변 위에도 있어서
# 세 도형 모두 여기서 출발해 여기로 돌아오면 도형이 바뀔 때 끊기지 않는다.
START = (CIRCLE_CX, CIRCLE_CY - CIRCLE_R)

running = True


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    handle_events()
    delay(FRAME_TIME)


def move_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    steps = max(1, round(math.dist(p1, p2) / SPEED))

    # i = 0(시작점)은 앞 구간의 끝점으로 이미 그렸으므로 1부터 시작
    for i in range(1, steps + 1):
        if not running:
            return
        t = i / steps
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2
        draw_character(x, y)


def move_path(points):
    for p1, p2 in zip(points, points[1:]):
        move_line(p1, p2)


def move_circle():
    steps = round(2 * math.pi * CIRCLE_R / SPEED)
    start_angle = -math.pi / 2  # START(원의 맨 아래)에서 출발

    for i in range(1, steps + 1):
        if not running:
            return
        theta = start_angle + 2 * math.pi * i / steps
        x = CIRCLE_CX + CIRCLE_R * math.cos(theta)
        y = CIRCLE_CY + CIRCLE_R * math.sin(theta)
        draw_character(x, y)


def move_rectangle():
    move_path([
        START,
        (RECT_RIGHT, RECT_BOTTOM),
        (RECT_RIGHT, RECT_TOP),
        (RECT_LEFT, RECT_TOP),
        (RECT_LEFT, RECT_BOTTOM),
        START,
    ])


def move_triangle():
    move_path([START, TRI_RIGHT, TRI_TOP, TRI_LEFT, START])


open_canvas(WIDTH, HEIGHT)
character = load_image('character.png')

while running:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()
