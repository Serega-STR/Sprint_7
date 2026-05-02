import pytest
import requests
import allure
import logging
import string

from url import URL
from api_methods.create_courier import CreateCourierMethods as Create
from data import Data

class TestСreateCourierMethods:

    @allure.title('Создание курьера')
    @allure.description("Проверка успешного создания курьера")
    def test_create_courier_success(self, create_courier_scope_function):
        response, _ = create_courier_scope_function
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

        response, _ = Create.create_courier_duplicate()
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
    def test_create_courier_with_empty_field_check_error_message(self, payload):
        response, _ = Create.check_create_courier(payload)
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
