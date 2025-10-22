from django.db.models import Q

def apply_filters(queryset, params):
    if 'is_palindrome' in params:
        val = params['is_palindrome'].lower() == 'true'
        queryset = queryset.filter(is_palindrome=val)

    if 'min_length' in params:
        queryset = queryset.filter(length__gte=int(params['min_length']))

    if 'max_length' in params:
        queryset = queryset.filter(length__lte=int(params['max_length']))

    if 'word_count' in params:
        queryset = queryset.filter(word_count=int(params['word_count']))

    if 'contains_character' in params:
        char = params['contains_character']
        queryset = queryset.filter(value__icontains=char)

    return queryset
