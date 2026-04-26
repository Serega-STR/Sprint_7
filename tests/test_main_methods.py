import pytest
import requests
import allure
import logging
import string

from helper import Helper
from url import URL
from api_methods.main_methods import CreateCourierMethods, DeleteCourierMethods, LoginCourierMethods, OrderMethods
from data import Data

# Инициализируем логгер из Helper
logger = Helper.logger


class TestСreateCourierMethods:

    @allure.title('Создание курьера')
    @allure.description("""Проверка успешного создания курьера""")
    def test_create_courier_success(self):
        response = CreateCourierMethods.create_courier_check_create_delete_courier()
        assert response.status_code == 201, f'Ошибка! Ожидаемый код статуса 201, фактический {response.status_code}'
        
        message = response.json()
        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert len(message) == 1, f"Ошибка! Ожидаемая длина словаря == 1. Фактическая: {len(message)}"
        for key, value in message.items():
            assert "ok" in key, f'Ошибка! Ожидаемый ключ словаря "ok", фактический : {key}'
            assert value==True, f'Ошибка! Ожидаемое значения словаря  True, фактический : {value}'


    
    @allure.title('Создание дубликата курьера')
    @allure.description("""Нельзя создать двух одинаковых курьеров.
                        Если создать пользователя с логином, который уже есть, 
                        возвращается ошибка""")
    def test_create_courier_duplicate_check_error_message(self):
        response = CreateCourierMethods.create_courier_check_create_duplicate_delete_courier()  # получаем генератор
        assert response.status_code == 409, f'Ошибка! Ожидаемый код статуса 409, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "message"
        expected_value = "Этот логин уже используется. Попробуйте другой."

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert expected_key in message and message[expected_key] == expected_value, (
                    f'Ошибка! Ожидаемое сообщение ответа должно содержать:' + 
                    f'{{\'{expected_key}\' : \'{expected_value}\'}} , фактическое содержит : {message}'
                    )

    @pytest.mark.parametrize('payload', Data.payload_with_empty_field)
    @allure.title('Нельзя создать курьера с пустым полем')
    @allure.description("""Нельзя создать курьера, если одного из полей нет. 
                        Запрос возвращает ошибку""")
    def test_create_courier_with_empty_field_error_message(self, payload):
        response = CreateCourierMethods.create_courier_with_empty_field_error_message(payload)
        expected_status_code = 400
        assert response.status_code == expected_status_code, f'Ошибка! Ожидаемый код статуса {expected_status_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "message"
        expected_value = "Недостаточно данных для создания учетной записи"

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert expected_key in message and message[expected_key] == expected_value, (
                    f'Ошибка! Ожидаемое сообщение ответа должно содержать:' + 
                    f'{{\'{expected_key}\' : \'{expected_value}\'}} , фактическое содержит : {message}'
                    )

