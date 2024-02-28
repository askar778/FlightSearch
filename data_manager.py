import requests


class DataManager:

    def __init__(self):
        url = "https://api.sheety.co"
        endpoint = "/75ac28121b6f0e02caba5096fed50b75/flightDeals2702/prices"
        self.response = requests.get(url=f"{url}{endpoint}")
        self.data = self.response.json()

    def IATA_code(self, n):
        IATACode = self.data["prices"][n]["iataCode"]
        return IATACode

    def lowest_price(self,n):
        lowest_price = self.data["prices"][n]["lowestPrice"]
        return lowest_price










