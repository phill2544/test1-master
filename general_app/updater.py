import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from .views import send_email, delete_file


def start():
    start_date = datetime.datetime.now().replace(hour=9, minute=30)
    end_date = datetime.datetime.now().replace(hour=9, minute=31)
    print('start()')
    scheduler = BackgroundScheduler()
    # scheduler.add_job(send_email, 'interval', seconds=50, start_date=start_date, end_date=end_date)
    scheduler.add_job(send_email, 'interval', seconds=2)
    # scheduler.add_job(delete_file, 'interval', seconds=1)
    scheduler.start()
