import face_recognition
import cv2
import os
import pickle

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

        self.pixmap = None
        self.current_image_path = None

        # 메뉴바 설정
        self.create_menu()

        self.ENCODINGS_FILE = 'encodings.pickle'

        # 테스트 할 사진 파일
        self.IMAGE_TO_TEST = 'test1.jpg'

        self.TOLERANCE = 0.4
        self.FRAME_THICKNESS = 3
        self.FONT_THICKNESS = 2
        self.MODEL = 'cnn'

        # 학습 데이터 불러오기
        with open(self.ENCODINGS_FILE, 'rb') as f:
            self.known_faces, self.known_names = pickle.load(f)

        print('얼굴인식 시작!')

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
        self.current_image_path = file_path
        # 현재 QLable의 크기를 얻음
        label_size = self.label.size()
        # 이미지의 비율을 유지하면서 앱 크기(800, 600)에 맞게 스케일 조정
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        # 얼굴인식 실행
        self.perform_face_recognition()

    def name_to_color(self, name):
        return [255, 255, 255]

    def perform_face_recognition(self):
        if self.current_image_path:
            # 테스트 이미지 로드
            test_image = face_recognition.load_image_file(self.IMAGE_TO_TEST)

            # 테스트 이미지에서 얼굴 추출
            locations = face_recognition.face_locations(test_image)
            encodings = face_recognition.face_encodings(test_image, locations)

            test_image = cv2.cvtColor(test_image, cv2.COLOR_BGRA2BGR)

            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(self.known_faces, face_encoding, self.TOLERANCE)
                match = None
                if True in results:
                    match = self.known_names[results.index(True)]
                    print(f'-{match} from {results}')

                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                    color = self.name_to_color(match)
                    cv2.rectangle(test_image, top_left, bottom_right, color, self.FRAME_THICKNESS)
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)
                    cv2.rectangle(test_image, top_left, bottom_right, color, cv2.FILLED)
                    cv2.putText(test_image, match, (face_location[3] + 10, face_location[2] + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (200, 200, 200), self.FONT_THICKNESS)

            cv2.imshow('face recognition', test_image)
            cv2.waitKey()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ImageWindow()

    window.show()
    sys.exit(app.exec_())
