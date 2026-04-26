import schedule
import time
import json
import os
import dogs_

DATA_FILE = "trainingData.json"
last_modified_time = 0

def run_training(training_id, training_type):
    # 1. training_type из JSON — это строка (например, "sit").
    # Чтобы превратить её в Enum (если нужно), используем dogs_.dogpos[training_type]
    try:
        position = dogs_.dogpos[training_type]
    except KeyError:
        print(f"Ошибка: Тип тренировки '{training_type}' не найден в Enum!")
        return

    # 2. Теперь training_id официально в руках!
    print(f"[{time.strftime('%H:%M:%S')}] Начинаем: {training_type} (ID в базе: {training_id})")
    
    # 3. Пробрасываем ID дальше в сканер, чтобы он улетел в аналитику
    dogs_.scan_of_dogs(position, training_id)
def reload_if_changed():
    global last_modified_time
    
    if not os.path.exists(DATA_FILE):
        return
    current_mtime = os.path.getmtime(DATA_FILE)
    if current_mtime > last_modified_time:
        print("Файл изменился")
        schedule.clear('training')
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                for item in data:
                    schedule.every().day.at(item['StartTime']).do(
                        run_training, 
                        training_id=item['Id'], 
                        training_type=item['TrainingType']
                    ).tag('training')
            
            last_modified_time = current_mtime
            print(f"Загружено задач: {len(data)}")
        except Exception as e:
            print(f"Ошибка чтения JSON: {e}")


reload_if_changed()

while True:
    
    reload_if_changed()
    
    schedule.run_pending()
    time.sleep(1)