from apscheduler.schedulers.background import BackgroundScheduler
from .scheduled_sms import send_reminder
import os


def start():
    if os.environ.get('RUN_MAIN'):
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_reminder, 'interval', minutes=30)
        scheduler.start()