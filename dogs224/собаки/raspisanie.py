import schedule
import time
import json
import os

DATA_FILE = "trainingData.json"
last_modified_time = 0

def run_training(training_id, training_type):
    print(f"[{time.strftime('%H:%M:%S')}] {training_type} (ID: {training_id})")
    

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