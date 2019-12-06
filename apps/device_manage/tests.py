from django.test import TestCase
import requests

base_url = 'http://127.0.0.1:8000/device_manage/'
data = {'type': 'tool'}
response = requests.post(f'{base_url}status/', json=data)
print(response)
