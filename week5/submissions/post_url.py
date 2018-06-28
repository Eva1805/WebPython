# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import json

url = 'http://79.137.175.13/submissions/1/'
login = 'alladin'
passw = 'opensesame'
res = requests.post(url,  auth=HTTPBasicAuth(login, passw))
r = res.json()
print(r)

url = 'http://79.137.175.13/submissions/super/duper/secret/'
login = 'galchonok'
passw = 'ktotama'
res = requests.put(url,  auth=HTTPBasicAuth(login, passw))
r = res.json()
print(r)
with open('answer.json', 'w') as f:
    json.dump(r, f)
with open('answer.json', 'r') as f:
    print(json.load(f))
