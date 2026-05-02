import requests
import random
import string
import logging
from url import *

class Helper:
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

        # раскомментируйте нужный обработчик и нужное добавление обработчика к логгеру
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

