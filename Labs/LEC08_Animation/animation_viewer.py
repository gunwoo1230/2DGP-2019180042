from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 640
GRASS_CENTER_Y = 30  # grass.png(높이 62)의 맨 아래 투명 1줄을 화면 밖으로 내림
GROUND_Y = 52        # 발판 잔디 윗면. 캐릭터 발(프레임 아래 변)이 놓이는 높이

# 프레임 = 시트 좌상단 기준 (x, y, w, h). 알파 경계로 타이트하게 잘라 프레임마다 크기가 다르다.
RUN_FRAMES = [
    (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38), (97, 80, 37, 37),
    (135, 80, 32, 35), (170, 79, 32, 38), (206, 79, 26, 38), (238, 80, 24, 37),
    (263, 80, 30, 37), (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
]
ROLL_FRAMES = [
    (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
    (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
]
BALANCE_FRAMES = [
    (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44), (90, 327, 25, 43),
    (119, 327, 25, 43), (149, 327, 20, 44), (184, 341, 40, 28), (232, 341, 39, 27),
]
DIZZY_FRAMES = [
    (6, 429, 34, 40), (49, 426, 34, 43), (96, 427, 23, 39), (125, 427, 23, 39),
]

# 재생 순서대로 (이름, 프레임 리스트). 프레임 수는 len()으로만 다룬다.
ANIMATIONS = [
    ('run', RUN_FRAMES),
    ('roll', ROLL_FRAMES),
    ('balance', BALANCE_FRAMES),
    ('dizzy', DIZZY_FRAMES),
]

running = True
background = None
ground = None
sheet = None


def init():
    global background, ground, sheet
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    hide_lattice()
    background = load_image('TUK_GROUND.png')
    ground = load_image('grass.png')
    sheet = load_image('sonic-sprite.png')
    for name, frames in ANIMATIONS:  # 확인용 출력 (다음 단계에서 제거)
        print(name, len(frames))


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
