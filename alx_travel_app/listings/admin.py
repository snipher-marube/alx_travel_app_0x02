from django.contrib import admin

from .models import Booking, Listing, Review

admin.site.register(Booking)
admin.site.register(Listing)
admin.site.register(Review)
