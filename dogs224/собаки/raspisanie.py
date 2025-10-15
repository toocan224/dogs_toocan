import schedule
import time
from dogs_ import sound_play,dogpos
schedule.every().hour.at(":51").do(lambda : sound_play(dogpos.sit))
# по запуску программы

while True:

    schedule.run_pending()
    time.sleep(1)