import urllib.request
import urllib.error
import json

base = 'http://127.0.0.1:8001'
endpoints = [
    {"method": "POST", "url": f"{base}/strings/", "data": {"value": "radar"}},
    {"method": "GET", "url": f"{base}/strings?min_length=5&max_length=10"},
    {"method": "GET", "url": f"{base}/strings?word_count=1"},
    {"method": "GET", "url": f"{base}/strings?contains_character=z"},
    {"method": "GET", "url": f"{base}/strings/filter-by-natural-language/?query=palindromic+strings"},
    {"method": "DELETE", "url": f"{base}/strings/radar/"},
    {"method": "DELETE", "url": f"{base}/strings/nonexistent_delete_xyz_98765/"}
]

for ep in endpoints:
    method = ep['method']
    url = ep['url']
    data = ep.get('data')
    print('\n=== {} {} ==='.format(method, url))
    try:
        if data is not None:
            b = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=b, headers={'Content-Type': 'application/json'}, method=method)
        else:
            req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8')
            print('Status:', resp.getcode())
            if body:
                print('Body:')
                print(body)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
        except Exception:
            body = ''
        print('HTTPError:', e.code)
        if body:
            print('Body:')
            print(body)
    except Exception as ex:
        print('Error:', ex)
