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
