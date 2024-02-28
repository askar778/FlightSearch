import os
import requests
import notification_manager
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_data import FlightData


class FlightSearch:

    def __init__(self, data: DataManager):

        self.apikey_tequila = os.environ["apikey_tequila"]
        self.url = "https://api.tequila.kiwi.com/v2"
        self.endpoint = "/search"
        self.apiKey = {"accept": "application/json",
                       "apikey": self.apikey_tequila}

        self.response = None
        # self.parameters = None
        self.data = data
        self.datetime = datetime
        self.timedelta = timedelta

    def search(self, n):
        today = self.datetime.now()
        date_from = today + self.timedelta(days=1)
        date_to = today + self.timedelta(days=30 * 6)
        parameters = {"fly_from": "LHR",
                      "fly_to": self.data.IATA_code(n=n),
                      "date_from": date_from.strftime("%d/%m/%Y"),
                      "date_to": date_to.strftime("%d/%m/%Y"),
                      "nights_in_dst_from": 7,
                      "nights_in_dst_to": 28,
                      "one_for_city": 1,
                      "max_stopovers": 0,
                      "curr": "GBP"
                      }
        self.response = requests.get(url=f"{self.url}{self.endpoint}", headers=self.apiKey, params=parameters)
        try:
            data = self.response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {self.data.IATA_code(n=n)}.")
            return None

        price = data["fare"]["adults"]
        print(price)
        origin_city = data["cityFrom"]
        origin_city_code = data["cityCodeFrom"]
        destination_city = data["cityTo"]
        destination_city_code = data["cityCodeTo"]

        arrivalstring = data["local_arrival"]
        departurestring = data["local_departure"]

        if self.price_verification(n=n, price=price):
            flightdata = FlightData(price=price, origin_city=origin_city,
                                    origin_city_code=origin_city_code, destination_city=destination_city,
                                    destination_city_code=destination_city_code,
                                    arrival=arrivalstring[:10],
                                    departure=departurestring[:10])
            body = (
                f"Low Price ALert! Only ${flightdata.price} to fly from {flightdata.origin_city}-{flightdata.origin_city_code} to "
                f"{flightdata.destination_city}-"f"{flightdata.destination_city_code},"
                f" from {flightdata.arrival} to {flightdata.departure}")

            from_number = os.environ["From_phoneNumber"]
            to = os.environ["to_PhoneNUmber"]

            message = notification_manager.NotificationManager(body=body, from_number=from_number, to=to)

    def price_verification(self, n, price):
        lowest_price = self.data.lowest_price(n)
        actual_price = price

        if actual_price <= lowest_price:
            return True
