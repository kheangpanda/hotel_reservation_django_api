# Hotel Reservation System

This project is a Django-based hotel reservation system for Squeeze Asia. It allows users to manage hotels, rooms, and reservations efficiently.

## Features

- Hotel and room management
- Reservation creation and management
- RESTful API endpoints
- Admin interface for hotel staff

## Project Structure

- `hotel_reservation/` - Django project settings and configuration
- `hotel/` - Main app containing models, views, serializers, and URLs
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `seed-data.py` - Script for populating initial data

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Django

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd hotel_reservation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. (Optional) Seed initial data:
   ```bash
   python seed-data.py
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

See `hotel/urls.py` for available endpoints. Example endpoints:

- `/api/hotels/` - List and create hotels
- `/api/rooms/` - List and create rooms
- `/api/reservations/` - Manage reservations

## Admin Panel

Access the Django admin panel at `/admin/` after creating a superuser:

```bash
python manage.py createsuperuser
```

## License

This project is licensed under the MIT License.