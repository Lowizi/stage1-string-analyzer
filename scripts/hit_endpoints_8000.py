import requests
import json

BASE = 'http://localhost:8000'

endpoints = [
    ('POST', '/strings/', {'value': 'radar'}),
    ('GET', '/strings?min_length=5&max_length=10', None),
    ('GET', '/strings?word_count=1', None),
    ('GET', '/strings?contains_character=z', None),
    ('GET', '/strings/filter-by-natural-language/?query=palindromic+strings', None),
    ('DELETE', '/strings/radar/', None),
    ('DELETE', '/strings/nonexistent_delete_xyz_98765/', None),
]

for method, path, data in endpoints:
    url = BASE + path
    try:
        if method == 'POST':
            r = requests.post(url, json=data)
        elif method == 'GET':
            r = requests.get(url)
        elif method == 'DELETE':
            r = requests.delete(url)
        else:
            continue
    except Exception as e:
        print(method, path, 'ERROR:', e)
        continue

    print('---')
    print(method, url)
    print('Status:', r.status_code)
    try:
        print('Body:', json.dumps(r.json(), indent=2))
    except Exception:
        print('Body:', r.text)
