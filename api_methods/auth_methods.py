import requests
import allure

from data import AUTH_BODY
from url import URL

class AuthMethods:

    @staticmethod
    def get_token():
        with allure.step("Получение токена авторизации"):
            response = requests.post(URL.AUTH_ENDPOINT, json=AUTH_BODY)
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            return response.json()['token']
