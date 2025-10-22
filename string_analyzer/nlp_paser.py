class NaturalLanguageParseError(ValueError):
    pass


def parse_natural_language(query: str):
    """Parse a small subset of natural language queries into filter dicts.

    Supported heuristics (from spec examples):
      - "all single word palindromic strings" -> {'word_count': 1, 'is_palindrome': True}
      - "strings longer than 10 characters" -> {'min_length': 11}
      - "palindromic strings that contain the first vowel" -> {'is_palindrome': True, 'contains_character': 'a'}
      - "strings containing the letter z" -> {'contains_character': 'z'}

    Raises NaturalLanguageParseError on parse failure, ValueError on conflicting filters.
    """
    if not query or not isinstance(query, str):
        raise NaturalLanguageParseError('Query must be a non-empty string')

    q = query.lower().strip()
    parsed = {}

    if 'palindrom' in q:
        parsed['is_palindrome'] = True

    if 'single word' in q or 'one word' in q:
        parsed['word_count'] = 1

    # longer than N
    if 'longer than' in q:
        # try to extract the number after 'longer than'
        try:
            after = q.split('longer than', 1)[1]
            num = ''.join(ch for ch in after if ch.isdigit())
            if not num:
                raise NaturalLanguageParseError('Unable to parse length in query')
            parsed['min_length'] = int(num) + 1
        except IndexError:
            raise NaturalLanguageParseError('Unable to parse length in query')

    # first vowel heuristic
    if 'first vowel' in q:
        parsed['contains_character'] = 'a'

    # "containing the letter X" or "containing the letter x"
    if 'letter' in q and 'containing' in q:
        # look for the word 'letter' and take the next character token
        try:
            part = q.split('letter', 1)[1].strip()
            if not part:
                raise NaturalLanguageParseError('No letter found in query')
            # take first alphabetic character
            for ch in part:
                if ch.isalpha():
                    parsed['contains_character'] = ch
                    break
        except IndexError:
            raise NaturalLanguageParseError('No letter found in query')

    # direct "containing the letter z" or "containing z"
    if 'containing' in q and 'letter' not in q:
        # attempt to find a single-letter token
        tokens = q.split()
        for i, t in enumerate(tokens):
            if t == 'containing' and i + 1 < len(tokens):
                candidate = tokens[i + 1]
                for ch in candidate:
                    if ch.isalpha():
                        parsed['contains_character'] = ch
                        break
                break

    if not parsed:
        raise NaturalLanguageParseError('Unable to parse natural language query.')

    # conflicting filters check (example: min_length > max_length)
    if 'min_length' in parsed and 'max_length' in parsed:
        if parsed['min_length'] > parsed['max_length']:
            raise ValueError('Parsed filters are conflicting: min_length > max_length')

    return parsed
