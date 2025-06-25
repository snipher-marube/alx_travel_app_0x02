from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, and reviews'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        self.create_users()
        self.create_listings()
        self.create_bookings()
        self.create_reviews()
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))

    def create_users(self):
        if User.objects.count() > 0:
            return

        # Create admin user
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )

        # Create regular users
        for i in range(5):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )

    def create_listings(self):
        if Listing.objects.count() > 0:
            return

        users = User.objects.all()
        property_types = [choice[0] for choice in Listing.PROPERTY_TYPES]
        amenities = [
            'WiFi', 'Kitchen', 'Parking', 'Pool', 'Air Conditioning',
            'Heating', 'Washer', 'Dryer', 'TV', 'Workspace'
        ]

        for i in range(20):
            owner = random.choice(users)
            amenities_sample = random.sample(amenities, random.randint(2, 6))
            
            Listing.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                address=fake.address(),
                city=fake.city(),
                price_per_night=random.randint(50, 500),
                property_type=random.choice(property_types),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                max_guests=random.randint(1, 10),
                amenities=amenities_sample,
                owner=owner
            )

    def create_bookings(self):
        if Booking.objects.count() > 0:
            return

        users = User.objects.all()
        listings = Listing.objects.all()
        statuses = [choice[0] for choice in Booking.STATUS_CHOICES]

        for i in range(30):
            user = random.choice(users)
            listing = random.choice(listings)
            start_date = fake.date_between(start_date='-30d', end_date='+30d')
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            Booking.objects.create(
                listing=listing,
                user=user,
                start_date=start_date,
                end_date=end_date,
                status=random.choice(statuses)
            )

    def create_reviews(self):
        if Review.objects.count() > 0:
            return

        users = User.objects.all()
        listings = Listing.objects.all()

        for listing in listings:
            for i in range(random.randint(1, 3)):
                user = random.choice(users)
                Review.objects.create(
                    listing=listing,
                    user=user,
                    rating=random.randint(1, 5),
                    comment=fake.paragraph(nb_sentences=3)
                )