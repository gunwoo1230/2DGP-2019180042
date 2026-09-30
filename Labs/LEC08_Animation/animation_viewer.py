running = True
frame_count = 0  # 1단계 확인용: 3프레임 후 종료 (2단계에서 제거)


def init():
    print('init')


def handle_events():
    print('handle_events')


def update():
    print('update')


def draw():
    print('draw')


init()
while running:
    handle_events()
    update()
    draw()
    frame_count += 1
    if frame_count >= 3:
        running = False
