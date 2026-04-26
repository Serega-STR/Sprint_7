import logging
import pytest
import requests

from data import Data

def setup_logger():
    # НАСТРОЙКА ЛОГИРОВАНИЯ
    # Создаём логгер для текущего модуля
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # минимальный уровень логирования

    # Очищаем существующие обработчики (чтобы избежать дублирования)
    if logger.handlers:
        logger.handlers.clear()

    # ФОРМАТИРОВЩИК (общий для всех обработчиков)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Создаём обработчик для записи в файл
    file_handler = logging.FileHandler('test_logs.log', mode='w', encoding='utf-8')  # 'w' — перезаписывать, 'a' — дописывать
    file_handler.setLevel(logging.INFO)  # уровень для этого обработчика
    file_handler.setFormatter(formatter)

    # Создаём обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # в консоль пишем DEBUG и выше
    console_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()

@pytest.fixture(scope='class')
def check_courier():
    login = Data.login
    password = Data.password
    first_name = Data.first_name
    payload = Data.payload_valid
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    if response.status_code == 201:
        logger.info(f'курьер создан!\n' + 
            f'login: {login}\n' +
            f'password: {password}\n' +
            f'firstName: {first_name}\n')
        
        payload_for_id = {
            "login": login,
            "password": password
        }
        id = LoginCourierMethods.get_id(payload_for_id)
        DeleteCourierMethods.delete_courier_by_id(id)
    elif response.status_code == 409 :
        logger.info(f'курьер уже существует!\n' + 
            f'login: {login}\n' +
            f'password: {password}\n' +
            f'firstName: {first_name}\n')
    else:
        logger.info(f'Не удалось создать курьера: response.status_code == {response.status_code} ')
    return response

    