import requests
import json

# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

# URL = 'http://localhost:5000/predict'
URL = 'https://vehicle-collision.herokuapp.com/predict'

content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = open('images/frame.jpg', 'rb').read()
response = requests.post(URL, data=img, headers=headers)

print(json.loads(response.text))
