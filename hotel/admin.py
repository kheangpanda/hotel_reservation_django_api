from django.contrib import admin
from .models import RoomType, Room, Guest, Booking

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'max_occupancy']
    list_filter = ['max_occupancy']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'floor_number', 'status']
    list_filter = ['room_type', 'status', 'floor_number']
    search_fields = ['room_number']

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    search_fields = ['first_name', 'last_name', 'email']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'guest', 'room', 'check_in_date', 'check_out_date', 'status', 'total_amount']
    list_filter = ['status', 'check_in_date']
    search_fields = ['guest__first_name', 'guest__last_name', 'room__room_number']
    readonly_fields = ['id', 'nights']
