from django.contrib import admin
from .models import MapPin

@admin.register(MapPin)
class MapPinAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude', 'created_at', 'user')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'description')
