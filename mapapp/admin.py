from django.contrib import admin
from .models import MapPin, Review

@admin.register(MapPin)
class MapPinAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude', 'created_at', 'user')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pin', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'pin__title', 'user__username')
