from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime, date
from .models import Room, Booking
from .serializers import (
    RoomSerializer, BookingSerializer, 
    BookingCreateSerializer,BookingListSerializer
)

class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        queryset = Room.objects.select_related('room_type').filter(status='available')
        
        # Filter by dates
        check_in = self.request.query_params.get('check_in')
        check_out = self.request.query_params.get('check_out')
        
        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                
                # Filter rooms that are available for the date range
                available_rooms = []
                for room in queryset:
                    if room.is_available(check_in_date, check_out_date):
                        available_rooms.append(room.id)
                
                queryset = queryset.filter(id__in=available_rooms)
            except ValueError:
                pass  # Invalid date format, ignore filtering
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            try:
                queryset = queryset.filter(room_type__base_price__gte=float(min_price))
            except ValueError:
                pass
        
        if max_price:
            try:
                queryset = queryset.filter(room_type__base_price__lte=float(max_price))
            except ValueError:
                pass
        
        # Filter by amenities
        amenities = self.request.query_params.get('amenities')
        if amenities:
            amenity_list = [a.strip() for a in amenities.split(',')]
            for amenity in amenity_list:
                queryset = queryset.filter(room_type__amenities__contains=[amenity])
        
        # Filter by occupancy
        guests = self.request.query_params.get('guests')
        if guests:
            try:
                queryset = queryset.filter(room_type__max_occupancy__gte=int(guests))
            except ValueError:
                pass
        
        return queryset.order_by('room_number')

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.select_related('guest', 'room', 'room__room_type')
    serializer_class = BookingListSerializer
    def get_queryset(self):
        queryset = Booking.objects.select_related('guest', 'room', 'room__room_type')
        return queryset.order_by('-created_at')

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        # Return full booking details
        response_serializer = BookingSerializer(booking)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.select_related('guest', 'room', 'room__room_type')
    serializer_class = BookingSerializer
    lookup_field = 'id'

class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
    
    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        
        # Only allow cancellation for now
        if 'status' in request.data and request.data['status'] == 'cancelled':
            if booking.status in ['confirmed', 'pending']:
                booking.status = 'cancelled'
                booking.save()
                serializer = self.get_serializer(booking)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Booking cannot be cancelled in current status'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {'error': 'Only cancellation is allowed'},
            status=status.HTTP_400_BAD_REQUEST
        )
