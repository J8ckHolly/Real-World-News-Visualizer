import json
import requests
import creds

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
response.encoding = 'utf-8'
# Assuming the response is JSON
for data in response.json()['items']:
    pass
    #print(data['title'])

