import requests
from pprint import pprint

# data = requests.post('http://127.0.0.1:5000/user',
#                      json={
#                          'name': 'Second_user',
#                          'password': 'Second_user_123!',
#                          'email': 'second_user@mail.ru'
#                      })
#
# print(data.status_code)
# print(data.text)
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
                         'title': 'first adv title',
                         'description': 'adv description',
                         'user_id': '1'
                     })

print(data.status_code)
pprint(data.text)
