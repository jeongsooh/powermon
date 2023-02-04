# 15분마다 동작하는 Task 프로그램
# run this code with celery -A tasks worker --loglevel=info command in the terminal

from celery import Celery
import datetime

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def alarm():
    while True:
        now = datetime.datetime.now()
        next_alarm = now + datetime.timedelta(minutes=15 - now.minute % 15)
        delta = next_alarm - now
        print('Alarm:', next_alarm.strftime("%H:%M:%S"))
        time.sleep(delta.total_seconds())

# 상기 Task를 15분 마다 구동할 수 있도록 하는 스케쥴러
# run this with celery -A tasks beat --loglevel=info command

from datetime import timedelta

app.conf.beat_schedule = {
    'print_every_15min': {
        'task': 'tasks.alarm',
        'schedule': timedelta(minutes=15),
    },
}
