import requests
import allure
import logging

from url import URL
from helper import Helper
from data import Data
from api_methods.generator import Main
from api_methods.delete_courier import DeleteCourierMethods as Delete
from api_methods.login_courier import LoginCourierMethods as Login

# Инициализируем логгер из Helper
logger = Helper.logger


class CreateCourierMethods:
    # метод регистрации нового курьера возвращает кортеж из ответа запроса (response), логина, пароля, имени
    # если регистрация не удалась, возвращает ответ запроса (response)
    def register_new_courier(payload=None):
        if payload is None:
            # генерируем логин, пароль и имя курьера
            login, password, first_name = Main.generate_credentials()

            # собираем тело запроса
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        else:
            # извлекаем значения из переданного payload
            login = payload.get("login")
            password = payload.get("password")
            first_name = payload.get("firstName")
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(URL.CREATE_COURIER_ENDPOINT, data=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            Helper.logger.info(f'курьер создан!\n' + 
                f'login: {login}\n' +
                f'password: {password}\n' +
                f'firstName: {first_name}\n')
            return response, payload
        else:
            Helper.logger.warning(f'Ошибка! Не удалось создать курьера: response.status_code == {response.status_code} ')
            return response, payload

    @staticmethod
    @allure.step("""
        Создаем курьера, response передаем в тест.
                """)
    def check_create_courier(payload=None):
        if payload is None:
            response, _ = CreateCourierMethods.register_new_courier(payload)
            return response
        else:
            response = CreateCourierMethods.register_new_courier(payload)
            return response


    @staticmethod
    @allure.step("""
        Создаем курьера, дублируем запрос на создание.
        response передаем в тест. 
        Получаем id. Удаляем курьера
        """)
    def create_courier_duplicate():
        # создаем курьера первично
        _, payload = CreateCourierMethods.register_new_courier()
        # отправляем повторный запрос на регистрацию курьера, ответ возвращаем в return
        response = CreateCourierMethods.register_new_courier(payload)
        # чистим за собой
        id = Login.get_id(payload)
        Delete.delete_courier_by_id(id)
        return response

    

