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


class CreateCourierMethods:
    
    @staticmethod
    @allure.step('создание курьера')
    def create_courier():
        return Helper.register_new_courier_and_return_credential()
    

    @staticmethod
    @allure.step("""
        Создаем курьера, здесь response передаем в тест. Проверяем создание. Удаляем курьера
                """)
    def create_courier_check_create_delete_courier():
        logger.info(f'создаем курьера')
        
        # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        # генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        if response.status_code == 201:
            Helper.logger.info(f'курьер создан!\n' + 
                f'login: {login}\n' +
                f'password: {password}\n' +
                f'firstName: {first_name}\n')
            
            payload_for_id = {
                "login": login,
                "password": password
            }
            id = LoginCourierMethods.get_id(payload_for_id)
            DeleteCourierMethods.delete_courier_by_id(id)
        else:
            Helper.logger.info(f'Не удалось создать курьера: response.status_code == {response.status_code} ')
        return response

    
    @staticmethod
    @allure.step("""
        Создаем курьера, дублируем запрос на создание.
        response передаем в тест. 
        Получаем id. Удаляем курьера
        """)
    def create_courier_check_create_duplicate_delete_courier():
        
        logger.info(f'создаем курьера')
        login_pass_arr = []
        login_pass_arr = CreateCourierMethods.create_courier()
        login = login_pass_arr[0]
        password = login_pass_arr[1]
        firstName = login_pass_arr[2]

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": firstName
        }
        
        # отправляем первый запрос на регистрацию курьера
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        
        if response.status_code == 201:
            Helper.logger.info(f'курьер создан!\n' + 
            f'login: {login}\n' +
            f'password: {password}\n' +
            f'firstName: {first_name}\n')
            payload_for_id = {
            "login": login,
            "password": password
            }
            # отправляем второй запрос на регистрацию этого же курьера
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
            
            # получаем id, удаляем курьера
            id = LoginCourierMethods.get_id(payload_for_id)
            DeleteCourierMethods.delete_courier_by_id(id)
            return response
        else:
            Helper.logger.info(f'Не удалось создать курьера: response.status_code == {response.status_code} ')
        return response


    @staticmethod
    @allure.step("""
        Попытка создать курьера с пустыми,
        или None полями, или без поля логин\пароль
        (значения передаются параметризацией)
        """)
    def create_courier_with_empty_field_error_message(payload):
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        return response


class LoginCourierMethods:
    @staticmethod
    @allure.step("""
        Получаем логин по переданным кредам
        """)   
    def get_id(payload):
        
        logger.info(f'получаем ID !\n')
        response = requests.post(URL.LOGIN_COURIER_ENDPOINT, json=payload)

        # Парсим JSON и достаём id
        data = response.json()
        id = str(data['id'])
        logger.info(f"Полученный ID курьера: {id}")  # Вывод: ID курьера: 12345
        
        return id


    @staticmethod
    @allure.step("""
        Создаем курьера. Получаем id. 
        response передаем в тест. Удаляем курьера
        """)
    def create_courier_check_login_delete_courier():
        
        logger.info(f'создаем курьера')
        login, password, _ = CreateCourierMethods.create_courier()

        payload = {"login": login, "password": password}

        # получаем логин
        logger.info(f'получаем ID !\n')
        response = requests.post(URL.LOGIN_COURIER_ENDPOINT, json=payload)

        # Парсим JSON и достаём id
        data = response.json()
        id = str(data['id'])
        logger.info(f"Полученный ID курьера: {id}")  # Вывод: ID курьера: 12345

        # Проверяем статус-код
        if response.status_code == 200:
            #удаляем курьера
            DeleteCourierMethods.delete_courier_by_id(id)
        else:
            logger.info(f"Ошибка получения логина: статус-код {response.status_code}. Курьер не удален")

        return response


    @staticmethod
    @allure.step("""
        Пытаемся получить логин по переданным кредам
        """)
    def get_id_by_payload(payload):
        
        logger.info(f'Пытаемся получить ID !')
        response = requests.post(URL.LOGIN_COURIER_ENDPOINT, json=payload)

        return response


    @staticmethod
    @allure.step("""
        Создаем курьера. Получаем креды. Удаляем курьера.
        Пытаемся по кредам несуществующего пользователя получить id
        response передаем в тест. 
        """)
    def get_id_unexistent_courier():
        
        logger.info(f'создаем курьера')
        login, password, _ = CreateCourierMethods.create_courier()

        payload = {"login": login, "password": password}

        # получаем логин
        logger.info(f'получаем ID !\n')
        response = requests.post(URL.LOGIN_COURIER_ENDPOINT, json=payload)

        # Парсим JSON и достаём id
        data = response.json()
        id = str(data['id'])

        # Проверяем статус-код
        if response.status_code == 200:
            #удаляем курьера
            DeleteCourierMethods.delete_courier_by_id(id)
        else:
            logger.info(f"Ошибка получения логина: статус-код {response.status_code}. Курьер не удален")

        # получаем логин несуществующего пользователя
        logger.info(f'получаем ID несуществующего пользователя !\n')
        response = requests.post(URL.LOGIN_COURIER_ENDPOINT, json=payload)
        return response


class OrderMethods:
    @staticmethod
    @allure.step("""
        Создаем заказ 
        """)
    def create_order(color):
        payload = {
            "firstName": "ivan",
            "lastName": "ivanov",
            "address": "Piter, Lenina д.1 кв. 5",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-05-06",
            "comment": "comment",
            "color": color
                }

        response = requests.post(URL.ORDER_ENDPOINT, json=payload)
        if response.status_code == 201:
            logger.info('Успешное создание заказа')
        else:
            logger.info(f'Не удалось создать заказ. status_code == {response.status_code}')
        return response


    @staticmethod
    @allure.step("""
        Получаем список заказов 
        """)
    def get_list_of_orders(payload=None):
        response = requests.get(URL.ORDER_ENDPOINT, json=payload)
        if response.status_code == 200:
            logger.info('Получен список заказов')
        else:
            logger.info(f'Не удалось получить список заказов. status_code == {response.status_code}')
        return response


class DeleteCourierMethods:
    @staticmethod
    @allure.step("""
        Удаление курьера по id
        """)
    def delete_courier_by_id(id):
        
        logger.info(f'удаляем курьера!')
        payload = { 'id' : str(id)}
        response = requests.delete(URL.DELETE_COURIER_ENDPOINT+str(id), data=payload)
        if response.status_code == 200:
            logger.info('курьер успешно удален!')
        else:
            logger.info('Ошибка! курьер не был удален!')
            logger.info(f'статус-код {response.status_code}')
            logger.info(f'сообщение {response.json()}')


    @staticmethod
    @allure.step("""
        Удаление курьера по id с возвратом response
        """)
    def delete_courier_return_response(id):
        
        logger.info(f'удаляем курьера!')
        payload = { 'id' : str(id)}
        response = requests.delete(URL.DELETE_COURIER_ENDPOINT+str(id), data=payload)
        if response.status_code == 200:
            logger.info('курьер успешно удален!')
        else:
            logger.info('Ошибка! курьер не был удален!')
            logger.info(f'статус-код {response.status_code}')
            logger.info(f'сообщение {response.json()}')

        return response
            
