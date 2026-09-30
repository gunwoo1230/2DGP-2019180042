from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 640
GRASS_CENTER_Y = 30  # grass.png(높이 62)의 맨 아래 투명 1줄을 화면 밖으로 내림
GROUND_Y = 52        # 발판 잔디 윗면. 캐릭터 발(프레임 아래 변)이 놓이는 높이
CHARACTER_HEIGHT = 340  # 애니메이션의 가장 큰 프레임이 화면에서 차지할 높이 (640의 절반 이상)
FRAME_TIME = 0.08       # 프레임 하나를 보여주는 시간(초)
REPEAT_COUNT = 5        # 애니메이션 하나를 반복하는 횟수

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
scales = {}  # 애니메이션 이름 → 배율. 한 애니메이션 안에서는 같은 배율을 써야 캐릭터가 떨리지 않는다.
anim_index = 0    # ANIMATIONS 중 재생 중인 애니메이션
frame_index = 0   # 그 애니메이션의 현재 프레임
play_start = 0.0  # 현재 애니메이션 재생을 시작한 시각
loop_count = 0    # 현재 애니메이션을 끝까지 재생한 횟수


def calc_scale(frames):
    return CHARACTER_HEIGHT / max(frame[3] for frame in frames)  # frame[3] = 높이


def init():
    global background, ground, sheet, play_start
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    hide_lattice()
    background = load_image('TUK_GROUND.png')
    ground = load_image('grass.png')
    sheet = load_image('sonic-sprite.png')
    for name, frames in ANIMATIONS:
        scales[name] = calc_scale(frames)
    play_start = get_time()


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def update():
    global frame_index, loop_count
    frames = ANIMATIONS[anim_index][1]
    elapsed = get_time() - play_start
    # 루프 속도와 상관없이 경과 시간으로 프레임을 정한다.
    step = int(elapsed / FRAME_TIME)  # 시작 후 지나간 프레임 수
    frame_index = step % len(frames)
    loop_count = step // len(frames)  # 마지막 프레임을 지나 0번으로 돌아올 때마다 1 증가
    if loop_count >= REPEAT_COUNT:    # 5회 반복을 마치면 마지막 프레임에서 멈춘다
        frame_index = len(frames) - 1


def draw_frame(frame, x, foot_y, scale):
    fx, fy, fw, fh = frame
    bottom = sheet.h - fy - fh  # 시트 좌상단 기준 y → pico2d 좌하단 기준 bottom
    w, h = fw * scale, fh * scale
    # clip_draw는 중심 기준이므로, 아래 변이 foot_y에 오도록 중심을 h/2만큼 올린다.
    sheet.clip_draw(fx, bottom, fw, fh, x, foot_y + h / 2, w, h)


def draw():
    clear_canvas()
    background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, CANVAS_WIDTH, CANVAS_HEIGHT)
    ground.draw(CANVAS_WIDTH // 2, GRASS_CENTER_Y)
    name, frames = ANIMATIONS[anim_index]
    draw_frame(frames[frame_index], CANVAS_WIDTH // 2, GROUND_Y, scales[name])
    update_canvas()


init()
while running:
    handle_events()
    update()
    draw()
    delay(0.01)
close_canvas()
