from rest_framework import serializers
from .models import StringEntry
from .utils import analyze_string

class StringEntrySerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = StringEntry
        fields = ['id', 'value', 'properties', 'created_at']

    def get_properties(self, obj):
        return {
            "length": obj.length,
            "is_palindrome": obj.is_palindrome,
            "unique_characters": obj.unique_characters,
            "word_count": obj.word_count,
            "sha256_hash": obj.id,
            "character_frequency_map": obj.character_frequency_map
        }

class CreateStringSerializer(serializers.Serializer):
    value = serializers.CharField()

    def validate_value(self, value):
        # DRF will coerce JSON types; ensure incoming value is a string
        if value is None:
            raise serializers.ValidationError("Value is required.")
        if not isinstance(value, str):
            raise serializers.ValidationError({
                'code': 'invalid_type',
                'message': 'Value must be a string.'
            })
        if not value.strip():
            raise serializers.ValidationError("Value cannot be empty.")
        return value

    def create(self, validated_data):
        value = validated_data['value']
        props = analyze_string(value)
        entry = StringEntry.objects.create(
            id=props['sha256_hash'],
            value=value,
            length=props['length'],
            is_palindrome=props['is_palindrome'],
            unique_characters=props['unique_characters'],
            word_count=props['word_count'],
            character_frequency_map=props['character_frequency_map']
        )
        return entry
