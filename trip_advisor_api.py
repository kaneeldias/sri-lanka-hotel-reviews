import os
import requests

TRIP_ADVISOR_API_KEY = os.getenv("TRIP_ADVISOR_API_KEY")

def get_reviews_for_location(location_id, limit=1):
    reviews = []
    offset = 0
    while len(reviews) < limit:
        response = fetch_reviews(location_id, offset)
        if 'data' in response:
            reviews.extend(response['data'])
            if len(response['data']) < 5:
                break
            offset += len(response['data'])
        else:
            break

    return reviews

def fetch_reviews(location_id, offset):
    print("Making API call to TripAdvisor for location ID:", location_id, "with offset:", offset)
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews?language=en&offset={offset}&key={TRIP_ADVISOR_API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    return response.json()

def get_nearby_hotels(lat, lon):
    offsets = [0]
    latitudes = [lat + offset for offset in offsets]
    longitudes = [lon + offset for offset in offsets]
    hotel_list = []
    for latitude in latitudes:
        for longitude in longitudes:
            hotels = fetch_hotels(latitude, longitude)
            if 'data' in hotels and len(hotels['data']) > 0:
                print(f"Found {len(hotels['data'])} hotels at lat: {latitude}, lon: {longitude}")
                hotel_list.extend(hotels['data'])

    return hotel_list


def fetch_hotels(lat, lon):
    print("Making API call to TripAdvisor for nearby hotels at lat:", lat, "lon:", lon)
    url = f"https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong={lat}%2C%20{lon}&category=hotels&radius=10&radiusUnit=km&language=en&key={TRIP_ADVISOR_API_KEY}"
    print(url)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

