import serial
import time
baud_rate = 9600
arduino = serial.Serial('COM5', baud_rate, timeout=1)
time.sleep(2)  # Ожидание инициализации

# Настройки порта (замените 'COM3' на ваш порт Arduino)
# arduino_port = 'COM5'
def arduino_signal(arduino_port):


    try:


        with open('dog.txt') as file:
                line = file.readline().strip()  # Удаляем пробелы и переводы строк
                if line in ('0', '1'):
                    arduino.write(line.encode())
                    print(f"Sent: {line}")
                    time.sleep(0.5)  # Пауза для обработки Arduino
                else:
                    print(f"Ignored: '{line}' (not 0 or 1)")

    except Exception as e:
        print(f"Error: {e}")

        file.close()
while __name__ == "__main__":
    arduino_signal('COM5')
    time.sleep(1)
'''
'''