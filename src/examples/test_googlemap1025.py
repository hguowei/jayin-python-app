import googlemaps
from datetime import datetime

API_key='AIzaSyD7wd8RcWDZ5xEgsfnnNBJOAzckp6uKgzw'

client = googlemaps.Client(key=API_key)
client.directions("Sydney", "Melbourne")
exit()


gmaps = googlemaps.client()

# geocoding an address
geocode_result = gmaps.geocode('1600 amphitheatre parkway, mountain view, ca')

# look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# request directions VIA public transit
now = datetime.now()
directions_result = gmaps.directions("sydney town hall",
                                     "parramatta, nsw",
                                     mode="transit",
                                     departure_time=now)

