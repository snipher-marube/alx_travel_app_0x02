from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/payments/verify/<uuid:payment_id>/', 
         BookingViewSet.as_view({'get': 'verify_payment'}), 
         name='verify-payment'),
]