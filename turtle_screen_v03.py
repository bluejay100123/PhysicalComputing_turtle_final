import pygame
import random
import serial
import serial.tools.list_ports
import time
import win32gui
import win32con
import win32api

# Arduino Leonardo를 HC-06의 명칭 확인 후 교체할 것
def find_hc06_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:    
        print(port)
    user_input = input("Enter COM number: ")
    for port in ports:
        if user_input in port.description:  # HC-06이 장치 설명에 포함되는지 확인
            return port.device
    return None

def make_window_always_on_top():
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,  # Always on top
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
    )

def make_window_transparent():
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

def comm_test(portID: str):
    ser = serial.Serial(portID, 9600, timeout=1)
    time.sleep(2)

    # Pygame 초기화
    pygame.init()

    # 화면 크기 설정 (주 모니터의 전체 화면 크기 가져오기)
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)  # UI를 없애기 위해 NOFRAME 사용
    pygame.display.set_caption("Sensor Turtle Drawer")

    # 배경 색 설정 (투명 효과처럼 느껴지도록 검은색 사용)
    background_color = (0, 0, 0)

    # 거북이 이미지 로드
    turtle_image = pygame.image.load("turtle_img.png")
    turtle_image = pygame.transform.scale(turtle_image, (50, 50))  # 이미지 크기 조정

    make_window_always_on_top()
    make_window_transparent()

    running = True
    last_num = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC 키로 종료
                    running = False

        get_data = ser.readline()
        if get_data:
            try:
                get_data = get_data.decode().strip()
                num = int(get_data)
                if num >= 15:
                    num = 0

                # 센서값이 바뀌었을 때만 화면 갱신
                if num != last_num:
                    last_num = num

                    # 배경 초기화
                    screen.fill(background_color)

                    # 센서값에 따라 랜덤 위치에 거북이 이미지 그리기
                    for _ in range(num*50):
                        x = random.randint(0, screen_width - turtle_image.get_width())
                        y = random.randint(0, screen_height - turtle_image.get_height())
                        screen.blit(turtle_image, (x, y))

                    # 화면 업데이트
                    pygame.display.flip()
            except ValueError:
                pass

    pygame.quit()
    ser.close()

hc06_port = find_hc06_port()
if hc06_port:
    print(f"HC-06 is connected at {hc06_port}")
else:
    print("HC-06 port not found.")

# portID = 'COM4'
comm_test(hc06_port)

