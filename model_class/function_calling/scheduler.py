from apscheduler.schedulers.background import BackgroundScheduler

# Function to execute
def scheduled_appointment(*args):
    print(f"Chào bạn, \n Bạn có lịch hẹn với {args[0]}")

def scheduled_remind(*args):
    print(f"Nhắc nhở bạn đã tới giờ {args[0]}")

class Scheduler_chatbot:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()
        self.start_scheduler()
        
    def start_scheduler(self):
        self.scheduler.start()
        
    def shutdown_scheduler(self):
        self.scheduler.shutdown()
        
    def add_job(self, action, function, args):
        self.scheduler.pause()
        self.scheduler.add_job(function, 'date', run_date=action.datetime, args=args)
        self.scheduler.resume()
        
    def remove_job(self, input_id):
        self.scheduler.remove_job(input_id)
        
    def get_jobs(self):
        jobs = self.scheduler.get_jobs()
        return jobs
