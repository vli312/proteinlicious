from datetime import datetime, date, timedelta

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.contrib.auth.models import User
from django.urls import reverse
from actions.models import Action


# Create your models here.

# model for list.html
class recipe_story_list(models.Model):
    source = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    protein = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=50)
    userFK = models.ForeignKey(User, on_delete=models.CASCADE, default=7)
    comments = models.IntegerField(default=0)

# model for the two detail pages
class recipe_detail(models.Model):
    title = models.CharField(max_length=200)
    user = models.CharField(max_length=50)
    userFK = models.ForeignKey(User, on_delete=models.CASCADE, default=7)
    date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=100)
    commentsNum = models.IntegerField(default=0)
    ingredients = ArrayField(models.CharField(), blank=True, default=list)
    nutrition = JSONField()
    instructions = ArrayField(models.CharField(), blank=True, default=list)
    gallery = models.CharField(max_length=200, blank=True)
    actions = GenericRelation('actions.Action', object_id_field='target_id', content_type_field='target_ct')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe:recipe_detail_view", args=[self.id])
