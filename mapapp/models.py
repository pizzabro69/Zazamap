from django.db import models
from django.contrib.auth.models import User

class MapPin(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='pin_images/', null=True, blank=True)
    
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
