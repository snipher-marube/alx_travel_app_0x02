# ALX Travel App - Database Modeling and Seeding

## Project Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Seed the database: `python manage.py seed`

## Models

- **Listing**: Represents properties available for booking
- **Booking**: Represents user bookings for listings
- **Review**: Represents user reviews for listings

## API Endpoints

- `/api/listings/` - List and create listings
- `/api/bookings/` - List and create bookings
- `/api/reviews/` - List and create reviews

## Seeding Data

The seed command creates:
- 1 admin user
- 5 regular users
- 20 listings
- 30 bookings
- 1-3 reviews per listing