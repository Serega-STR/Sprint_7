
class URL:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    CREATE_COURIER_ENDPOINT = f"{BASE_URL}/api/v1/courier" #POST для создания курьера
    DELETE_COURIER_ENDPOINT = f"{BASE_URL}/api/v1/courier/" #POST для удаления курьера
    LOGIN_COURIER_ENDPOINT = f"{BASE_URL}/api/v1/courier/login" #post логин курьера в системе
