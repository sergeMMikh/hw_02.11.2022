import requests

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
data = requests.get('http://127.0.0.1:5000/user/2')

print(data.status_code)
print(data.text)

data = requests.get('http://127.0.0.1:5000/adv/1')

print(data.status_code)
print(data.text)
