from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@shared_task
def send_booking_confirmation(booking_id):
    booking = Booking.objects.get(id=booking_id)
    subject = f'Booking Confirmation #{booking.id}'
    message = f'''
    Thank you for your booking!
    
    Booking Details:
    - Property: {booking.listing.title}
    - Dates: {booking.start_date} to {booking.end_date}
    - Total: {booking.total_price} ETB
    
    We look forward to hosting you!
    '''
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [booking.user.email],
        fail_silently=False,
    )