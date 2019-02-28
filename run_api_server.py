# coding:utf-8
from utils import is_downloadable, get_name, download_image, IMG_DIR, IMG_EXT
from utils import is_request_data, is_URL, url_cv2image, base64_cv2image
from utils import Logger, save_base64_image, mklogdir_writelog
from yolo import yolov3_detector, convert_result

import time, os
import numpy as np
from PIL import Image
from flask  import Flask, render_template, request, jsonify

app = Flask(__name__)

taskid = 0

detector = yolov3_detector()
net = detector.load_net_weights()

@app.route("/", methods=['GET'])
def homepage():
	# return render_template("index.html")
	return "Yolov3 Object Detection API"


def check_valid(func):

	def wrapper(*args,**kwargs):

		try:
			try_result = func(*args,**kwargs)
			return try_result
		except KeyError:
			code = 222101
			message = "not a valid key"
			res = {}
			error_msg = {"message": message, "code":code, "res":res}
			return error_msg


	return wrapper


@app.route("/predict", methods=['POST'])
def predict():

	res = data = {}
	error_code = 1
	error_msg = ""


	global taskid
	taskid += 1
	taskid_dir = "%06d"%taskid
	if not os.path.exists("tasks"):
		os.mkdir("tasks")
	full_taskid_dir = os.path.join("tasks", taskid_dir)
	if not os.path.exists(full_taskid_dir):
		os.mkdir(full_taskid_dir)

	log_dir = "log"
	log_file = "error.log"
	log_path = os.path.join(log_dir, log_file)
	mklogdir_writelog(log_file)
	log = Logger(log_path, level='error')

	image_data_value = ""

	s = time.time()

	if request.method == "POST":

		if is_request_data("image", request.data):
			req_data = request.get_json()
			# print(request.data)
			# req_data = json.loads(request.data.decode("utf-8"), strict=False)
			image_data = req_data["image"]
			image_data_value = ""

			if is_URL(image_data):
				image_name = get_name(image_data)
				image_data_value = image_data
				if not image_name.split(".")[-1] in IMG_EXT:
					error_code = 222102
					error_msg = "Wrong image format, should be [.jpg, .jpeg, .png, .bmp]"
					log.logger.error("{}-{}-{}-{}".format(taskid_dir,image_data_value,error_code,error_msg))
				try:
					image = url_cv2image(image_data)

				except Exception:
					error_code = 222103
					error_msg = "Can't download image"
					res = {}
					log.logger.error("{}-{}-{}-{}".format(taskid_dir,image_data_value, error_code,error_msg))
				else:
					result = detector.object_detector(net, image)
					res = convert_result(result)
					error_code = 0

					download_image(image_data, full_taskid_dir, image_name)

			else:
				try:
					image = base64_cv2image(image_data)

				except Exception:
					error_code = 222104
					error_msg = "Wrong string to an image"
					image_data_value = "wrong_str"
					res = {}
					log.logger.error("{}-{}-{}-{}".format(taskid_dir,image_data_value, error_code,error_msg))
				else:
					result = detector.object_detector(net, image)
					res = convert_result(result)
					error_code = 0

					image_data_value =  "base64str"
					# convert base64str to image
					# save image to taskid_dir/image.ext
					save_base64_image(image_data, os.path.join(full_taskid_dir,taskid_dir+".jpg"))

		else:
			error_code = 222101
			error_msg = "Not a vaild key in requested data"
			log.logger.error("{}-{}-{}".format(taskid_dir,error_code,error_msg))

		res.update({"taskid": taskid, "image": image_data_value})

		data.update({"code": error_code, "message":error_msg, "data":res})
		# data = {"image":image_data_value, "code": 0, "objects":result["names"], "rect":result["objects"]}



	print(" -  API takes {:.3f} seconds!\n".format(time.time()-s))

	return jsonify(data)

if __name__ == "__main__":
	print(" - Starting api service ...")
	app.run(host="127.0.0.1")
