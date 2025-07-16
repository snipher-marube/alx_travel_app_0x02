import requests
from decouple import config
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from .models import Listing, Booking, Payment
from rest_framework.response import Response
from rest_framework import status
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        # Trigger async email task
        send_booking_confirmation.delay(booking.id)
        return booking

CHAPA_SECRET_KEY = config('CHAPA_SECRET_KEY')
CHAPA_BASE_URL = 'https://api.chapa.co/v1/transaction'

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def initiate_payment(self, request, pk=None):
        booking = self.get_object()
        
        # Create payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price
        )

        # Prepare Chapa API request
        headers = {
            'Authorization': f'Bearer {CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'amount': str(booking.total_price),
            'currency': 'ETB',
            'email': booking.user.email,
            'first_name': booking.user.first_name or 'User',
            'last_name': booking.user.last_name or '',
            'tx_ref': f'booking_{booking.id}',
            'callback_url': f'{settings.BASE_URL}/api/payments/verify/{payment.id}/',
            'return_url': f'{settings.FRONTEND_URL}/bookings/{booking.id}/payment-complete/',
            'customization': {
                'title': 'ALX Travel Booking',
                'description': f'Payment for booking #{booking.id}'
            }
        }

        try:
            response = requests.post(
                f'{CHAPA_BASE_URL}/initialize',
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            payment.transaction_id = data.get('data', {}).get('tx_ref')
            payment.save()
            
            return Response({
                'payment_url': data.get('data', {}).get('checkout_url'),
                'payment_id': payment.id
            })
        except requests.exceptions.RequestException as e:
            payment.status = 'FAILED'
            payment.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='verify/(?P<payment_id>[^/.]+)')
    def verify_payment(self, request, payment_id=None):
        payment = Payment.objects.get(id=payment_id)
        
        headers = {
            'Authorization': f'Bearer {CHAPA_SECRET_KEY}'
        }
        
        try:
            response = requests.get(
                f'{CHAPA_BASE_URL}/verify/{payment.transaction_id}/',
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'success':
                payment.status = 'COMPLETED'
                payment.booking.status = 'CONFIRMED'
                payment.booking.save()
                payment.save()
                
                # Send confirmation email (Celery task would go here)
                send_booking_confirmation.delay(payment.booking.id)
                return Response({'status': 'Payment verified successfully'})
            else:
                payment.status = 'FAILED'
                payment.save()
                return Response(
                    {'error': 'Payment verification failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )