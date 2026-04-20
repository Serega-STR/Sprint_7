import requests
import allure
import logging

from url import URL
from helper import *


class AuthMethods:

    @staticmethod
    def get_token():
        with allure.step("Получение токена авторизации"):
            response = requests.post(URL.AUTH_ENDPOINT, json=AUTH_BODY)
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            return response.json()['token']

    

class CouriersMethods:
    @staticmethod
    def create_courier():
        return register_new_courier_and_return_login_password()

    @staticmethod
    def return_data_courier():
        login_pass_arr = []
                
        #создаем курьера
        login_pass_arr = CouriersMethods.create_courier()
        login = login_pass_arr[0]
        password = login_pass_arr[1]
        firstName = login_pass_arr[2]
        return login, password, firstName

    @staticmethod
    def create_delete_courier():
        logger.info(f'создаем курьера')
        login_pass_arr = []
        login_pass_arr = CouriersMethods.return_data_courier()
        login = login_pass_arr[0]
        password = login_pass_arr[1]
        firstName = login_pass_arr[2]

        logger.info(f'курьер создан!')
        logger.info(f'login: {login}') 
        logger.info(f'password: {password}')
        logger.info(f'firstName: {firstName}')

        payload = {"login": login, "password": password}

        # получаем логин
        response = requests.post(URL.LOGIN_COURIER_ENDPOINT, json=payload)
        # Проверяем статус-код
        if response.status_code == 200:
            # Парсим JSON и достаём id
            data = response.json()
            id = str(data['id'])
            logger.info(f"ID курьера: {id}")  # Вывод: ID курьера: 12345
        else:
            logger.info(f"Ошибка получения логина: статус-код {response.status_code}")

        #удаляем курьера
        logger.info(f'удаляем курьера c Id : {id}')
        payload = { 'id' : id}
        response = requests.delete(URL.DELETE_COURIER_ENDPOINT+id, data=payload)
        if response.status_code == 200:
            logger.info(response.status_code)
            logger.info(response.json())
            logger.info('курьер удален!')
        else:
            logger.info(f"Ошибка: статус-код {response.status_code}")
        
    @staticmethod
    def only_delete_courier(id):
        logger.info(f'удаляем курьера!')
        payload = { 'id' : str(id)}
        response = requests.delete(URL.DELETE_COURIER_ENDPOINT+str(id), data=payload)
        if response.status_code == 200:
            logger.info(response.status_code)
            logger.info(response.json())
            logger.info('курьер удален!')
        else:
            logger.info(f"{response.status_code}")
            logger.info(response.json())
            logger.info(response.text)


# CouriersMethods.create_delete_courier()
CouriersMethods.only_delete_courier(735327)