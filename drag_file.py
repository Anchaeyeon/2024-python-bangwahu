import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
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

    # 드래그 이벤트 처리
    def dragEnterEvent(self, event):
        pass

    # 드랍 이벤트 처리
    def dropEvent(self, event):
        pass

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ImageWindow()

    window.show()
    sys.exit(app.exec_())