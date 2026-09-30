from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 640

running = True


def init():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    hide_lattice()


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


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
close_canvas()
