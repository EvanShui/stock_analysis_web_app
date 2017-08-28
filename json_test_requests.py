import requests
import json as m_json

query = input ( 'Query: ' )
query = ( { 'q' : query } )
r = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&', params=query)
print(r.url)