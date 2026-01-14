import schedule
import cv2
from random import randint
# import mediapipe
import time
import enum
from model import prediction
# import PySide6
# import ultralytics
import sounddevice as sd
import soundfile as sf
class dogpos(enum.Enum):
    sit = 1
    stand = 2
    lay = 3
    none = 4
datafile = open('dog.txt', 'w')
datafile.write('1')
dog_position = dogpos.none
print(dog_position.name)
def sound_play(command):
    audio_data, sample_rate = sf.read(f'{command}.wav')
    sd.play(audio_data, sample_rate)
    sd.wait()
    print("Воспроизведение завершено.")
def sound_rec(command):
    duration = 3
    sample_rate = 44100
    print("Запись началась...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    sf.write(f"{command.name}.wav", audio_data, sample_rate)
    print(f"Запись сохранена в {command.name}.name")


def scan_of_dogs(needed_position):
    sound_play(needed_position)
    global dog_position
    checking_time = 0
    cap = cv2.VideoCapture(0)  # 0 — это индекс камеры
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру.")
        return
    photo_count = 0
    # scan_predict = {'predictions': [
    #     {'x': 0,
    #      'y': 0,
    #      'width': 0,
    #      'height': 0,
    #      'confidence': 0,
    #      'class': 'none',
    #      'class_id': 4,
    #      'detection_id': '',
    #      'image_path': '',
    #      'prediction_type': 'ObjectDetectionModel'}
    # ]
    #     , 'image': {'width': '0', 'height': ''}
    # }
#   ''' (((scan_predict['predictions'])[0])['class_id'])'''
    while not (dog_position == needed_position) or checking_time >= 180:
        # Захват кадра с камеры
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: Не удалось получить кадр.")
            break

        # Сохранение кадра в файл
        photo_name = "photo_.jpg"
        cv2.imwrite(photo_name, frame)
        print(f"Сохранено фото: photo_")
        scan_predict = prediction('photo_.jpg')
        try:
            dog_position = (((scan_predict['predictions'])[0])['class'])
            print(dog_position)
        except IndexError:
            dog_position = dogpos.none.name
        # dog_position = (((scan_predict['predictions'])[0])['class_id'])

        cv2.imshow('Image', frame)
        cv2.waitKey(0)

        # Ожидание 1 секунды
        time.sleep(0.3)
        checking_time += 0.4


        cv2.destroyAllWindows()
    textfile = open('dog.txt', 'w')
    if dog_position == needed_position:
        textfile.write('1')
    else:
        textfile.write('0')
    # Освобождение камеры
    cap.release()
    print("Камера освобождена. Завершение работы.")
if __name__ == '__main__':
    scan_of_dogs(dogpos.sit.name)