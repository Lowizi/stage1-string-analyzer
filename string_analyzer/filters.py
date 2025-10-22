from django.db.models import Q

def apply_filters(queryset, params):
    # params is expected to be a dict with typed values (bools/ints/str)
    if not params:
        return queryset

    if 'is_palindrome' in params:
        queryset = queryset.filter(is_palindrome=bool(params['is_palindrome']))

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


def validate_filter_params(query_params):
    """Validate and coerce query parameters from request.query_params (QueryDict or dict).

    Returns a dict of typed parameters or raises ValueError for invalid input.
    """
    params = {}
    # accept both QueryDict and plain dict
    get = query_params.get

    if get('is_palindrome') is not None:
        val = get('is_palindrome')
        if isinstance(val, bool):
            params['is_palindrome'] = val
        else:
            lv = str(val).lower()
            if lv in ('true', 'false'):
                params['is_palindrome'] = lv == 'true'
            else:
                raise ValueError('is_palindrome must be true or false')

    if get('min_length') is not None:
        try:
            params['min_length'] = int(get('min_length'))
        except Exception:
            raise ValueError('min_length must be an integer')

    if get('max_length') is not None:
        try:
            params['max_length'] = int(get('max_length'))
        except Exception:
            raise ValueError('max_length must be an integer')

    if get('word_count') is not None:
        try:
            params['word_count'] = int(get('word_count'))
        except Exception:
            raise ValueError('word_count must be an integer')

    if get('contains_character') is not None:
        c = get('contains_character')
        if not isinstance(c, str) or len(c) == 0:
            raise ValueError('contains_character must be a non-empty string')
        params['contains_character'] = c[0]

    return params
