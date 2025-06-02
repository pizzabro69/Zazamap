from django.contrib import admin
from .models import MapPin, Review, Badge, UserBadge, Profile

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

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color', 'created_at')
    search_fields = ('name', 'description')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at', 'awarded_by')
    list_filter = ('badge', 'awarded_at')
    search_fields = ('user__username', 'badge__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email')
    search_fields = ('user__username', 'user__email')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
