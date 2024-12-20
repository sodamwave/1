import time
from datetime import datetime

# 5초마다 현재 시간 출력
while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S (%A)")
    print(current_time)
    time.sleep(5)
