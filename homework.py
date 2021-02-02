import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

BASE_URL = 'https://api.vk.com/method/users.get'
ACCESS_TOKEN = ('17b418a96d75e01754e8084f0c5fdca73ea3715dce413'
                '5fb4aadb37cb146a865fcf3f964aab3416712305')
API_V = '5.89'


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': API_V,
        'access_token': ACCESS_TOKEN,
        'fields': 'online'
    }
    status = requests.post(BASE_URL, params=params).json()['response']
    return status[0]['online']


def send_sms(sms_text):
    message = (CLIENT.messages.create(
        body=sms_text, from_=NUMBER_FROM, to=NUMBER_TO))
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
