import pytest
import requests
import allure
import logging
import string

from helper import Helper
from url import URL
from api_methods.main_methods import DeleteCourierMethods

""" class TestCreateCourierMethods:
    @staticmethod
    def test_create_courier():
        # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        # создаём список, чтобы метод мог его вернуть
        login_pass = []

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
        ### в этом месте верх можно сделать методом create_courier_return_response с return response
        ### далее тут тупо вызываем response = create_courier_return_response() и пошли assert'ы
        assert response.status_code == 201, logger.info(f'Ошибка! Ожидаемый код статуса 201, фактический {response.status_code}')
        assert response.json() == {"ok":true}, logger.info(f'Ошибка! Ожидаемое сообщение: {"ok":true}, фактическое: {response.json()}')

    @staticmethod
    def test_create_courier_duplicate_error_message():
        response = create_duplicate_courier()
        assert response.status_code == 409, logger.info(f'Ошибка! Ожидаемый код статуса 409, фактический {response.status_code}')
        message = {"message": "Этот логин уже используется"}
        assert response.json() == message, logger.info(f'Ошибка! Ожидаемое сообщение: {message}, фактическое: {response.json()}') 

    @staticmethod
    def test_create_courier_without_login_error_message():
        response = create_courier_without_login_error_message()
        assert response.status_code == 409, logger.info(f'Ошибка! Ожидаемый код статуса 409, фактический {response.status_code}')
        message = {"message": "Этот логин уже используется"}
        assert response.json() == message, logger.info(f'Ошибка! Ожидаемое сообщение: {message}, фактическое: {response.json()}') """

class TestDeleteCourierMethods:
    
    def test_create_delete_courier_succes(self):
        response = DeleteCourierMethods.create_delete_courier()
        assert response.status_code == 200, logger.info(f'Ошибка! Ожидаемый код статуса 200, фактический {response.status_code}')
        message = {ok: true}
        assert response.json() == message, logger.info(f'Ошибка! Ожидаемое сообщение: {message}, фактическое: {response.json()}')
        
    """ @staticmethod
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
            logger.info(response.text) """


# DeleteCourierMethods.create_delete_courier()
# DeleteCourierMethods.only_delete_courier(735327)
# TestDeleteCourierMethods.test_create_delete_courier_succes()