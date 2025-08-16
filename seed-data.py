import os
import django
from datetime import date, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_reservation.settings')
django.setup()

from hotel.models import RoomType, Room, Guest, Booking

def load_sample_data():
    print("Loading sample data...")
    
    # Create room types
    print("Creating room types...")
    
    standard = RoomType.objects.get_or_create(
        name="Standard Single",
        defaults={
            'description': "Comfortable single room with city view and modern amenities",
            'base_price': 89.00,
            'max_occupancy': 2,
            'amenities': ["WiFi", "TV", "Air Conditioning", "Mini Bar", "Work Desk"]
        }
    )[0]

    deluxe = RoomType.objects.get_or_create(
        name="Deluxe Double",
        defaults={
            'description': "Spacious double room with ocean view and premium facilities",
            'base_price': 149.00,
            'max_occupancy': 3,
            'amenities': ["WiFi", "TV", "Air Conditioning", "Mini Bar", "Balcony", "Ocean View", "Coffee Machine"]
        }
    )[0]

    suite = RoomType.objects.get_or_create(
        name="Premium Suite",
        defaults={
            'description': "Luxury suite with separate living area and exclusive amenities",
            'base_price': 249.00,
            'max_occupancy': 4,
            'amenities': ["WiFi", "TV", "Air Conditioning", "Mini Bar", "Balcony", "Ocean View", "Jacuzzi", "Room Service", "Butler Service"]
        }
    )[0]

    executive = RoomType.objects.get_or_create(
        name="Executive Room",
        defaults={
            'description': "Business-class room with work area and executive lounge access",
            'base_price': 199.00,
            'max_occupancy': 2,
            'amenities': ["WiFi", "TV", "Air Conditioning", "Mini Bar", "Work Desk", "Executive Lounge Access", "Express Check-in"]
        }
    )[0]

    print(f"Created {RoomType.objects.count()} room types")

    # Create rooms
    print("Creating rooms...")
    
    room_data = [
        # Standard rooms (Floor 1)
        *[(f"10{i:02d}", standard, 1) for i in range(1, 11)],
        # Deluxe rooms (Floor 2)
        *[(f"20{i:02d}", deluxe, 2) for i in range(1, 11)],
        # Executive rooms (Floor 3)
        *[(f"30{i:02d}", executive, 3) for i in range(1, 8)],
        # Suites (Floor 4)
        *[(f"40{i:02d}", suite, 4) for i in range(1, 6)],
    ]

    for room_number, room_type, floor in room_data:
        Room.objects.get_or_create(
            room_number=room_number,
            defaults={
                'room_type': room_type,
                'floor_number': floor,
                'status': 'available'
            }
        )

    print(f"Created {Room.objects.count()} rooms")

    # Create sample guests
    print("Creating sample guests...")
    
    sample_guests = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0123',
            'nationality': 'United Kingdom'
        },
        {
            'first_name': 'Emily',
            'last_name': 'Davis',
            'email': 'emily.davis@example.com',
            'phone': '+33-1-42-86-83-33',
            'nationality': 'France'
        },
        {
            'first_name': 'David',
            'last_name': 'Wilson',
            'email': 'david.wilson@example.com',
            'phone': '+49-30-12345678',
            'nationality': 'Germany'
        },
        {
            'first_name': 'Sarah',
            'last_name': 'Brown',
            'email': 'sarah.brown@example.com',
            'phone': '+61-2-9876-5432',
            'nationality': 'Australia'
        },
        {
            'first_name': 'Carlos',
            'last_name': 'Rodriguez',
            'email': 'carlos.rodriguez@example.com',
            'phone': '+34-91-123-4567',
            'nationality': 'Spain'
        },
        {
            'first_name': 'Lisa',
            'last_name': 'Anderson',
            'email': 'lisa.anderson@example.com',
            'phone': '+46-8-123-456-78',
            'nationality': 'Sweden'
        }
    ]

    for guest_data in sample_guests:
        Guest.objects.get_or_create(
            email=guest_data['email'],
            defaults=guest_data
        )

    print(f"Created {Guest.objects.count()} guests")

    # Create sample bookings
    print("Creating sample bookings...")
    
    guests = list(Guest.objects.all())
    rooms = list(Room.objects.all())
    
    # Create bookings for the next 3 months
    start_date = date.today() + timedelta(days=1)
    
    booking_statuses = ['confirmed', 'checked_in', 'checked_out', 'cancelled']
    
    for i in range(20):  # Create 20 sample bookings
        guest = random.choice(guests)
        room = random.choice(rooms)
        
        # Random check-in date within next 90 days
        days_ahead = random.randint(1, 90)
        check_in = start_date + timedelta(days=days_ahead)
        
        # Random stay length (1-7 nights)
        nights = random.randint(1, 7)
        check_out = check_in + timedelta(days=nights)
        
        # Random number of guests
        adults = random.randint(1, min(3, room.room_type.max_occupancy))
        children = random.randint(0, max(0, room.room_type.max_occupancy - adults))
        
        # Calculate total amount
        total_amount = room.room_type.base_price * nights
        
        # Random status (mostly confirmed for future bookings)
        if check_in > date.today():
            status = random.choice(['confirmed', 'confirmed', 'confirmed', 'cancelled'])
        else:
            status = random.choice(['checked_out', 'checked_out', 'checked_in'])
        
        # Check if room is already booked for these dates
        overlapping = Booking.objects.filter(
            room=room,
            status__in=['confirmed', 'checked_in'],
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        ).exists()
        
        if not overlapping:
            special_requests = [
                "",
                "Late check-in requested",
                "High floor preference",
                "Extra towels please",
                "Early check-in if possible",
                "Quiet room requested",
                "Airport pickup needed"
            ]
            
            Booking.objects.get_or_create(
                guest=guest,
                room=room,
                check_in_date=check_in,
                check_out_date=check_out,
                defaults={
                    'adults': adults,
                    'children': children,
                    'total_amount': total_amount,
                    'status': status,
                    'special_requests': random.choice(special_requests)
                }
            )

    print(f"Created {Booking.objects.count()} bookings")

    # Print summary
    print("\n" + "="*50)
    print("SAMPLE DATA LOADED SUCCESSFULLY!")
    print("="*50)
    print(f"Room Types: {RoomType.objects.count()}")
    print(f"Rooms: {Room.objects.count()}")
    print(f"Guests: {Guest.objects.count()}")
    print(f"Bookings: {Booking.objects.count()}")
    print("\nBreakdown by room type:")
    for room_type in RoomType.objects.all():
        count = room_type.rooms.count()
        print(f"  {room_type.name}: {count} rooms")
    
    print("\nBooking status breakdown:")
    for status in ['confirmed', 'checked_in', 'checked_out', 'cancelled']:
        count = Booking.objects.filter(status=status).count()
        print(f"  {status.title()}: {count}")
    
    print("\n" + "="*50)
    print("You can now:")
    print("1. Start the Django server: python manage.py runserver")
    print("2. Access admin panel: http://localhost:8000/admin/")
    print("3. Test API endpoints: http://localhost:8000/api/")
    print("4. Use the frontend React application")
    print("="*50)

if __name__ == '__main__':
    load_sample_data()
    print("Sample data loading complete.")
    print("You can now run the Django server and test the application.")
    print("Run: python manage.py runserver")
    print("Visit: http://localhost:8000/admin/ to manage data.")
    print("Visit: http://localhost:8000/api/ to test API endpoints.")
    print("Visit: http://localhost:3000/ to use the frontend application.")
    print("Enjoy your hotel reservation system!")   