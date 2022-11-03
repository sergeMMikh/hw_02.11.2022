import requests
from pprint import pprint

data = requests.post('http://127.0.0.1:5000/user',
                     json={
                         'name': 'fifth_user',
                         'password': 'Fifth_user_123%',
                         'email': 'fifth_user@mail.ru'
                     })

print(data.status_code)
pprint(data.text)

data = requests.post('http://127.0.0.1:5000/adv',
                     json={
                         'title': '4 adv title',
                         'description': 'adv description',
                         'name': 'fifth_user',
                         'password': 'Fifth_user_123%',
                     })

print(data.status_code)
pprint(data.text)
