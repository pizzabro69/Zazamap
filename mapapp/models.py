from django.db import models
from django.contrib.auth.models import User

class MapPin(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=20, choices=[('smoke', 'Smoke Spot'), ('dispensary', 'Dispensary')], default='smoke')
    image = models.ImageField(upload_to='pin_images/', null=True, blank=True)
    
    # Add these amenity fields
    has_seating = models.BooleanField(default=False)
    is_scenic = models.BooleanField(default=False)
    is_sheltered = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_accessible = models.BooleanField(default=True)  # Default to accessible
    security_level = models.IntegerField(default=1, choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    
    def __str__(self):
        return self.title
    
    def average_rating(self):
        reviews = Review.objects.filter(pin=self)
        if reviews.count() > 0:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


class Review(models.Model):
    RATING_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    
    pin = models.ForeignKey(MapPin, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Prevent users from reviewing the same pin multiple times
        unique_together = ('pin', 'user')
    
    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star review of {self.pin.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    pin = models.ForeignKey(MapPin, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'pin')
        
    def __str__(self):
        return f"{self.user.username} - {self.pin.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_other_participant(self, user):
        """Get the other user in a two-person conversation"""
        return self.participants.exclude(id=user.id).first()
    
    class Meta:
        ordering = ['-updated_at']

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class (e.g., 'bi-trophy')")
    color = models.CharField(max_length=20, default="success", 
                            help_text="Bootstrap color class (e.g., 'success', 'primary', 'warning')")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                  related_name='badges_awarded', null=True)
    
    class Meta:
        unique_together = ('user', 'badge')
        
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
