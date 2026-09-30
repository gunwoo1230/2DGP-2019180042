from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 640
GRASS_CENTER_Y = 30  # grass.png(높이 62)의 맨 아래 투명 1줄을 화면 밖으로 내림
GROUND_Y = 52        # 발판 잔디 윗면. 캐릭터 발(프레임 아래 변)이 놓이는 높이

running = True
background = None
ground = None


def init():
    global background, ground
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    hide_lattice()
    background = load_image('TUK_GROUND.png')
    ground = load_image('grass.png')


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
    background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, CANVAS_WIDTH, CANVAS_HEIGHT)
    ground.draw(CANVAS_WIDTH // 2, GRASS_CENTER_Y)
    update_canvas()


init()
while running:
    handle_events()
    update()
    draw()
    delay(0.01)
close_canvas()
