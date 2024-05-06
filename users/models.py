from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.db import models
User=get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CodeSnippetImage(models.Model):
    image = models.BinaryField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

from django.contrib.auth import get_user_model
#from django

# Create your models here.

# User=get_user_model()
# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     id_user = models.IntegerField()
#     bio = models.TextField(blank=True)
#     profileimg = models.ImageField(upload_to='profile_images',default='blank-profile-picture.png')
#     location = models.CharField(max_length=100, blank = True)

#     def __str__(self):
#         return self.user.username

