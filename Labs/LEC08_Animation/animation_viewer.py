# Drill #8 애니메이션 뷰어
# 소닉 스프라이트 시트의 4종 애니메이션(run, roll, balance, dizzy)을 화면 중앙에서
# 각각 5회 반복 → 1초 정지 → 다음 순으로 무한 재생한다. ESC 또는 창 닫기로 종료.

import os
import sys
from pico2d import *

BACKGROUND_FILE = 'TUK_GROUND.png'
GROUND_FILE = 'grass.png'
SHEET_FILE = 'sonic-sprite.png'

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 640
GRASS_CENTER_Y = 30  # grass.png(높이 62)의 맨 아래 투명 1줄을 화면 밖으로 내림
GROUND_Y = 52        # 발판 잔디 윗면. 캐릭터 발(프레임 아래 변)이 놓이는 높이
CHARACTER_HEIGHT = 340  # 애니메이션의 가장 큰 프레임이 화면에서 차지할 높이 (640의 절반 이상)
FRAME_TIME = 0.08       # 프레임 하나를 보여주는 시간(초)
REPEAT_COUNT = 5        # 애니메이션 하나를 반복하는 횟수
PAUSE_TIME = 1.0        # 반복을 마친 뒤 정지하는 시간(초)

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
player = None


class Animation:
    def __init__(self, name, frames, sheet):
        self.name = name
        self.frames = frames  # [(x, y, w, h), ...] 프레임마다 크기가 다르다
        self.sheet = sheet
        # 배율은 애니메이션마다 한 번만 계산해 모든 프레임에 같이 쓴다. (프레임마다 바꾸면 캐릭터가 떨린다)
        self.scale = CHARACTER_HEIGHT / max(h for _, _, _, h in frames)

    def draw(self, index, x, foot_y):
        fx, fy, fw, fh = self.frames[index]
        bottom = self.sheet.h - fy - fh  # 시트 좌상단 기준 y → pico2d 좌하단 기준 bottom
        w, h = fw * self.scale, fh * self.scale
        # clip_draw는 중심 기준이므로, 아래 변이 foot_y에 오도록 중심을 h/2만큼 올린다.
        self.sheet.clip_draw(fx, bottom, fw, fh, x, foot_y + h / 2, w, h)


class AnimationPlayer:
    """애니메이션 목록을 차례로 REPEAT_COUNT회 반복 → PAUSE_TIME 정지 → 다음 순으로 무한 재생한다."""

    def __init__(self, animations):
        self.animations = animations
        self.anim_index = 0     # 재생 중인 애니메이션
        self.frame_index = 0    # 그 애니메이션의 현재 프레임
        self.loop_count = 0     # 현재 애니메이션을 끝까지 재생한 횟수
        self.play_start = get_time()  # 현재 애니메이션 재생을 시작한 시각

    def update(self):
        frames = self.animations[self.anim_index].frames
        elapsed = get_time() - self.play_start
        # 루프 속도와 상관없이 경과 시간으로 프레임을 정한다.
        step = int(elapsed / FRAME_TIME)  # 시작 후 지나간 프레임 수
        self.frame_index = step % len(frames)
        self.loop_count = step // len(frames)  # 마지막 프레임을 지나 0번으로 돌아올 때마다 1 증가
        if self.loop_count >= REPEAT_COUNT:    # 5회 반복을 마치면 정지. 정지 중에는 첫 프레임을 보여준다
            self.frame_index = 0
            pause_elapsed = elapsed - REPEAT_COUNT * len(frames) * FRAME_TIME
            if pause_elapsed >= PAUSE_TIME:  # 정지 시간이 지나면 다음 애니메이션으로 (마지막 다음은 처음)
                self.anim_index = (self.anim_index + 1) % len(self.animations)
                self.play_start = get_time()

    def draw(self, x, foot_y):
        self.animations[self.anim_index].draw(self.frame_index, x, foot_y)


def find_missing_resources():
    return [f for f in (BACKGROUND_FILE, GROUND_FILE, SHEET_FILE) if not os.path.isfile(f)]


def init():
    global background, ground, player
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    hide_lattice()
    background = load_image(BACKGROUND_FILE)
    ground = load_image(GROUND_FILE)
    sheet = load_image(SHEET_FILE)
    player = AnimationPlayer([Animation(name, frames, sheet) for name, frames in ANIMATIONS])


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def update():
    player.update()


def draw():
    clear_canvas()
    background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, CANVAS_WIDTH, CANVAS_HEIGHT)
    ground.draw(CANVAS_WIDTH // 2, GRASS_CENTER_Y)
    player.draw(CANVAS_WIDTH // 2, GROUND_Y)
    update_canvas()


# 메인
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 어디서 실행해도 이 파일 옆의 리소스를 찾도록
missing = find_missing_resources()
if missing:  # 창을 열기 전에 확인해, 빈 창이 뜨거나 알 수 없는 OSError로 죽지 않게 한다
    print('[오류] 리소스 파일을 찾을 수 없습니다:')
    for f in missing:
        print('  -', os.path.join(os.getcwd(), f))
    print('animation_viewer.py와 같은 폴더에 위 파일을 넣은 뒤 다시 실행하세요.')
    sys.exit(1)
try:
    init()
except OSError:  # 파일은 있지만 이미지로 읽을 수 없는 경우 (손상된 파일 등)
    close_canvas()
    print('[오류] 이미지를 불러오지 못했습니다. 리소스 파일이 손상되지 않았는지 확인하세요.')
    sys.exit(1)
while running:
    handle_events()
    update()
    draw()
    delay(0.01)
close_canvas()
