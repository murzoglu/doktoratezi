import urllib.request
import json
import urllib.parse

query = urllib.parse.quote("A triadic perspective on control perceptions in youth with type 1 diabetes and their parents Prikken")
url = f"https://api.crossref.org/works?query={query}&select=title,abstract,author,DOI&rows=1"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    items = data['message']['items']
    if items:
        print(items[0]['title'])
        print(items[0].get('abstract', 'No abstract available'))
