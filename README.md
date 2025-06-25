# Travel API Documentation

## API Endpoints

### Listings
- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create new listing
- `GET /api/listings/{id}/` - Get listing details
- `PUT /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing

### Bookings
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Get booking details
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Delete booking

## Swagger Documentation
Access interactive API documentation at:  
`http://localhost:8000/swagger/`

## Testing
1. Install requirements: `pip install -r requirements.txt`
2. Run server: `python manage.py runserver`
3. Test endpoints using:
   - Swagger UI
   - Postman
   - Curl commands (examples provided above)