from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# from django.contrib.auth.models import User
class CodeSnippetImage(models.Model):
    image = models.BinaryField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)