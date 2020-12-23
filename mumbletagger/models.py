import requests
import json

from django.db import models
from django.contrib.auth.models import Group

class TagAssociation(models.Model):
    """Discord Webhook for pings"""
    tag = models.CharField(max_length=150)
    groups = models.ManyToManyField(Group, blank=True)
    enabled = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.tag)
