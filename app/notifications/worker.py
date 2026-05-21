from apscheduler.schedulers.background import BackgroundScheduler
from app.notifications.send_all_user_notifications import send_all_user_notifications

scheduler = BackgroundScheduler()

def start_scheduler(db_session_factory):

    def job():
        send_all_user_notifications(db_session_factory)

    scheduler.add_job(job, "interval", minutes=1)
    scheduler.start()