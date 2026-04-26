import json
from datetime import datetime
import cv2
import shagoviy
import time
import enum
from model import prediction, model_initialization
import sounddevice as sd
import soundfile as sf
from ffpyplayer.player import MediaPlayer

class dogpos(enum.Enum):
    sit = 1
    stand = 2
    lay = 3
    none = 4
REPORTS_FILE = 'training_reports.json'



def play_video_with_audio(position):
    video_path = f"{position}_video.mp4"
    player = MediaPlayer(video_path)
    cap = cv2.VideoCapture(video_path)
    
    while True:
        grabbed, frame = cap.read()
        audio_frame, val = player.get_frame()        
        if not grabbed:
            break
            
        if cv2.waitKey(28) & 0xFF == ord('q'):
            break
            
        cv2.imshow('Video', frame)
        
        if val == 'eof':
            break
            
    cap.release()
    cv2.destroyAllWindows()


def log_training_result(command, is_success, duration):
    new_report = {
        "SessionId": int(time.time()),
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
        return
    photo_count = 0
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 180: #собаки тупят>3минут оффаем
            break
        if dog_position == needed_position:
            shagoviy.vibromove(5)
            shagoviy.motor_off()
            is_success = True
        # Сохранение кадра в файл
        photo_name = "photo_.jpg"
        cv2.imwrite(photo_name, frame)
        print(f"Сохранено фото: photo_")
        photo_count+=1
        scan_predict = prediction('photo_.jpg', AIMODEL)
        try:
            dog_position = (((scan_predict['predictions'])[0])['class'])
            print(dog_position)
        except IndexError:
            dog_position = dogpos.none.name
        # dog_position = (((scan_predict['predictions'])[0])['class_id'])

        

        
        time.sleep(0.3)
        checking_time += 0.4


        cv2.destroyAllWindows()
    textfile = open('dog.txt', 'w')
    cap.release()
    print("Камера освобождена. Завершение работы.")
    total_duration = time.time() - start_time
    log_training_result(needed_position, is_success, total_duration)

if __name__ == '__main__':
    scan_of_dogs(dogpos.sit.name)