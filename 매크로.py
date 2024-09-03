import pyautogui

# 클릭한 좌표를 설정합니다.
# x, y = 200, 150

# 마우스를 지정한 좌표로 이동합니다.
# pyautogui.moveTo(x, y)

# 마우스를 클릭합니다.
# pyautogui.click()

# 현재 마우스 좌표 가져오기
x, y = pyautogui.position()

# 좌표 출력
print(f"현재 마우스 좌표: ({x}, {y})")

x, y = 1910, -50
pyautogui.moveTo(x, y)
pyautogui.click()
x, y = 1000, 540
pyautogui.moveTo(x, y)
pyautogui.click()