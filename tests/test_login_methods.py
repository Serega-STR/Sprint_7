import pytest
import requests
import allure
import logging
import string

from url import URL
from api_methods.create_courier import CreateCourierMethods as Create
from api_methods.delete_courier import DeleteCourierMethods as Delete
from api_methods.login_courier import LoginCourierMethods as Login
from data import Data

class TestLoginCourierMethods:
    @allure.title('Проверка успешного логина курьера')
    @allure.description("""курьер может успешно авторизоваться""")
    def test_login_courier_success(self, create_courier_scope_function):
        _, payload = create_courier_scope_function
        response = Login.requests_get_id(payload)
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
    def test_get_id_with_empty_field_check_error_message(self, payload, create_valid_courier):
        response = Login.requests_get_id(payload)
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
    @allure.description("""Если авторизоваться под несуществующим пользователем,
                         запрос возвращает ошибку""")
    def test_get_id_of_unexistent_courier_check_error_message(self):
        # создаем и удаляем курьера
        _, payload = Create.register_new_courier()
        id = Login.get_id(payload)
        Delete.delete_courier_by_id(id)

        # делаем запрос с заведомо несуществующим курьером
        response = Login.requests_get_id(payload)
        
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
    @allure.description("""Система вернёт ошибку, если неправильно 
                        указать логин или пароль при авторизации""")
    def test_get_id_with_wrong_credentials_check_error_message(self, payload, create_valid_courier):
        response = Login.requests_get_id(payload)
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

