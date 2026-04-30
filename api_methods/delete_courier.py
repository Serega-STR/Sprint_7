import requests
import allure
import logging
import string
import random

from url import URL
from helper import Helper
from data import Data

class DeleteCourierMethods:
    @staticmethod
    @allure.step("Удаление курьера по id")    
    def delete_courier_by_id(id):
        Helper.logger.info(f'удаляем курьера!')
        payload = { 'id' : str(id)}
        response = requests.delete(URL.DELETE_COURIER_ENDPOINT+str(id), data=payload)
        if response.status_code == 200:
            Helper.logger.info(f'курьер с {id} успешно удален!')
        else:
            Helper.logger.warning('Ошибка! курьер не был удален!')
            Helper.logger.warning(f'статус-код {response.status_code}')
            Helper.logger.warning(f'сообщение {response.json()}')
        return response