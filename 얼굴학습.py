import face_recognition
import os
import pickle

# 학습할 사진이 있는 디렉터리
KNOWN_FACES_DIR = 'known_faces'

# 학습모델
ENCODINGS_FILE = 'encodings.pickle'

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

with open(ENCODINGS_FILE, 'wb') as f:
    pickle.dump((known_faces, known_names), f)

print('학습된 데이터가 저장되었습니다.')