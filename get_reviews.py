from config import cities
from trip_advisor_api import get_reviews_for_location, get_nearby_hotels
from utils import process_review, append_to_csv, get_collected_hotel_ids

total_reviews = 0
collected_hotel_ids = set(get_collected_hotel_ids('reviews.csv'))
print(len(collected_hotel_ids), "hotel IDs already collected.")

for city in cities:
    print(f"Fetching hotels for {city['city']}...")
    hotels = get_nearby_hotels(city['latitude'], city['longitude'])
    print(f"Found {len(hotels)} hotels in {city['city']}.")

    for hotel in hotels:
        if hotel.get('location_id') in collected_hotel_ids:
            print(f"Skipping {hotel.get('name')} (Location ID: {hotel.get('location_id')}) - already collected.")
            continue

        hotel_name = hotel.get('name')
        location_id = hotel.get('location_id')

        print(f"Fetching reviews for {hotel_name} (Location ID: {location_id})...")
        reviews = get_reviews_for_location(location_id, 100)
        print(f"Found {len(reviews)} reviews for {hotel_name}.")

        for review in reviews:
            processed_review = process_review(review, hotel)
            print(processed_review)
            append_to_csv(processed_review, 'reviews.csv')
            total_reviews += 1
            print(f"Total reviews fetched so far: {total_reviews}")

        collected_hotel_ids.add(location_id)