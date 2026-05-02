import requests
import allure
import logging
import string
import random

from url import URL
from helper import Helper
from data import Data

# Инициализируем логгер из Helper
logger = Helper.logger

class LoginCourierMethods:
    @staticmethod
    @allure.step("Получаем логин по переданным кредам")
    def get_id(payload):
        if len(payload) == 3:
            payload = LoginCourierMethods.make_payload_for_id(payload)
        response = LoginCourierMethods.requests_get_id(payload)

        if response.status_code == 200:
            # Парсим JSON и достаём id
            data = response.json()
            id = str(data['id'])
            Helper.logger.info(f"Полученный ID курьера: {id}")
            return id

        else:
            error_message = (
            f"Ошибка получения ID курьера. "
            f"Статус: {response.status_code}, "
            f"Ответ: {response.text}"
        )
            Helper.logger.error(error_message)
            raise Exception(error_message)

    def make_payload_for_id(payload):
        new_payload = {
            "login": payload["login"],
            "password": payload["password"]
                    }
        return new_payload

    def requests_get_id(payload):
        Helper.logger.info(f'получаем ID !\n')
        response = requests.post(URL.LOGIN_COURIER_ENDPOINT, json=payload)
        return response

