from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 640

running = True
frame_count = 0  # 확인용: 3프레임 후 종료 (종료 처리 구현 후 제거)


def init():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    hide_lattice()


def handle_events():
    pass


def update():
    pass


def draw():
    clear_canvas()
    update_canvas()


init()
while running:
    handle_events()
    update()
    draw()
    delay(0.01)
    frame_count += 1
    if frame_count >= 3:
        running = False
close_canvas()
