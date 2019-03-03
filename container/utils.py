
#### images utils
import requests, cv2
import numpy as np
from PIL import Image
import os, re, base64, io

IMG_EXT = ["jpg", "jpeg", "png", "bmp"]

IMG_DIR = "images"

def is_downloadable(url):
	# does url contain a downloadable resource
	h = requests.head(url, allow_redirects=True)
	header = h.headers
	content_type = header.get("content-type")
	if "text" in content_type.lower():
		return False
	if "html" in content_type.lower():
		return False

	# target file should smaller thant 5MB
	content_length = header.get("contect-length", None)
	if content_length and content_length > 5e7:
		return False

	return True

def get_name(url):
	if url.find("/"):
		return url.rsplit("/", 1)[1]

def download_image(url, taskid_dir,image_name):
	r = requests.get(url)

	if not os.path.exists(IMG_DIR):
		os.mkdir(IMG_DIR)
	if not os.path.exists(taskid_dir):
		os.mkdir(taskid_dir)

	with open(os.path.join(taskid_dir,image_name), "wb") as f:
		f.write(r.content)

	return True

######
def is_URL(url):
	if re.match(r'^https?:/{2}\w.+$', url):
		return True

	# 	error_msg = "Not a valid URL"


def url_cv2image(image_url):
	request_content = requests.get(image_url).content
	image_pil = Image.open(io.BytesIO(request_content))
	image_np = np.array(image_pil)
	if image_pil.mode == "RGB":
		cv2_converter = cv2.COLOR_RGB2BGR
	if image_pil.mode == "RGBA":
		cv2_converter = cv2.COLOR_RGBA2BGR
	if image_pil.mode == "L":
		cv2_converter = cv2.COLOR_GRAY2BGR
	image = cv2.cvtColor(image_np, cv2_converter)
	return image

def base64_cv2image(base64_data):
	image_data = base64.b64decode(base64_data)
	np_array = np.fromstring(image_data, np.uint8)
	image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
	return image

def save_base64_image(base64_data, image_name):
	image = base64_cv2image(base64_data)
	cv2.imwrite(image_name, image)
	return True

def image_base64str(file_name):
	with open(file_name, "rb") as image_file:
		image_bytes = base64.b64encode(image_file.read())
		# str(image_bytes, "utf-8")
	return image_bytes.decode()

def post_imgbase64str(api_endpoint, **data):
	return requests.post(url=api_endpoint, json=data)

########

def is_request_data(key_data, bytes_data):
	str_data = str(bytes_data, "utf-8")
	if key_data in str_data:
		key_data_first = key_data.split(":")[0]
		if key_data in key_data_first:
			return True

	# 		error_msg = "Not a vaild key in request data"



def is_download_image(url):
	if is_URL(url):
		image_name = get_name(url)
	else:
		return False


######## Logging #########

def mklogdir_writelog(file_name):
	log_dir = "log"
	log_file = "error.log"
	log_file = file_name
	log_path = os.path.join(log_dir, log_file)
	if not os.path.exists(log_dir):
		os.mkdir(log_dir)
	return True

import logging
from logging import handlers

class Logger:
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,
                 filename,
                 level='info',
                 when='D',
                 backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        self.logger = logging.getLogger(filename)

        format_str = logging.Formatter(fmt)#设置日志格式

        self.logger.setLevel(self.level_relations.get(level))#设置日志级别

        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式

        th = handlers.TimedRotatingFileHandler(filename=filename,
                                                       when=when,
                                                       backupCount=backCount,
                                                       encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式

        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)

if __name__ == '__main__':
    mklogdir_writelog("error.log")
    log = Logger('log/all.log',level='debug')
    # log.logger.debug('debug')
    # log.logger.info('info')
    # log.logger.warning('警告')
    log.logger.error('警告')
    # log.logger.critical('严重')
    # log.logger
    # Logger(log_path, level='error').logger.error('error')


