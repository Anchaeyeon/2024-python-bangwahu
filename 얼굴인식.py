import face_recognition
import cv2
import os

# 학습할 사진이 있는 디렉터리
KNOWN_FACES_DIR = 'known_faces'

# 테스트 할 사진 파일
IMAGE_TO_TEST = 'test1.jpg'

TOLERANCE = 0.4
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'

def name_to_color(name):
    return [255, 255, 255]

print('얼굴 학습중')
known_faces = []
known_names = []

# 얼굴 학습
# 폴더 각각 (JHI, LJH)
for name in os.listdir(KNOWN_FACES_DIR):
    # 폴더 안의 파일 (정해인1, 정해인2, ...)
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        # 이미지 불러오기
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        # 이미지 중에서 얼굴만 추출
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print('학습 끝. 얼굴인식 시작!')

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