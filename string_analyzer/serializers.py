from rest_framework import serializers
from .models import AnalyzedString
import hashlib
from collections import Counter
from rest_framework.exceptions import ValidationError

class AnalyzedStringSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='sha256_hash', read_only=True)
    properties = serializers.SerializerMethodField()

    class Meta:
        model = AnalyzedString
        fields = ['id', 'value', 'properties', 'created_at']
        read_only_fields = ['id', 'properties', 'created_at']

    def get_properties(self, obj):
        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'sha256_hash': obj.sha256_hash,
            'character_frequency_map': obj.character_frequency_map
        }

    def validate(self, data):
        value = data.get('value')
        if not value:
            raise ValidationError({"value": ["This field is required."]}, code=422)
        if not isinstance(value, str):
            raise ValidationError({"value": ["Must be a string."]}, code=422)
        sha256_hash = hashlib.sha256(value.encode()).hexdigest()
        if AnalyzedString.objects.filter(sha256_hash=sha256_hash).exists():
            raise ValidationError({"value": ["Analyzed string with this value already exists."]}, code=409)
        return data

    def create(self, validated_data):
        value = validated_data['value']
        sha256_hash = hashlib.sha256(value.encode()).hexdigest()
        instance = AnalyzedString(
            value=value,
            length=len(value),
            is_palindrome=value.lower() == value.lower()[::-1],  # Case-insensitive
            unique_characters=len(set(value)),
            word_count=len(value.split()),
            sha256_hash=sha256_hash,
            character_frequency_map=dict(Counter(value))
        )
        instance.save()
        return instance
            
