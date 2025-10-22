from django.db import models

# Create your models here.
import hashlib
from django.db import models
from django.utils import timezone

class StringEntry(models.Model):
    id = models.CharField(primary_key=True, max_length=64, editable=False)
    value = models.TextField(unique=True)
    length = models.PositiveIntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.PositiveIntegerField()
    word_count = models.PositiveIntegerField()
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = hashlib.sha256(self.value.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.value
