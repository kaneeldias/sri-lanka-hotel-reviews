def process_review(review, hotel):
    processed_review = {
        'review_id': review.get('id'),
        'review_url': review.get('url'),
        'location_id': review.get('location_id'),
        'hotel_name': hotel.get('name'),
        'city': hotel.get('address_obj', {}).get('city'),
        'timestamp': review.get('published_date'),
        'rating': review.get('rating'),
        'title': review.get('title'),
        'text': review.get('text'),
        'travel_date': review.get('travel_date'),
        'username': review.get('user', {}).get('username'),
        'value_rating': review.get('subratings', {}).get('0', {}).get('value'),
        'room_rating': review.get('subratings', {}).get('1', {}).get('value'),
        'location_rating': review.get('subratings', {}).get('2', {}).get('value'),
        'cleanliness_rating': review.get('subratings', {}).get('3', {}).get('value'),
        'service_rating': review.get('subratings', {}).get('4', {}).get('value'),
        'sleep_rating': review.get('subratings', {}).get('5', {}).get('value'),
    }
    return processed_review

def append_to_csv(row: dict, csv_path: str):
    import csv
    from pathlib import Path

    file_path = Path(csv_path)
    file_exists = file_path.exists()

    with file_path.open('a', newline='', encoding='utf-8') as csvfile:
        fieldnames = row.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header only if file does not exist

        writer.writerow(row)

def get_collected_hotel_ids(csv_path: str):
    import csv
    from pathlib import Path

    file_path = Path(csv_path)
    if not file_path.exists():
        return set()

    collected_ids = set()
    with file_path.open('r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            collected_ids.add(row['location_id'])

    return collected_ids