from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(upload_to='profile_images/')
    address = models.TextField()
    otp = models.CharField(max_length=6)
    email_verified = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return self.user.username
