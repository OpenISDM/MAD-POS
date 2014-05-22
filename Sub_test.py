import requests

url = 'http://localhost:8888/callback'
headers = {'enctype': 'multipart/form-data'}
files = {'image': open('./Resource/image.jpg', 'rb'),
         'rdf': open('./Resource/ex4.rdf', 'rb')}

print files

r = requests.post(url, files=files)
print r.text
