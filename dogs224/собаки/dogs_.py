import json
from datetime import datetime
#import schedule
import cv2

#from random import randint
# import mediapipe
#from shagoviy import kormushka
import time
import enum
from model import prediction, model_initialization
# import PySide6
# import ultralytics
import sounddevice as sd
import soundfile as sf
class dogpos(enum.Enum):
    sit = 1
    stand = 2
    lay = 3
    none = 4
REPORTS_FILE = 'training_reports.json'

def log_training_result(command, is_success, duration):
    new_report = {
        "SessionId": int(time.time()),
        "DateTime": datetime.now().isoformat(),
        "Command": command,
        "IsSuccess": is_success,
        "DurationSeconds": round(duration, 2)
    }
    try:
        # Читаем старые отчеты
        try:
            with open(REPORTS_FILE, 'r') as f:
                reports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            reports = []

        # Добавляем новый и сохраняем
        reports.append(new_report)
        with open(REPORTS_FILE, 'w') as f:
            json.dump(reports, f, indent=4)
        print(f"Аналитика сохранена: Success={is_success}")
    except Exception as e:
        print(f"Ошибка сохранения аналитики: {e}")
dog_position = dogpos.none
print(dog_position.name)
AIMODEL = model_initialization()
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
    start_time = time.time()
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
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 180: # Тайм-аут 3 минуты
            break

        # Сохранение кадра в файл
        photo_name = "photo_.jpg"
        cv2.imwrite(photo_name, frame)
        print(f"Сохранено фото: photo_")
        scan_predict = prediction('photo_.jpg', AIMODEL)
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
    # if dog_position == needed_position:
    #     kormushka.give()
    #     textfile.write('1')
    # else:
    #     textfile.write('0')
    cap.release()
    print("Камера освобождена. Завершение работы.")
    total_duration = time.time() - start_time
    log_training_result(needed_position, is_success, total_duration)
if __name__ == '__main__':
    scan_of_dogs(dogpos.sit.name)