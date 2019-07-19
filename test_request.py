import requests
import json
import cv2

# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

URL = 'http://localhost:5000/predict'

content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('images/frame.jpg')

_, img_encoded = cv2.imencode('.jpg', img)

response = requests.post(URL, data=img_encoded.tostring(), headers=headers)

print(json.loads(response.text))
