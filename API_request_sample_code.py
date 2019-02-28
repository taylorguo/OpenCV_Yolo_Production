import base64
import requests

def image_base64str(file_name):
	with open(file_name, "rb") as image_file:
		image_bytes = base64.b64encode(image_file.read())
		# str(image_bytes, "utf-8")
	return image_bytes.decode()

def post_imgbase64str(api_endpoint, **data):
	return requests.post(url=api_endpoint, json=data)


API_ENDPOINT = "http://127.0.0.1:5000/predict"

file_name = "images/brush_cup.png"

data = {'image': image_base64str(file_name)}

# r =  post_imgbase64str(API_ENDPOINT, **data)
r = requests.post(url=API_ENDPOINT, json=data)

print(r.text)
