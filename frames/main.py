import imutils
from config import Config

# Video Options
#rotate_degree = 90
#resize = 1.6 # for cam 2 for video 3
resize = Config().get("resize")
rotate_degree = Config().get("rotation")

def vidops(frame, camcrop=False):
	########################################
	# Операции с входным видео
	height, width, _ = frame.shape
	frame = imutils.resize(frame, int(width // resize), int(height // resize)) # resize

	if camcrop:
		frame = frame[0:width, round(height//1.9):height]
		#frame = frame[0:width, round(height//1.001):height] # Обрезка для сохранения ресурсов cpu
	
	frame = imutils.rotate_bound(frame, int(rotate_degree)) # rotate 

	########################################

	return frame