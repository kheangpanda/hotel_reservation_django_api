from django.urls import path
from .views import (
    RoomListView, BookingCreateView,
    BookingDetailView, BookingUpdateView,BookingListView
)

urlpatterns = [
    path('rooms', RoomListView.as_view(), name='room-list'),
    path('bookings', BookingListView.as_view(), name='booking-list'),
    path('bookings/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<uuid:id>', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<uuid:id>/update', BookingUpdateView.as_view(), name='booking-update'),
]
