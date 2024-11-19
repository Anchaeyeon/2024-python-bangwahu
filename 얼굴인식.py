import face_recognition
import cv2
import os
import pickle

ENCODINGS_FILE = 'encodings.pickle'

# 테스트 할 사진 파일
IMAGE_TO_TEST = 'test1.jpg'

TOLERANCE = 0.4
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'

def name_to_color(name):
    return [255, 255, 255]

# 학습 데이터 불러오기
with open(ENCODINGS_FILE, 'rb') as f:
    known_faces, known_names = pickle.load(f)

print('얼굴인식 시작!')

# 테스트 이미지 로드
test_image = face_recognition.load_image_file(IMAGE_TO_TEST)

# 테스트 이미지에서 얼굴 추출
locations = face_recognition.face_locations(test_image)
encodings = face_recognition.face_encodings(test_image, locations)

test_image = cv2.cvtColor(test_image, cv2.COLOR_BGRA2BGR)

for face_encoding, face_location in zip(encodings, locations):
    results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
    match = None
    if True in results:
        match = known_names[results.index(True)]
        print(f'-{match} from {results}')

        top_left = (face_location[3], face_location[0])
        bottom_right = (face_location[1], face_location[2])
        color = name_to_color(match)
        cv2.rectangle(test_image, top_left, bottom_right, color, FRAME_THICKNESS)
        top_left = (face_location[3], face_location[2])
        bottom_right = (face_location[1], face_location[2] + 22)
        cv2.rectangle(test_image, top_left, bottom_right, color, cv2.FILLED)
        cv2.putText(test_image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (200, 200, 200), FONT_THICKNESS)

cv2.imshow('face recognition', test_image)
cv2.waitKey()
cv2.destroyAllWindows()