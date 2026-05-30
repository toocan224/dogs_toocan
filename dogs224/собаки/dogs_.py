import os
import subprocess
import json
from datetime import datetime
import cv2
import shagoviy
import time
import enum
#from model import prediction, model_initialization
import sounddevice as sd
import soundfile as sf
from ffpyplayer.player import MediaPlayer

class dogpos(enum.Enum):
    sit = 1
    stand = 2
    lay = 3
    none = 4
REPORTS_FILE = 'training_reports.json'

# import the inference-sdk
'''from inference_sdk import InferenceHTTPClient

# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=""
)
'''


from inference import get_model

# Uses cached weights for on-device inference
model = get_model(
    model_id="toocandogs/4",
    api_key="Wb68uTXkugSzoRdiNY5P"
)

def play_video_with_audio(position):
    video_path = f"/home/ilya/dogs_toocan/dogs224/собаки/{position}_video.mp4"
    if not os.path.exists(video_path):
        print(f"Видео {video_path} не найдено!")
        return
    
    # ... внутри функции play_video_with_audio ...
    my_env = os.environ.copy()
    my_env["DISPLAY"] = ":0" # Указывает на основной экран малинки

   
#    cmd = [
#        "cvlc", "-I", "dummy", "--play-and-exit", 
#        "--fullscreen", "--no-video-title-show", 
#        video_path
#    ]
    print(f"Запускаю видео для атлетов: {position}")
    try:
#       subprocess.run([
#            "cvlc", "-I","dummy","--fullscreen", "--play-and-exit", "--no-video-title-show", video_path
#        ], check=True)
        # Вместо cvlc используй это в subprocess:
        subprocess.run(["mpv", "--fs", "--vo=gpu", "--hwdec=auto", video_path])
    except Exception as e:
        print(f"Ошибка плеера: {e}")
    time.sleep(3)

def log_training_result(training_id, command, is_success, duration):
    new_report = {
        "SessionId": training_id,
        "DateTime": datetime.now().isoformat(),
        "Command": command,
        "IsSuccess": is_success,
        "DurationSeconds": round(duration, 2)
    }
    try:  
        try:
            with open(REPORTS_FILE, 'r') as f:
                reports = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            reports = []
        reports.append(new_report)
        with open(REPORTS_FILE, 'w') as f:
            json.dump(reports, f, indent=4)
        print(f"Аналитика сохранена: Success={is_success}")
    except Exception as e:
        print(f"Ошибка сохранения аналитики: {e}")


dog_position = dogpos.none
print(dog_position.name)
#AIMODEL = model_initialization()
#print(AIMODEL)


def sound_play(command):
    file_path = f"/home/ilya/dogs_toocan/dogs224/собаки/{command}.wav"
    # Запускаем системный плеер. Он надежнее и не требует настройки форматов в Python
    subprocess.run(["aplay", file_path])

def sound_rec(command):
    duration = 3
    sample_rate = 44100
    print("Запись началась...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    sf.write(f"{command.name}.wav", audio_data, sample_rate)
    print(f"Запись сохранена в {command.name}.name")

def scan_of_dogs(needed_position, training_id):
    shagoviy.motor_on()
    is_success = False
    sound_play("umka")
    sound_play("umka")
    # 1. Голос команды
    sound_play(needed_position)
    
    # 2. Видео-инструкция (теперь не зависнет)
    play_video_with_audio(needed_position)

    sound_play(needed_position)
    
    global dog_position
    start_time = time.time()
    
    cap = cv2.VideoCapture(0)
    # Настройка разрешения для скорости
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру.")
        return

    try:
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 180:
                print("Время вышло, собаки не справились.")
                break
            
            ret, frame = cap.read()
            if not ret:
                continue

            # 3. ПРЯМОЙ ИНФЕРЕНС (без записи на диск!)
            # Передаем frame напрямую, это в 10 раз быстрее
            result = model.infer(frame, confidence = 0.4)[0] # inference возвращает список для батча
            print(result)
            try:
                # В локальном inference структура ответа чуть отличается
                if len(result.predictions) > 0:
                    dog_position = result.predictions[0].class_name
                    confidence  = result.predictions[0].confidence
                    print(f"Вижу позу: {dog_position}, Уверенность: {confidence}")
                else:
                    print("Не вижу собак")
                    dog_position = "none"
            except Exception:
                dog_position = "none"
            
            if dog_position == needed_position:
                print('УСПЕШНО! Выдаю вкусняшку.')
                shagoviy.vibromove(5)
                is_success = True
                cv2.imwrite(f'photo_{training_id}.jpg', frame)
                break

            # Небольшая пауза, чтобы не перегреть проц
            time.sleep(2)
            
    finally:
        cap.release()
        shagoviy.motor_off()
        total_duration = time.time() - start_time
        log_training_result(training_id, needed_position, is_success, total_duration)
'''

def scan_of_dogs(needed_position):
    shagoviy.motor_on()
    is_success = False
    sound_play(needed_position)
    play_video_with_audio(needed_position)
    global dog_position
    start_time = time.time()
    checking_time = 0
    cap = cv2.VideoCapture(0)  # 0 — это индекс камеры
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру.")
    photo_count = 0
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 180: #собаки тупят>3минут оффаем
            break
        if dog_position == needed_position:
            print('УСПЕШНО')
            shagoviy.vibromove(5)
            shagoviy.motor_off()
            is_success = True
            break
        # Сохранение кадра в файл
        ret, frame = cap.read()
        photo_name = "photo_.jpg"
        cv2.imwrite(photo_name, frame)
        print(f"Сохранено фото: photo_")
        photo_count+=1
        result = model.infer(photo_name)
        try:
            dog_position = (((result['predictions'])[0])['class'])
            print(dog_position)
        except IndexError:
            dog_position = dogpos.none.name
        # dog_position = (((scan_predict['predictions'])[0])['class_id'])
        time.sleep(0.3)
        checking_time += 0.4
        #cv2.destroyAllWindows()
    textfile = open('dog.txt', 'w')
    cap.release()
    print("Камера освобождена. Завершение работы.")
    total_duration = time.time() - start_time
    log_training_result(needed_position, is_success, total_duration)
'''
if __name__ == '__main__':
    scan_of_dogs(dogpos.sit.name, 1)

