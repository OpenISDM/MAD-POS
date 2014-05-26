import requests

topic = {
		'jpg': './Resource/image.jpg',
		'rdf'  : './Resource/ex4.rdf',
		'zip'  : './Resource/Archive.zip'
		}

url = 'http://localhost:888/callback'
headers = {'enctype': 'multipart/form-data'}

for x in topic:
	files = {'file': open(topic[x], 'rb')}
	print files
	r = requests.post(url, files=files)

print r.text
