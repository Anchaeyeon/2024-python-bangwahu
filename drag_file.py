import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 창의 제목을 설정
        self.setWindowTitle('사진 끌어오기')
        # 창의 크기와 위치 설정 (x, y, width, height)
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel('여기에 사진을 drag 하세요', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        # 드래그 앤 드랍 활성화
        self.setAcceptDrops(True)

        # 메뉴바 설정
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        # 파일 메뉴 생성
        file_menu = menu_bar.addMenu('파일')

        # '이미지 열기' 액션을 추가
        open_action = QAction('이미지 열기', self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        # '종료' 액션 추가
        exit_action = QAction('종료', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_image(self):
        # 대화상자를 열고 이미지 파일 선택
        file_path, _ = QFileDialog.getOpenFileName(self, '이미지 파일 열기', '', '이미지 파일 (*.png;*.jpg;*.jpeg;*.bmp;*.gif)')
        if file_path:
            self.load_image(file_path)

    # 드래그 이벤트 처리
    def dragEnterEvent(self, event):
        # 드래그 된 데이터에 파일이 있는지 확인
        if event.mimeData().hasUrls():
            # 드래그 동작 허용
            event.acceptProposedAction()

    # 드랍 이벤트 처리
    def dropEvent(self, event):
        # 드랍된 모든 파일 URL에 대해 반복 처리
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()

            # 이미지 파일 확장자 체크
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.load_image(file_path)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        # 현재 QLable의 크기를 얻음
        label_size = self.label.size()
        # 이미지의 비율을 유지하면서 앱 크기(800, 600)에 맞게 스케일 조정
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ImageWindow()

    window.show()
    sys.exit(app.exec_())