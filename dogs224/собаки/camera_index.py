import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"Индекс {i} РАБОТАЕТ")
        else:
            print(f"Индекс {i} открыт, но кадр не читается")
        cap.release()
    else:
        print(f"Индекс {i} недоступен")
