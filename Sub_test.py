import requests

url = 'http://localhost:8888/5000'

files = {'file': open('ex4.rdf', 'rb')}

r = requests.post(url, files=files)
r.text