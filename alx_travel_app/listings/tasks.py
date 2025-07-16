from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_booking_confirmation(booking_id):
    """
    Sends booking confirmation email asynchronously
    """
    from .models import Booking
    
    try:
        booking = Booking.objects.get(id=booking_id)
        user = booking.user
        listing = booking.listing
        
        subject = f'Booking Confirmation for {listing.title}'
        html_message = render_to_string('emails/booking_confirmation.html', {
            'user': user,
            'booking': booking,
            'listing': listing
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        return f"Email sent to {user.email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"