#!/bin/bash
export DISPLAY=:0
# Прямой путь, который у тебя сработал:
export XAUTHORITY=/run/user/1000/gdm/Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
export GPIOZERO_PIN_FACTORY=lgpio

# Запуск с сохранением переменных окружения
sudo -E /home/ilya/dogs_toocan/dogs224/собаки/yolovenv/bin/python3 /home/ilya/dogs_toocan/dogs224/собаки/dogs_.py
