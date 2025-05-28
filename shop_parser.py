import os
import django
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mapproject.settings')
django.setup()

from mapapp.models import MapPin

def insert_shops_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    shops = data.get('shops', [])
    for shop in shops:
        # Avoid duplicates by name and lat/lng
        if MapPin.objects.filter(title=shop['name'], latitude=shop['lat'], longitude=shop['lng']).exists():
            print(f"Skipping existing: {shop['name']}")
            continue
        pin = MapPin(
            title=shop['name'],
            description=f"{shop['street']} {shop['number']}, {shop['zipcode']} {shop['city']}\nPhone: {shop['phone_number']}",
            latitude=shop['lat'],
            longitude=shop['lng'],
            category='dispensary',
            has_seating=False,
            is_scenic=False,
            is_sheltered=False,
            is_private=False,
            is_accessible=True,
            security_level=1,
        )
        pin.save()
        print(f"Inserted: {shop['name']}")

if __name__ == "__main__":
    insert_shops_from_json('shops.json')