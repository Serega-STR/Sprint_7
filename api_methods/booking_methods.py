import requests
import allure

from url import URL

class BookingMethods:

    @staticmethod
    @allure.step("Создание бронирования")
    def create_booking(booking_data: dict):
        return requests.post(URL.BOOKING_ENDPOINT, json=booking_data)


    @staticmethod
    @allure.step("Удаление бронирования")
    def delete_booking(booking_id, token):
        headers = {"Cookie": f"token={token}"}
        return requests.delete(URL.BOOKING_ENDPOINT + f"/{booking_id}", headers=headers)
    
    @staticmethod
    @allure.step("Получение бронирования по ID")
    def get_booking_by_id(booking_id):
        return requests.get(URL.BOOKING_ENDPOINT + f"/{booking_id}")

    @staticmethod
    @allure.step("Получение ID бронирования по имени и фамилии")
    def get_booking_by_firstname_surname(firstname, surname):
        params = {"firstname": firstname, "lastname": surname}
        response = requests.get(URL.BOOKING_ENDPOINT, params=params)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        bookings = response.json()
        if bookings:
            return bookings[0]['bookingid']
        else:
            raise Exception(f"No booking found for {firstname} {surname}")
