import requests
import random
import string
import logging
from url import *


class Main:
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    def generate_credentials():
        login = Main.generate_random_string(10)
        password = Main.generate_random_string(10)
        first_name = Main.generate_random_string(10)
        return login, password, first_name

