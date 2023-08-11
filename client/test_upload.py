import requests

url = 'http://127.0.0.1:8000/upload'
files = [('files', open('files/0.txt', 'rb')), ('files', open('files/1.txt', 'rb')),
         ('files', open('files/2.txt', 'rb'))]
resp = requests.post(url=url, files=files) 
print(resp.json())