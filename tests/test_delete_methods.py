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

class TestDeleteCourierMethods:
    @allure.title('Успешное удаление курьера')
    @allure.description("Проверка успешного удаления курьера")
    def test_delete_courier_success(self):
        _, payload = Create.register_new_courier()
        id = Login.get_id(payload)
        response = Delete.delete_courier_by_id(id)
        expected_code = 200
        assert response.status_code == expected_code, f'Ошибка! Ожидаемый код статуса {expected_code}, фактический {response.status_code}'
        
        message = response.json()
        expected_key = "ok"
        expected_value = True

        assert len(message) == 1, f"Ошибка! Ожидаемая длина ответа == 1. Фактическая: {len(message)}"
        for key, value in message.items():
            assert key == expected_key  , f'Ошибка! Ожидаемый ключ ответа {expected_key}, фактический : {key}'
            assert value == expected_value , f'Ошибка! Ожидаемое значение ответа {expected_value}, фактическое : {value}'

