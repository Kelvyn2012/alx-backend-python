from rest_framework import viewsets
from django.http import HttpResponse
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


def home(request):
    return HttpResponse("Welcome to ALX Travel App v2!")


class ListingViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Listings"""

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Bookings"""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
