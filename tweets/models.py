from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    text = models.CharField(max_length=280)
    image = models.ImageField(upload_to='tweets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username if self.author else 'Anonymous'}: {self.text[:50]}..." 