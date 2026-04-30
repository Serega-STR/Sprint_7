import requests
import random
import string
import logging
from url import *


class Main:
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    def generate_credentials():
        login = Main.generate_random_string(10)
        password = Main.generate_random_string(10)
        first_name = Main.generate_random_string(10)
        return login, password, first_name













            
# class CourierManager:
#     @staticmethod
#     def create_courier(payload):
#         """Создаёт курьера и возвращает его ID."""
#         url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
#         response = requests.post(url, data=payload)

#         if response.status_code == 201:
#             courier_id = response.json().get('id')
#             Helper.logger.info(f"Курьер создан, ID: {courier_id}")
#             return courier_id
#         else:
#             Helper.logger.error(f"Не удалось создать курьера. Статус: {response.status_code}, ответ: {response.text}")
#             raise Exception(f"Ошибка создания курьера: {response.status_code}")

#     @staticmethod
#     def delete_courier(courier_id):
#         """Удаляет курьера по ID."""
#         url = f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}'
#         response = requests.delete(url)

#         if response.status_code == 202:
#             Helper.logger.info(f"Курьер с ID {courier_id} успешно удалён")
#             return True
#         else:
#             Helper.logger.warning(f"Не удалось удалить курьера с ID {courier_id}. Статус: {response.status_code}")
#             return False