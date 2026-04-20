import requests
import allure
import logging

from url import URL
from helper import Helper


class AuthMethods:

    @staticmethod
    def get_token():
        with allure.step("Получение токена авторизации"):
            response = requests.post(URL.AUTH_ENDPOINT, json=AUTH_BODY)
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            return response.json()['token']


class CreateCourierMethods:
    """ @staticmethod # будто бы этот метод излишний
    def create_courier_return_data_courier():
        login_pass_arr = []
                
        #создаем курьера
        login_pass_arr = register_new_courier_and_return_login_password()
        login = login_pass_arr[0]
        password = login_pass_arr[1]
        firstName = login_pass_arr[2]
        return login, password, firstName """

    @staticmethod
    def create_courier():
        return Helper.register_new_courier_and_return_login_password()

    @staticmethod
    def create_duplicate_courier():
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
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        return response

    @staticmethod
    def create_courier_without_login_error_message():
        # генерируем пароль и имя курьера
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "password": password,
            "firstName": first_name
        }
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        return response

    @staticmethod
    def create_courier_without_password_error_message():
        # генерируем логин,   и имя курьера
        login = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "firstName": first_name
        }
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        
        return response

    @staticmethod
    def create_courier_without_first_name_error_message():
        # генерируем логин, пароль 
        login = generate_random_string(10)
        password = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password
        }
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        
        return response

    
    @staticmethod
    def create_courier_with_already_used_login_error_message():
        # генерируем логин, пароль и имя курьера
        login = "ninja"
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password
        }
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        
        return response

class LoginCourierMethods:
    @staticmethod
    def courier_can_login():
        logger.info(f'курьер может авторизоваться')
        
        login_pass_arr = []
        login_pass_arr = CreateCourierMethods.create_courier()
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

        yield response

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

class DeleteCourierMethods:
    @staticmethod
    def create_delete_courier():
        logger.info(f'создаем курьера')
        login_pass_arr = []
        login_pass_arr = CreateCourierMethods.create_courier()
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

        yield response

        # Проверяем статус-код
        if response.status_code == 200:
            # Парсим JSON и достаём id
            data = response.json()
            id = str(data['id'])
            logger.info(f"ID курьера: {id}")  # Вывод: ID курьера: 12345
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
        else:
            logger.info(f"Ошибка получения логина: статус-код {response.status_code}. Курьер не удален")

        
        
    @staticmethod
    def delete_courier_by_id(id):
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


# DeleteCourierMethods.create_delete_courier()
# DeleteCourierMethods.delete_courier_by_id(735327)