import requests
from pprint import pprint

data = requests.post('http://127.0.0.1:5000/user',
                     json={
                         'name': 'fird_user2',
                         'password': 'Fird_user_123%',
                         'email': 'fird_user@mail.ru'
                     })

print(data.status_code)
print(data.text)
#
# data = requests.get('http://127.0.0.1:5000/user/1')
#
# print(data.status_code)
# print(data.text)
#
# data = requests.get('http://127.0.0.1:5000/adv/1')
#
# print(data.status_code)
# print(data.text)

data = requests.post('http://127.0.0.1:5000/adv',
                     json={
                         'title': '5 adv title',
                         'description': 'adv description',
                         'name': 'fird_user2',
                         'password': 'Fird_user_123%',
                     })

print(data.status_code)
pprint(data.text)