class TestLoginCourierMethods:
    @allure.title('Проверка успешного логина курьера')
    @allure.description("""курьер может авторизоваться""")
    def test_login_courier_success(self):
        response = LoginCourierMethods.create_courier_check_login_delete_courier()
        assert response.status_code == 200, f'Ошибка! Ожидаемый код статуса 200, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "id"

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert len(message) == 1, f"Ошибка! Ожидаемая длина словаря == 1. Фактическая: {len(message)}"
        for key, value in message.items():
            assert expected_key in key, f'Ошибка! Ожидаемый ключ ответа {expected_key}, фактический : {key}'
            assert isinstance(value, int), f'Ошибка! Ожидаемый тип значения ответа  — целое число, фактический : {value}'
            assert value > 0, f'Ошибка! Значение ответа должно быть положительным числом, фактическое : {value}'

    @pytest.mark.parametrize('payload', Data.payload_with_empty_login_field)
    @allure.title('Проверка ошибки логина курьера с пустым полем')
    @allure.description("""Для авторизации нужно передать все обязательные поля.
                        Если какого-то поля нет, запрос возвращает ошибку""")
    def test_get_id_empty_field_error_message(self, payload):
        response = LoginCourierMethods.get_id_by_payload(payload)
        expected_status_code = 400
        assert response.status_code == expected_status_code, f'Ошибка! Ожидаемый код статуса {expected_status_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "message"
        expected_value = "Недостаточно данных для входа"

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert expected_key in message and message[expected_key] == expected_value, (
                    f'Ошибка! Ожидаемое сообщение ответа должно содержать:' + 
                    f'{{\'{expected_key}\' : \'{expected_value}\'}} , фактическое содержит : {message}'
                    )

    @allure.title('Проверка ошибки логина несуществующего курьера')
    @allure.description("""Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку""")
    def test_get_id_unexistent_courier(self):
        response = LoginCourierMethods.get_id_unexistent_courier()
        expected_status_code = 404
        assert response.status_code == expected_status_code, f'Ошибка! Ожидаемый код статуса {expected_status_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "message"
        expected_value = "Учетная запись не найдена"

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert expected_key in message and message[expected_key] == expected_value, (
                    f'Ошибка! Ожидаемое сообщение ответа должно содержать:' + 
                    f'{{\'{expected_key}\' : \'{expected_value}\'}} , фактическое содержит : {message}'
                    )

    @pytest.mark.parametrize('payload', Data.payload_wrong_credentials)
    @allure.title('Проверка ошибки логина курьера с неверными кредами')
    @allure.description("""Система вернёт ошибку, если неправильно указать логин или пароль при авторизации""")
    def test_get_id_wrong_credentials_error_message(self, payload, check_courier):
        
        # проверка создания или наличия пользователя
        response = check_courier
        assert response.status_code == 404 or 409, f'Ошибка! Ожидаемый код статуса 404 или 409, фактический {response.status_code}'
        
        response = LoginCourierMethods.get_id_by_payload(payload)
        expected_status_code = 404
        assert response.status_code == expected_status_code, f'Ошибка! Ожидаемый код статуса {expected_status_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "message"
        expected_value = "Учетная запись не найдена"

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert expected_key in message and message[expected_key] == expected_value, (
                    f'Ошибка! Ожидаемое сообщение ответа должно содержать:' + 
                    f'{{\'{expected_key}\' : \'{expected_value}\'}} , фактическое содержит : {message}'
                    )

class TestOrderMethods:
    @pytest.mark.parametrize('color', Data.color)
    @allure.title('Успешное создания заказа')
    @allure.description("""Проверка успешного создания заказа
                         с разными параметрами цвета""")
    def test_create_order(self, color):
        response = OrderMethods.create_order(color)
        expected_status_code = 201
        assert response.status_code == expected_status_code, f'Ошибка! Ожидаемый код статуса {expected_status_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "track"
        expected_value = message[expected_key]

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert expected_key in message, (
                    f'Ошибка! Ожидаемое сообщение ответа должно содержать: {expected_key}, фактическое содержит : {message.keys()}'
                    )
        assert isinstance(expected_value, int), f"Ошибка! Ответ не является целым числом, тип: {type(expected_value).__name__}"

    @allure.title('Успешное получение списка заказов')
    @allure.description("""Проверка, что в тело ответа возвращается список заказов""")
    def test_get_list_of_orders(self):
        response = OrderMethods.get_list_of_orders()
        expected_status_code = 200
        assert response.status_code == expected_status_code, f'Ошибка! Ожидаемый код статуса {expected_status_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "orders"
        expected_value = message[expected_key]

        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert expected_key in message, (
                    f'Ошибка! Ожидаемое сообщение ответа должно содержать: {expected_key}, фактическое содержит : {message.keys()}'
                    )
        assert isinstance(expected_value, list), f"Ошибка! Ответ не является списком, тип: {type(expected_value).__name__}"

class TestDeleteCourierMethods:
    @allure.title('Успешное удаление курьера')
    @allure.description("""Проверка успешного удаления курьера""")
    def test_delete_courier_success(self):
        login, password, _ = CreateCourierMethods.create_courier()
        payload = {
            "login": login,
            "password": password
        }

        id = LoginCourierMethods.get_id(payload)
        response = DeleteCourierMethods.delete_courier_return_response(id)
        expected_code = 200
        assert response.status_code == expected_code, f'Ошибка! Ожидаемый код статуса {expected_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "ok"
        expected_value = True

        assert len(message) == 1, f"Ошибка! Ожидаемая длина ответа == 1. Фактическая: {len(message)}"
        for key, value in message.items():
            assert key == expected_key  , f'Ошибка! Ожидаемый ключ ответа {expected_key}, фактический : {key}'
            assert value == expected_value , f'Ошибка! Ожидаемое значение ответа {expected_value}, фактическое : {value}'

