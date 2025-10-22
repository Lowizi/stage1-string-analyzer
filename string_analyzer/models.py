from django.db import models

# Create your models here.
from django.db import models
import hashlib
from collections import Counter

class AnalyzedString(models.Model):
    value = models.TextField(unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only compute on creation
            self.length = len(self.value)
            self.is_palindrome = self.value.lower() == self.value.lower()[::-1]
            self.unique_characters = len(set(self.value))
            self.word_count = len(self.value.split())
            self.sha256_hash = hashlib.sha256(self.value.encode()).hexdigest()
            self.character_frequency_map = dict(Counter(self.value))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.value
