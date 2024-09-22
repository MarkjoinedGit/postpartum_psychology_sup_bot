import instructor
from pydantic import BaseModel
from datetime import datetime, timedelta
from openai import OpenAI
from zoneinfo import ZoneInfo
import unicodedata
from function_calling.scheduler import Scheduler_chatbot
class TakeActionIntructor:
    def __init__(self) -> None:
        llm = OpenAI(
            api_key="lamacpp", 
            base_url="http://zep.hcmute.fit/7500/v1",  
        )
        self.client = instructor.patch(client=llm)
        self.list_keyword = ["appointment", "remind", "help"]
        self.context = {
            "appointment" : " (Thời gian tính theo ngày giờ Việt Nam, timezone Asia/Ho_Chi_Minh)",
            "remind" : " (Thời gian tính theo ngày giờ Việt Nam, timezone Asia/Ho_Chi_Minh)"
        }
        self.action_class = {
            "appointment" : self.AppointmentDetail,
            "remind" : self.RemindDetail
        }
        self.scheduler = Scheduler_chatbot()
        
    class AppointmentDetail(BaseModel):
        datetime: datetime
        appointment_with: str
        def to_string(self, remind_now = False):
            if remind_now:
                s = "Hi"
            else:
                s = "Okie"
            return f"{s}, hiện tại bạn có lịch hẹn : \n 📆Thời gian: {self.datetime} \n 👨🏼‍⚕️Hẹn với: {self.appointment_with}"

    class RemindDetail(BaseModel):
        datetime: datetime 
        remind_description: str
        def to_string(self, remind_now = False):
            if remind_now:
                s = "Hi👋🏼"
            else:
                s = "Okie👌🏼"
            return f"{s}, hiện tại bạn có lịch nhắc nhở: \n 📆Thời gian: {self.datetime} \n 📋Nội dung: {self.remind_description}"

    class Help():
        help: str = "Chức năng hỗ trợ: \n👉🏼 appointment: Lịch hẹn <cú pháp: 'appointment + datetime + appointment_with'> \nVí dụ: 'appointment Hẹn với bác sĩ Khoa vào 8h30 ngày mai nha' or 'appointment Hẹn với chatbot vào 8h30 ngày 21/9 nha' \n👉🏼 remind: Nhắc nhở <cú pháp: 'remind + datetime + description'> \nVí dụ: 'remind Nhắc nhở tôi 20h hôm nay pha sữa cho con' or 'remind Nhớ nói chuyện với chồng vào lúc 8h30 21/9'\n👉🏼 help: Trợ giúp"
        def to_string(self):
            return self.help

    def add_job_scheduler(self, action, function, args):
        self.scheduler.add_job(action, function, args)

    def check_extract_keyword(self, input_string):
        for keyword in self.list_keyword:
            if input_string.lower().startswith(keyword):
                self.keyword = keyword
                return True, input_string[len(self.keyword):].strip()
        return False, input_string
    
    def take_action(self, input_string):
        check, s = self.check_extract_keyword(input_string)
        if not check:
            print("Keyword not found")
            return None
        elif self.keyword == "help":
            return self.Help()

        action = self.client.chat.completions.create(
            model="gemma-2-9b-it",
            response_model=self.action_class[self.keyword],
            messages=[
                {"role": "user", "content": s + self.context[self.keyword]},
            ],
        )
        s = unicodedata.normalize('NFC', s.lower())
        if "ngày mai" in s or "tomorrow" in s:
            action.datetime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 
                                                    action.datetime.hour, action.datetime.minute, 
                                                    0, 0, ZoneInfo("Asia/Ho_Chi_Minh")) + timedelta(days=1)
        elif "hôm nay" in s or "today" in s:
            action.datetime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 
                                                    action.datetime.hour, action.datetime.minute, 
                                                    0, 0, ZoneInfo("Asia/Ho_Chi_Minh"))
        elif((action.datetime.month < datetime.now().month) or 
            (action.datetime.month == datetime.now().month and action.datetime.day < datetime.now().day)):
            action.datetime = action.datetime.replace(year=datetime.now().year + 1)
        elif(action.datetime.month >= datetime.now().month and action.datetime.day >= datetime.now().day):
            action.datetime = action.datetime.replace(year=datetime.now().year)
        return action