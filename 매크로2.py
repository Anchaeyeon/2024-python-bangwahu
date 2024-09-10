import pyautogui
import subprocess
import time
import pyperclip

#잠시 대기 (메모장이 열릴 때까지 대기)
time.sleep(5)

#메모장 실행
subprocess.Popen(['notepad.exe'])

#잠시 대기 (메모장이 열릴 때까지 대기)
time.sleep(2)

#메모장에 멘트 입력
ment = ('깜짝 놀랐지?'
        '하지만 이렇게 예고 없이 찾아오는 놀라움들이 때론 우리의 하루를 특별하게 만들어주는 법이야!'
        '이제 웃으며 하루를 시작해봐!')

#클립보드에 한글 텍스트 복사
pyperclip.copy(ment)

pyautogui.hotkey('ctrl', 'v')