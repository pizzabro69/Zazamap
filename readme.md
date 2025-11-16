# Zaza Map

A Django + Leaflet playground for discovering smoke spots and dispensaries, complete with user accounts, amenity-rich map pins, ratings, favorites, and private messaging.

## Features

- **Interactive Leaflet map** with custom markers, clustering, geolocation, and pin placement mode.
- **Rich pin metadata**: amenities (seating, shelter, privacy, accessibility, discretion levels) plus optional photos.
- **Community contributions**: authenticated users can add, review, favorite, and delete their own pins.
- **Profiles & avatars** with stats (pins, favorites, reviews) and a favorites tab.
- **Direct messaging** between users, inbox view with unread counts, and AJAX message polling.
- **Utility scripts** such as `shop_parser.py` for bulk-importing dispensaries from `shops.json`.

## Getting started

### Prerequisites

- Python 3.11+
- A virtual environment (recommended)

### Installation

```powershell
cd Zazamap
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

The settings module now reads from environment variables. Create a `.env` or export the following (defaults work for local dev):

| Variable | Purpose | Default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Secret key for crypto signing | `dev-insecure-secret-key` |
| `DJANGO_DEBUG` | Enable Django debug mode | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames | `zaza-map.social,127.18.0.4,localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | `https://zaza-map.social` |

### Database & static assets

```powershell
python manage.py migrate
python manage.py collectstatic
```

### Run the app

```powershell
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and create an account to start contributing pins.

### Tests

```powershell
python manage.py test
```

### Bulk import shops (optional)

```powershell
python shop_parser.py
```

## Assets & credits

- Duck GIF: <https://media1.giphy.com/media/S1SnLg08CxnUGqyqha/giphy.gif>
- Weed icon: <https://opengameart.org/content/cannabis-sativa>
- Shop icon set: <https://opengameart.org/content/2d-shop-set>