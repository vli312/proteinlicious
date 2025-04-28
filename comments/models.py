from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from recipe.models import recipe_detail

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipe_detail = models.ForeignKey(recipe_detail, on_delete=models.CASCADE, related_name='comments')
