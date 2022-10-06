from fastapi import FastAPI
import os
import json
import pprint
import time
from starlette.config import Config

import requests


class Settings:
    def __init__(self):
        config = Config(".env")
        self.line_notify_url = config('LINE_NOTIFY_URL')
        self.weather_api_url = config('WEATHER_API_URL')
        self.headers = {
            # 各自発行したトークンを記述
            'Authorization': 'Bearer ' + config('LINE_NOTIFY_AC_TOKEN')
        }

settings = Settings()
app = FastAPI()

class Message:
    def send_message(self, list):
        text= "\n" + "日付:" + list['forecasts'][0]['date'] + "\n" + "地域:" + list['title'] + "\n" + "天気:" + list['forecasts'][0]['detail']['weather'] + "\n" + "風速:" + list['forecasts'][0]['detail']['wind'] + list['forecasts'][0]['detail']['wave']
        files = {
            'message': (None, text)
        }
        files=files
        requests.post(settings.line_notify_url, headers=settings.headers, files=files)
        return

    def get_forecast(self):
        return requests.get(settings.weather_api_url).json()



msg = Message()


# 無限ループ(1日1回通知)
while True:
    # lineへ通知
    msg.send_message(msg.get_forecast())
    time.sleep(3600*24)