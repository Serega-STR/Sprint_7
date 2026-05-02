import logging
import pytest
import requests

from data import Data
from url import *
from api_methods.create_courier import CreateCourierMethods as Create
from api_methods.login_courier import LoginCourierMethods as Login
from api_methods.delete_courier import DeleteCourierMethods as Delete
    
# Создаём функцию‑фабрику, которая возвращает фикстуру с нужными параметрами:
def _make_courier_fixture(scope, payload=None):
    @pytest.fixture(scope=scope)
    def _courier_fixture(received_payload=payload):
        response, used_payload = Create.register_new_courier(received_payload)

        yield response, used_payload

        # Очистка после теста
        courier_id = Login.get_id(used_payload)
        Delete.delete_courier_by_id(courier_id)
    return _courier_fixture

# Создаём конкретные фикстуры на основе фабрики
create_courier_scope_function = _make_courier_fixture('function')
create_courier_scope_class = _make_courier_fixture('class')
create_valid_courier = _make_courier_fixture('class', Data.payload_valid)