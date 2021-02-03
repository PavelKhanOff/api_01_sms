import logging
import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

BASE_URL = 'https://api.vk.com/method/users.get'
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
API_V = '5.89'


def get_timeout():
    time.sleep(5)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': API_V,
        'access_token': ACCESS_TOKEN,
        'fields': 'online'
    }
    try:
        status = requests.post(BASE_URL, params=params).json()['response']
        return status[0]['online']
    except Exception:
        logging.exception(msg='Ошибка в работе отправки сообщения!')


def sms_sender(sms_text):
    message = (CLIENT.messages.create(
        body=sms_text, from_=NUMBER_FROM, to=NUMBER_TO))
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        get_timeout()
