from rest_framework import serializers
from .models import Room, RoomType, Guest, Booking
from datetime import date


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'description', 'base_price', 'max_occupancy', 'amenities']


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'floor_number', 'status']


class GuestSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Guest
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 
            'phone', 'address', 'date_of_birth', 'nationality'
        ]

class BookingListSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    nights = serializers.ReadOnlyField()
    total_guests = serializers.ReadOnlyField()
    can_be_cancelled = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = [
            'id', 'guest', 'room', 'check_in_date', 'check_out_date',
            'adults', 'children', 'total_guests', 'total_amount', 'status',
            'special_requests', 'booking_date', 'nights', 'can_be_cancelled'
        ]

class BookingSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    nights = serializers.ReadOnlyField()
    total_guests = serializers.ReadOnlyField()
    can_be_cancelled = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'guest', 'room', 'check_in_date', 'check_out_date',
            'adults', 'children', 'total_guests', 'total_amount', 'status',
            'special_requests', 'booking_date', 'nights', 'can_be_cancelled'
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    guest_details = GuestSerializer(write_only=True)
    room_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'guest_details', 'room_id', 'check_in_date', 'check_out_date',
            'adults', 'children', 'special_requests'
        ]
    
    def validate_check_in_date(self, value):
        print("Validating check-in date:", value)  # Debugging line
        print("date.today():", date.today())  # Debugging line
        if value < date.today():
            raise serializers.ValidationError("Check-in date must be in the future.")
        return value
    
    def validate(self, data):
        # Check dates are valid
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        # Check room availability
        try:
            room = Room.objects.get(id=data['room_id'])
        except Room.DoesNotExist:
            raise serializers.ValidationError("Room not found.")
        
        if not room.is_available(data['check_in_date'], data['check_out_date']):
            raise serializers.ValidationError("Room is not available for selected dates.")
        
        # Check occupancy
        # total_guests = data['adults'] + data['children']
        # if total_guests > room.room_type.max_occupancy:
        #     raise serializers.ValidationError(
        #         f"Too many guests. Maximum occupancy for this room: {room.room_type.max_occupancy}"
        #     )
        
        # Check minimum stay (at least 1 night)
        nights = (data['check_out_date'] - data['check_in_date']).days
        if nights < 1:
            raise serializers.ValidationError("Minimum stay is 1 night.")
        
        return data
    
    def create(self, validated_data):
        guest_data = validated_data.pop('guest_details')
        room_id = validated_data.pop('room_id')
        
        # Create or get guest
        guest, created = Guest.objects.get_or_create(
            email=guest_data['email'],
            defaults=guest_data
        )
        
        # If guest exists but has different details, update them
        if not created:
            for key, value in guest_data.items():
                if value:  # Only update non-empty values
                    setattr(guest, key, value)
            guest.save()
        
        # Get room and calculate total
        room = Room.objects.get(id=room_id)
        nights = (validated_data['check_out_date'] - validated_data['check_in_date']).days
        total_amount = room.room_type.base_price * nights
        
        # Create booking
        booking = Booking.objects.create(
            guest=guest,
            room=room,
            total_amount=total_amount,
            **validated_data
        )
        
        return booking


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status', 'special_requests']
    
    def validate_status(self, value):
        booking = self.instance
        if value == 'cancelled' and not booking.can_be_cancelled():
            raise serializers.ValidationError(
                f"Cannot cancel booking with status '{booking.status}'."
            )
        return value