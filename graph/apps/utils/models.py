from sqlite3 import Timestamp
from django.db import models

# Create your mcodels here.
class Timestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True