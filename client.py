import requests

data = requests.post('http://127.0.0.1:5000/user',
                     json={
                         'name': 'tupo_user',
                         'password': 'Tupo_user_123!',
                         'email': 'tupo_user@mail.ru'
                     })

print(data.status_code)
print(data.text)

data = requests.get('http://127.0.0.1:5000/user/1')

print(data.status_code)
print(data.text)
