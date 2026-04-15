import gpiozero
from time import sleep

# Используем альтернативный метод управления
step = gpiozero.LED(5) # Используем как LED для простоты
direction = gpiozero.LED(4)

direction.on() # Направление

print("Начинаю агрессивный тест...")
try:
    while True:
        step.on()
        sleep(0.05) # Очень длинный импульс (50мс)
        step.off()
        sleep(0.05)
        print("Импульс отправлен")
except KeyboardInterrupt:
    print("Стоп")

class kormushka:
    step = 0
    direction = 0
    def __init__(self,step , direction):
        self.step = step
        self.direction = direction
    def give(self, stepstime):
        step.on()
        for i in range(stepstime//0.05):
            direction.on()
            sleep(0.1) # Очень длинный импульс (50мс)
            direction.off()
            sleep(0.05)
        step.off()

        

        

kkk = kormushka(1,1)
print(kkk.step)
