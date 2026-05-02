import pytest
import requests
import allure
import logging
import string

from url import URL
from api_methods.order import OrderMethods
from data import Data


class TestOrderMethods:
    @pytest.mark.parametrize('color', Data.color)
    @allure.title('Успешное создания заказа')
    @allure.description("""Проверка успешного создания заказа
                         с разными параметрами цвета""")
    def test_create_order_success(self, color):
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
    @allure.description("Проверка, что в тело ответа возвращается список заказов")
    def test_get_list_of_orders_success(self):
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

 