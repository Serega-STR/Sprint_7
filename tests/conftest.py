import logging
import pytest
import requests

from data import Data
from url import *
from helper import Helper
from api_methods.create_courier import CreateCourierMethods as Create
from api_methods.login_courier import LoginCourierMethods as Login
from api_methods.delete_courier import DeleteCourierMethods as Delete

# Инициализируем логгер из Helper
logger = Helper.logger


@pytest.fixture(scope='function')
def create_courier_scope_function(payload=None):
    response, payload = Create.register_new_courier(payload)
    yield response, payload
    id = Login.get_id(payload)
    Delete.delete_courier_by_id(id)

@pytest.fixture(scope='class')
def create_courier_scope_class(payload=None):
    response, payload = Create.register_new_courier(payload)
    yield response, payload
    id = Login.get_id(payload)
    Delete.delete_courier_by_id(id)

@pytest.fixture(scope='class')
def create_valid_courier(payload=Data.payload_valid):
    response, payload = Create.register_new_courier(payload)
    yield response, payload
    id = Login.get_id(payload)
    Delete.delete_courier_by_id(id)    