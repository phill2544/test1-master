import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from .views import send_email, delete_file


def start():
    print('start()')
    scheduler = BackgroundScheduler(timezone='Asia/Bangkok')
    scheduler.add_job(send_email, 'cron', day_of_week='mon-fri', hour=9, minute=30,)
    scheduler.add_job(delete_file, 'cron', day=1, month=1)
    # scheduler.add_job(send_email, 'interval', seconds=2)
    # scheduler.add_job(delete_file, 'interval', seconds=5)
    scheduler.start()
