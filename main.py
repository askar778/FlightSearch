import data_manager
import flight_search

data = data_manager.DataManager()

flight = flight_search.FlightSearch(data)
for n in range(1,8):
    fligh1_date = flight.search(n)

