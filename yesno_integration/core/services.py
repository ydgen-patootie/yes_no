import requests
import time
from .models import Answer


class AnswerFromYesno:

    url_to_yesno = 'https://yesno.wtf/api/'
    retries_num = 5
    timeout = 5

    def __init__(self, question_instance):
        self.question_instance = question_instance
        self.success = False
        self.attempt_num = 0
        self.answer_text = None
        self.image_url = None

    def get_answer(self):
        while self.attempt_num < self.retries_num:
            try:
                r = requests.get(self.url_to_yesno, timeout=self.timeout)
            except:
                self.attempt_num += 1
                continue
            if r.status_code == 200:
                data = r.json()
                self.answer_text = data['answer']
                self.image_url = data['image']
                self.success = True
                break
            else:
                self.attempt_num += 1
                time.sleep(self.timeout)

    def save_answer(self):
        ans_object = Answer(question=self.question_instance,
                            answer_text=self.answer_text,
                            image_url=self.image_url)
        ans_object.save()
