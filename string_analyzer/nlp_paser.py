def parse_natural_language(query: str):
    query = query.lower().strip()
    parsed = {}

    # "all single word palindromic strings"
    if "palindromic" in query:
        parsed["is_palindrome"] = True

    if "single word" in query:
        parsed["word_count"] = 1

    # "strings longer than 10 characters"
    if "longer than" in query:
        parts = query.split()
        if "than" in parts:
            idx = parts.index("than")
            length_str = ''.join([c for c in parts[idx+1] if c.isdigit()])
            if length_str:
                parsed["min_length"] = int(length_str) + 1
            else:
                raise ValueError("Invalid length in query")

    # "palindromic strings that contain the first vowel"
    if "first vowel" in query:
        parsed["contains_character"] = "a"

    # "strings containing the letter z"
    if "letter" in query:
        letter_part = query.split("letter")[-1].strip()
        if letter_part:
            parsed["contains_character"] = letter_part[0]

    if not parsed:
        raise ValueError("Unable to parse natural language query.")

    return parsed
