import pytest
import requests
import allure
import logging

from data import Data
from url import URL
from helper import Helper

# Инициализируем логгер из Helper
logger = Helper.logger

class OrderMethods:
    @staticmethod
    @allure.step("""
        Создаем заказ 
        """)
    def create_order(color):
        
        payload = Data.order_payload
        payload.update({"color": color})
        response = requests.post(URL.ORDER_ENDPOINT, json=payload)
        if response.status_code == 201:
            logger.info('Успешное создание заказа')
        else:
            logger.warning(f'Не удалось создать заказ. status_code == {response.status_code}')
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
            logger.warning(f'Не удалось получить список заказов. status_code == {response.status_code}')
        return response