import requests
import random
import string
import logging

class Helper:
    # метод регистрации нового курьера возвращает список из логина и пароля
    # если регистрация не удалась, возвращает пустой список
    def register_new_courier_and_return_login_password():
        # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        # создаём список, чтобы метод мог его вернуть
        login_pass = []

        # генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        # возвращаем список
        return login_pass

    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

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
