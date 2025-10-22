import hashlib
from collections import Counter

def analyze_string(value: str):
    cleaned_value = value.strip()
    length = len(cleaned_value)
    is_palindrome = cleaned_value.lower() == cleaned_value[::-1].lower()
    unique_characters = len(set(cleaned_value))
    word_count = len(cleaned_value.split())
    char_freq = dict(Counter(cleaned_value))
    sha_hash = hashlib.sha256(cleaned_value.encode('utf-8')).hexdigest()
    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha_hash,
        "character_frequency_map": char_freq
    }
