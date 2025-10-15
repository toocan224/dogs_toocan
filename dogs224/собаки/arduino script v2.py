import serial
import time
import os


def arduino_signal(arduino_port):
    baud_rate = 9600
    last_modified = 0  # Время последнего изменения файла
    last_value = None  # Последнее отправленное значение

    try:
        arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)

        while True:
            # Проверяем время изменения файла
            current_modified = os.path.getmtime('dog.txt')

            if current_modified != last_modified:
                with open('dog.txt') as file:
                    line = file.read().strip()

                if line in ('0', '1'):
                    if line != last_value:  # Отправляем только новые значения
                        arduino.write(line.encode())
                        print(f"Sent: {line}")
                        last_value = line
                else:
                    print(f"Ignored: '{line}' (not 0 or 1)")

                last_modified = current_modified

            time.sleep(0.1)  # Проверка каждые 500 мс

    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    finally:
        if 'arduino' in locals():
            arduino.close()
arduino_signal('COM5')